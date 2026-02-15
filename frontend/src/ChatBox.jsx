import { useEffect, useRef, useState } from "react";
import { sendChatMessage } from "./api";

export default function ChatBox() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const token = localStorage.getItem("token");
  const inputRef = useRef(null);

  // 👂 Listen for slot clicks
  useEffect(() => {
    function handlePrefill(e) {
      setInput(e.detail);
      setTimeout(() => {
        inputRef.current?.focus();
      }, 0);
    }

    window.addEventListener("chat_prefill", handlePrefill);
    return () =>
      window.removeEventListener("chat_prefill", handlePrefill);
  }, []);

  async function sendMessage() {
    if (!input.trim() || loading) return;

    const userMsg = { role: "user", text: input };
    setMessages(prev => [...prev, userMsg]);
    setInput("");
    setLoading(true);

    try {
      const res = await sendChatMessage(userMsg.text, token);

      let botText = "";
      if (res.type === "ask") botText = res.message;
      else if (res.type === "success") botText = "✅ " + res.message;
      else if (res.type === "error") botText = "❌ " + res.message;
      else botText = JSON.stringify(res);

      setMessages(prev => [
        ...prev,
        { role: "bot", text: botText }
      ]);
    } catch {
      setMessages(prev => [
        ...prev,
        { role: "bot", text: "❌ Server error" }
      ]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="bg-gray-900 rounded-xl p-4 h-[400px] flex flex-col">
      {/* Messages */}
      <div className="flex-1 overflow-y-auto space-y-3 mb-3">
        {messages.map((m, i) => (
          <div
            key={i}
            className={`max-w-[75%] px-4 py-2 rounded-lg text-sm
              ${
                m.role === "user"
                  ? "bg-blue-600 text-white ml-auto"
                  : "bg-gray-700 text-white mr-auto"
              }`}
          >
            {m.text}
          </div>
        ))}

        {loading && (
          <div className="bg-gray-700 text-white px-4 py-2 rounded-lg text-sm w-fit">
            Assistant is typing…
          </div>
        )}
      </div>

      {/* Input */}
      <div className="flex gap-2">
        <input
          ref={inputRef}
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyDown={e => e.key === "Enter" && sendMessage()}
          placeholder="Book a meeting..."
          className="flex-1 px-3 py-2 rounded-lg bg-gray-800 text-white border border-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-600"
        />
        <button
          onClick={sendMessage}
          disabled={loading}
          className="px-4 py-2 bg-blue-600 rounded-lg hover:bg-blue-700 disabled:opacity-50"
        >
          Send
        </button>
      </div>
    </div>
  );
}
