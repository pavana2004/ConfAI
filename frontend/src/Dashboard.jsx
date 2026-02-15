import { useEffect, useState } from "react";
import { getDashboardStats, getRooms } from "./api";
import RoomSlots from "./RoomSlots";
import ChatBox from "./ChatBox";
import MySchedules from "./MySchedules";

export default function Dashboard({ onLogout }) {
  const [stats, setStats] = useState(null);
  const [rooms, setRooms] = useState([]);
  const [selectedRoom, setSelectedRoom] = useState(null);
  const [view, setView] = useState("dashboard"); // dashboard | schedules

  const token = localStorage.getItem("token");

  useEffect(() => {
    if (!token) return;

    getDashboardStats(token).then(setStats);
    getRooms(token).then(setRooms);
  }, [token]);

  return (
    <div className="w-full h-full p-6 text-white">
      {/* HEADER */}
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-semibold">ConfAI Dashboard</h1>

        <div className="flex gap-3">
          <button
            onClick={() => setView("dashboard")}
            className={`px-4 py-2 rounded-lg ${
              view === "dashboard"
                ? "bg-blue-600"
                : "bg-gray-700 hover:bg-gray-600"
            }`}
          >
            Dashboard
          </button>

          <button
            onClick={() => setView("schedules")}
            className={`px-4 py-2 rounded-lg ${
              view === "schedules"
                ? "bg-blue-600"
                : "bg-gray-700 hover:bg-gray-600"
            }`}
          >
            My Schedules
          </button>

          <button
            onClick={onLogout}
            className="px-4 py-2 rounded-lg bg-red-600 hover:bg-red-700"
          >
            Logout
          </button>
        </div>
      </div>

      {/* STATS */}
      {view === "dashboard" && stats && (
        <div className="grid grid-cols-4 gap-4 mb-6">
          <StatCard label="Total Rooms" value={stats.total_rooms} />
          <StatCard label="Available" value={stats.available_rooms} />
          <StatCard label="In Use" value={stats.rooms_in_use} />
          <StatCard label="Booked" value={stats.rooms_booked} />
        </div>
      )}

      {/* MAIN CONTENT */}
      {view === "dashboard" && (
        <div className="grid grid-cols-4 gap-6 h-[70vh]">
          {/* ROOMS */}
          <div className="col-span-1 bg-gray-800 rounded-xl p-4 overflow-y-auto">
            <h2 className="text-lg font-semibold mb-4">Rooms</h2>

            <div className="space-y-2">
              {rooms.map(room => (
                <div
                  key={room.id}
                  onClick={() => setSelectedRoom(room)}
                  className={`p-3 rounded-lg cursor-pointer transition
                    ${
                      selectedRoom?.id === room.id
                        ? "bg-blue-600"
                        : "bg-gray-700 hover:bg-gray-600"
                    }`}
                >
                  <div className="font-medium">{room.name}</div>
                  <div className="text-xs opacity-80">
                    Capacity: {room.capacity}
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* SLOTS */}
          <div className="col-span-2 bg-gray-800 rounded-xl p-4 overflow-y-auto">
            <h2 className="text-lg font-semibold mb-4">Time Slots</h2>
            <RoomSlots room={selectedRoom} />
          </div>

          {/* CHAT */}
          <div className="col-span-1 bg-gray-800 rounded-xl p-4 flex flex-col">
            <h2 className="text-lg font-semibold mb-4">Assistant</h2>
            <ChatBox />
          </div>
        </div>
      )}

      {/* MY SCHEDULES VIEW */}
      {view === "schedules" && (
        <div className="bg-gray-800 rounded-xl p-6">
          <MySchedules />
        </div>
      )}
    </div>
  );
}

/* ---------------- SMALL COMPONENT ---------------- */

function StatCard({ label, value }) {
  return (
    <div className="bg-gray-800 rounded-xl p-4 text-center">
      <div className="text-sm opacity-80">{label}</div>
      <div className="text-2xl font-bold mt-1">{value}</div>
    </div>
  );
}
