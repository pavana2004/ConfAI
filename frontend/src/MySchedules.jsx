import { useEffect, useState } from "react";
import { getMySchedules, checkIn } from "./api";

export default function MySchedules() {
  const [schedules, setSchedules] = useState([]);
  const token = localStorage.getItem("token");

  useEffect(() => {
    refresh();
  }, []);

  async function refresh() {
    const data = await getMySchedules(token);
    setSchedules(data);
  }

  function canCheckIn(m) {
    if (m.status !== "booked") return false;

    const now = new Date();
    const start = new Date(m.start_time);
    const end = new Date(m.end_time);

    return now >= start && now <= end;
  }

  async function handleCheckIn(bookingId) {
    try {
      await checkIn(bookingId, token);
      await refresh();
    } catch {
      alert("Check-in failed");
    }
  }

  if (!schedules.length) {
    return (
      <div className="text-gray-400 text-center mt-6">
        No meetings scheduled
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {schedules.map((m) => {
        const start = new Date(m.start_time);
        const end = new Date(m.end_time);

        return (
          <div
            key={m.booking_id}
            className="bg-gray-800 rounded-lg p-4 flex justify-between items-center"
          >
            {/* LEFT */}
            <div>
              <div className="font-semibold text-white">
                {m.meeting_type === "offline"
                  ? `Room ${m.room_id}`
                  : "Online Meeting"}
              </div>

              <div className="text-sm text-gray-300">
                {start.toLocaleDateString()} ·{" "}
                {start.toLocaleTimeString([], {
                  hour: "2-digit",
                  minute: "2-digit",
                })}{" "}
                –{" "}
                {end.toLocaleTimeString([], {
                  hour: "2-digit",
                  minute: "2-digit",
                })}
              </div>

              <div className="text-xs text-gray-400 mt-1">
                Status: {m.status}
              </div>
            </div>

            {/* RIGHT */}
            <div className="flex flex-col items-end gap-2">
              {canCheckIn(m) && (
                <button
                  onClick={() => handleCheckIn(m.booking_id)}
                  className="px-3 py-1 text-sm bg-green-600 rounded hover:bg-green-700"
                >
                  Check in
                </button>
              )}

              {m.status === "booked" && (
                <span className="text-xs text-yellow-400">
                  Scheduled
                </span>
              )}

              {m.status === "in_use" && (
                <span className="text-xs text-green-400">
                  In progress
                </span>
              )}

              {m.status === "cancelled" && (
                <span className="text-xs text-red-400">
                  Cancelled
                </span>
              )}
            </div>
          </div>
        );
      })}
    </div>
  );
}
