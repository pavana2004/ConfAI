const API_BASE = "http://127.0.0.1:8000";

export async function login(email, password) {
  const url = `${API_BASE}/login?email=${encodeURIComponent(email)}&password=${encodeURIComponent(password)}`;

  const res = await fetch(url, {
    method: "POST",
  });

  return res.json();
}
export async function getDashboardStats(token) {
  const res = await fetch(`${API_BASE}/dashboard/stats`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
  return res.json();
}
export async function getRooms(token) {
  const res = await fetch("http://127.0.0.1:8000/rooms", {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
  return res.json();
}
export async function getRoomBookings(roomId, date, token) {
  const res = await fetch(
    `http://127.0.0.1:8000/room/${roomId}/bookings?date=${date}`,
    {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }
  );
  return res.json();
}
export async function sendChatMessage(message, token) {
  const res = await fetch(
    `http://127.0.0.1:8000/chat?message=${encodeURIComponent(message)}`,
    {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }
  );
  return res.json();
}
export async function getMe(token) {
  const res = await fetch("http://127.0.0.1:8000/me", {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  if (!res.ok) {
    throw new Error("Invalid token");
  }

  return res.json();
}
export async function getMySchedules(token) {
  const res = await fetch("http://127.0.0.1:8000/my-schedules", {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
  return res.json();
}
export async function checkIn(bookingId, token) {
  const res = await fetch(
    `http://127.0.0.1:8000/check-in?booking_id=${bookingId}`,
    {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }
  );

  return res.json();
}
