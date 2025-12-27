 

export default function MessageBubble({ message, mentorName }) {
  const isUser = message.from === "user";

  return (
    <div className={`flex ${isUser ? "justify-end" : "justify-start"}`}>
      <div
        className={`max-w-[75%] px-4 py-3 rounded-2xl shadow-sm text-sm leading-relaxed ${
          isUser
            ? "bg-indigo-600 text-white rounded-br-none"
            : "bg-white text-gray-800 border rounded-bl-none"
        }`}
      >
        <div className="text-xs font-semibold mb-1 opacity-80">
          {isUser ? "You" : mentorName}
        </div>
        {message.text}
      </div>
    </div>
  );
}
