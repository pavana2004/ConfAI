from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from sqlalchemy import distinct
from datetime import datetime
from typing import Dict

from database import engine, get_db, SessionLocal
from models import Base, User, Room, Booking
from auth import hash_password, verify_password, create_access_token, decode_token
from rooms import seed_rooms
from bookings import is_room_available
from booking_service import create_booking
from room_resolver import resolve_room_id
from auto_cancel import auto_cancel_expired_bookings
from time_utils import now_ist_naive
from intent_utils import infer_intent_from_text
from room_utils import extract_room_name
from participant_utils import extract_participants_from_text
from time_parser import extract_date_time
from chat_llm import call_llm
from chat_prompt import ask_missing_fields
from email_service import send_email
from ics_utils import generate_ics

# -------------------------------
# APP INIT
# -------------------------------

Base.metadata.create_all(bind=engine)

app = FastAPI(title="ConfAI Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# seed rooms once
db = SessionLocal()
seed_rooms(db)
db.close()

# -------------------------------
# AUTH
# -------------------------------

security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    payload = decode_token(credentials.credentials)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(User).filter(User.id == payload["user_id"]).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user

# -------------------------------
# BOOKING STATE
# -------------------------------

pending_bookings: Dict[int, dict] = {}

def empty_booking(intent: str):
    return {
        "intent": intent,
        "room_name": None,
        "date": None,
        "start_time": None,
        "end_time": None,
        "participants": []
    }

def merge_booking(existing: dict, new: dict):
    for k, v in new.items():
        if v is None:
            continue
        if k == "participants":
            existing[k] = list(set(existing[k] + v))
        else:
            existing[k] = v

# -------------------------------
# BASIC ROUTES
# -------------------------------

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/register")
def register(name: str, email: str, password: str, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == email).first():
        raise HTTPException(400, "User already exists")

    user = User(
        name=name,
        email=email,
        password=hash_password(password)
    )
    db.add(user)
    db.commit()
    return {"message": "Registered"}

@app.post("/login")
def login(email: str, password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.password):
        raise HTTPException(401, "Invalid credentials")

    token = create_access_token({
        "user_id": user.id,
        "email": user.email
    })

    return {"access_token": token, "token_type": "bearer"}

@app.get("/me")
def me(user: User = Depends(get_current_user)):
    return {"id": user.id, "name": user.name, "email": user.email}

# -------------------------------
# ROOMS & DASHBOARD
# -------------------------------

@app.get("/rooms")
def get_rooms(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    auto_cancel_expired_bookings(db)
    return db.query(Room).all()

@app.get("/room/{room_id}/bookings")
def get_room_bookings(
    room_id: int,
    date: str,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    auto_cancel_expired_bookings(db)

    start = datetime.fromisoformat(f"{date}T09:00")
    end = datetime.fromisoformat(f"{date}T18:00")

    return db.query(Booking).filter(
        Booking.room_id == room_id,
        Booking.start_time < end,
        Booking.end_time > start,
        Booking.status != "cancelled"
    ).all()

@app.get("/dashboard/stats")
def dashboard(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    auto_cancel_expired_bookings(db)
    now = now_ist_naive()

    total = db.query(Room).count()
    in_use = db.query(distinct(Booking.room_id)).filter(
        Booking.status == "in_use",
        Booking.start_time <= now,
        Booking.end_time >= now
    ).count()

    booked = db.query(distinct(Booking.room_id)).filter(
        Booking.status == "booked",
        Booking.start_time <= now,
        Booking.end_time >= now
    ).count()

    return {
        "total_rooms": total,
        "available_rooms": max(total - in_use - booked, 0),
        "rooms_in_use": in_use,
        "rooms_booked": booked
    }

# -------------------------------
# MY SCHEDULES + CHECK-IN
# -------------------------------

@app.get("/my-schedules")
def my_schedules(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    auto_cancel_expired_bookings(db)
    name = user.name.lower()

    bookings = db.query(Booking).filter(
        (Booking.host_id == user.id) |
        (Booking.participants.ilike(f"%{name}%"))
    ).all()

    return bookings

@app.post("/check-in")
def check_in(booking_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    auto_cancel_expired_bookings(db)
    now = now_ist_naive()

    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(404, "Booking not found")

    if booking.status != "booked":
        raise HTTPException(400, "Not eligible")

    if not (booking.start_time <= now <= booking.end_time):
        raise HTTPException(400, "Check-in only during meeting")

    participants = [p.strip().lower() for p in booking.participants.split(",")]
    if user.id != booking.host_id and user.name.lower() not in participants:
        raise HTTPException(403, "Not allowed")

    booking.status = "in_use"
    db.commit()
    return {"message": "Checked in"}

# -------------------------------
# CHAT (FINAL)
# -------------------------------

@app.post("/chat")
def chat(
    message: str,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    auto_cancel_expired_bookings(db)

    uid = user.id
    msg = message.lower()

    intent = infer_intent_from_text(msg)
    if intent == "unknown":
        intent = call_llm(message).get("intent", "unknown")

    if uid not in pending_bookings:
        pending_bookings[uid] = empty_booking(intent)

    booking = pending_bookings[uid]
    if booking["intent"] == "unknown":
        booking["intent"] = intent

    extracted = {
        "room_name": extract_room_name(msg),
        "participants": extract_participants_from_text(msg, db)
    }

    date, start, end = extract_date_time(msg)
    extracted["date"] = date
    if start and not booking["start_time"]:
        extracted["start_time"] = start
    if end:
        extracted["end_time"] = end

    merge_booking(booking, extracted)

    missing = [k for k in ["date", "start_time", "end_time", "participants"] if not booking[k]]
    if booking["intent"] == "book_offline_meeting" and not booking["room_name"]:
        missing.append("room name")

    if missing:
        return {"type": "ask", "message": ask_missing_fields(missing)}

    data = booking.copy()
    pending_bookings.pop(uid, None)

    meeting_type = "offline" if data["intent"] == "book_offline_meeting" else "online"
    room_id = None

    start_dt = datetime.fromisoformat(f"{data['date']}T{data['start_time']}")
    end_dt = datetime.fromisoformat(f"{data['date']}T{data['end_time']}")

    if meeting_type == "offline":
        room_id = resolve_room_id(db, data["room_name"])
        if not room_id or not is_room_available(db, room_id, start_dt, end_dt):
            return {"type": "error", "message": "Room unavailable"}

    booking_row = create_booking(
        db=db,
        host_id=user.id,
        room_id=room_id,
        date=data["date"],
        start_time=data["start_time"],
        end_time=data["end_time"],
        meeting_type=meeting_type,
        participants=data["participants"]
    )

    users = db.query(User).filter(User.name.in_(data["participants"])).all()
    emails = [u.email for u in users]

    if emails:
        room_display = (
    data["room_name"] if meeting_type == "offline" else "Online"
)

        ics = generate_ics(
            title="ConfAI Meeting",
            start_dt=start_dt,
            end_dt=end_dt,
            description=f"Host: {user.name}",
            
        )
        send_email(
            to_emails=emails,
            subject="Meeting Scheduled – ConfAI",
            body=f"""
Hello,

A meeting has been scheduled.

Meeting details:
• Type: {meeting_type.capitalize()}
• Room: {room_display}
• Date: {data['date']}
• Time: {data['start_time']} – {data['end_time']}
• Host: {user.name}

An attached calendar invitation (.ics) is included.
Please add it to your calendar.

Regards,
ConfAI
Meeting & Room Scheduling System
""",
            ics_content=ics
        )

    return {
        "type": "success",
        "message": "Meeting booked successfully",
        "booking_id": booking_row.id
    }
