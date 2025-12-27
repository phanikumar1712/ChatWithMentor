import { useState } from "react";

export default function ChatInput({ onSend }) {
  const [text, setText] = useState("");

  const submit = e => {
    e.preventDefault();
    if (!text.trim()) return;
    onSend(text);
    setText("");
  };

  return (
    <form
      onSubmit={submit}
      className="flex items-center gap-4 px-4 py-3"
    >
      {/* Input Container */}
      <div
        className="
          flex-1 flex items-center gap-3
          rounded-2xl px-4 py-2
          border border-gray-600
          transition-all duration-300
          focus-within:border-indigo-500
          focus-within:shadow-[0_0_0_1px_rgba(99,102,241,0.5)]
        "
      >
        {/* Text Input */}
        <input
          value={text}
          onChange={e => setText(e.target.value)}
          placeholder="Type your message…"
          className="
            flex-1 bg-transparent
            text-white placeholder-gray-400
            focus:outline-none
          "
        />

        {/* Send Button */}
        <button
          type="submit"
          disabled={!text.trim()}
          className="
            group relative
            h-10 w-10 rounded-full
            flex items-center justify-center
            bg-indigo-600
            text-white
            transition-all duration-300
            hover:bg-indigo-500
            hover:shadow-[0_6px_20px_rgba(99,102,241,0.5)]
            active:scale-95
            disabled:opacity-40 disabled:cursor-not-allowed
          "
        >
          <span className="text-lg transition-transform duration-300 group-hover:translate-x-0.5">
            ➜
          </span>
        </button>
      </div>
    </form>
  );
}
