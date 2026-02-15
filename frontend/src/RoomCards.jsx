export default function RoomCards({ rooms, onSelect }) {
  return (
    <div className="flex flex-wrap gap-4">
      {rooms.map(room => (
        <div
          key={room.id}
          onClick={() => onSelect(room)}
          className="w-44 p-4 rounded-lg bg-gray-700 hover:bg-gray-600 cursor-pointer transition"
        >
          <h3 className="font-semibold">{room.name}</h3>
          <p className="text-sm text-gray-300">
            Capacity: {room.capacity}
          </p>
        </div>
      ))}
    </div>
  );
}
