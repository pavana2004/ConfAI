# from datetime import timedelta
# from time_utils import now_ist_naive
# from models import Booking

# GRACE_MINUTES = 10

# def auto_cancel_expired_bookings(db):
#     now = now_ist_naive()
#     deadline = now - timedelta(minutes=GRACE_MINUTES)

#     expired = db.query(Booking).filter(
#         Booking.status == "booked",
#         Booking.start_time <= deadline
#     ).all()

#     for booking in expired:
#         booking.status = "cancelled"

#     if expired:
#         db.commit()

# auto_cancel.py








# from datetime import timedelta
# from models import Booking
# from time_utils import now_ist_naive

# def auto_cancel_expired_bookings(db):
#     now = now_ist_naive()

#     expired = db.query(Booking).filter(
#         Booking.status == "booked",
#         Booking.start_time + timedelta(minutes=10) < now
#     ).all()

#     for booking in expired:
#         booking.status = "cancelled"

#     if expired:
#         db.commit()

#     return len(expired)


from models import Booking

from datetime import timedelta
from time_utils import now_ist_naive

AUTO_CANCEL_GRACE_MINUTES = 10

def auto_cancel_expired_bookings(db):
    now = now_ist_naive()
    cancelled_count = 0

    bookings = db.query(Booking).filter(
        Booking.status == "booked"
    ).all()

    for booking in bookings:
        grace_deadline = booking.start_time + timedelta(minutes=AUTO_CANCEL_GRACE_MINUTES)

        if now >= grace_deadline:
            booking.status = "cancelled"
            cancelled_count += 1

    if cancelled_count:
        db.commit()

    return cancelled_count
