import { useState } from "react";
import { login } from "./api";

export default function Login({ onLogin }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      const res = await login(email, password);
      if (res.access_token) {
        localStorage.setItem("token", res.access_token);
        onLogin();
      } else {
        setError("Invalid credentials");
      }
    } catch {
      setError("Server error");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="w-[360px] bg-white rounded-xl shadow-xl p-8">
      <h2 className="text-2xl font-semibold text-center text-gray-800 mb-6">
        ConfAI Login
      </h2>

      <form onSubmit={handleSubmit} className="space-y-4">
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className="w-full px-4 py-2 border rounded-lg text-gray-800 focus:outline-none focus:ring-2 focus:ring-blue-500"
          required
        />

        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="w-full px-4 py-2 border rounded-lg text-gray-800 focus:outline-none focus:ring-2 focus:ring-blue-500"
          required
        />

        <button
          type="submit"
          disabled={loading}
          className="w-full py-2 rounded-lg bg-blue-600 text-white font-semibold hover:bg-blue-700 transition disabled:opacity-50"
        >
          {loading ? "Logging in..." : "Login"}
        </button>
      </form>

      {error && (
        <p className="text-red-500 text-sm text-center mt-4">
          {error}
        </p>
      )}
    </div>
  );
}
