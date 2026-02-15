import { useEffect, useState } from "react";
import { getRoomBookings } from "./api";

const HOURS = [
  "09:00","10:00","11:00","12:00",
  "13:00","14:00","15:00","16:00","17:00"
];

function formatDate(date) {
  return date.toISOString().slice(0, 10);
}

function isPastDate(date) {
  const today = new Date();
  today.setHours(0,0,0,0);

  const d = new Date(date);
  d.setHours(0,0,0,0);

  return d < today;
}

function isPastHour(date, hour) {
  const now = new Date();
  const slotTime = new Date(date);

  const [h, m] = hour.split(":").map(Number);
  slotTime.setHours(h, m, 0, 0);

  return slotTime < now;
}

export default function RoomSlots({ room }) {
  const token = localStorage.getItem("token");

  const [selectedDate, setSelectedDate] = useState(new Date());
  const [bookings, setBookings] = useState([]);

  useEffect(() => {
    if (!room) return;

    getRoomBookings(
      room.id,
      formatDate(selectedDate),
      token
    ).then(setBookings);
  }, [room, selectedDate]);

  if (!room) {
    return (
      <div className="text-gray-400 text-center mt-20">
        Select a room to view availability
      </div>
    );
  }

  function isBooked(hour) {
    return bookings.some(b => {
      const start = b.start_time.slice(11, 16);
      const end = b.end_time.slice(11, 16);
      return hour >= start && hour < end;
    });
  }

  function handleSlotClick(hour) {
    const msg = `book ${room.name} on ${formatDate(selectedDate)} at ${hour}`;
    window.dispatchEvent(
      new CustomEvent("chat_prefill", { detail: msg })
    );
  }

  const pastDate = isPastDate(selectedDate);

  return (
    <div>
      {/* DATE NAVIGATION */}
      <div className="flex items-center justify-between mb-4">
        <button
          onClick={() =>
            setSelectedDate(d => {
              const nd = new Date(d);
              nd.setDate(nd.getDate() - 1);
              return nd;
            })
          }
          disabled={isPastDate(new Date(selectedDate.getTime() - 86400000))}
          className="px-3 py-1 rounded bg-gray-700 disabled:opacity-40"
        >
          ←
        </button>

        <div className="text-sm font-semibold">
          {selectedDate.toDateString()}
        </div>

        <button
          onClick={() =>
            setSelectedDate(d => {
              const nd = new Date(d);
              nd.setDate(nd.getDate() + 1);
              return nd;
            })
          }
          className="px-3 py-1 rounded bg-gray-700"
        >
          →
        </button>
      </div>

      {/* TIME SLOTS */}
      <div className="grid grid-cols-3 gap-4">
        {HOURS.map(hour => {
          const booked = isBooked(hour);
          const pastSlot =
            pastDate || isPastHour(selectedDate, hour);

          const disabled = booked || pastSlot;

          return (
            <div
              key={hour}
              onClick={() =>
                !disabled && handleSlotClick(hour)
              }
              className={`rounded-lg p-4 text-center font-semibold
                ${
                  booked
                    ? "bg-red-600"
                    : pastSlot
                    ? "bg-gray-600"
                    : "bg-green-600 hover:bg-green-700 cursor-pointer"
                }
                ${disabled ? "cursor-not-allowed" : ""}
              `}
            >
              <div className="text-sm">
                {hour} – {String(Number(hour.slice(0, 2)) + 1).padStart(2, "0")}:00
              </div>
              <div className="text-xs mt-1 opacity-80">
                {booked
                  ? "Booked"
                  : pastSlot
                  ? "Unavailable"
                  : "Available"}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
