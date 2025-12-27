


import { useEffect, useRef, useState } from "react";
import ChatHeader from "./ChatHeader";
import ChatInput from "./ChatInput";
import MessageBubble from "./MessageBubble";
import TypingIndicator from "./TypingIndicator";
import api from "../../services/api";

export default function ChatWindow({
  mentorId,
  mentorName,
  mentorImage,
  backgroundImage
}) {
  const [messages, setMessages] = useState([]);
  const [typing, setTyping] = useState(false);
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, typing]);

  const sendMessage = async (text) => {
    setMessages(prev => [...prev, { from: "user", text }]);
    setTyping(true);

    try {
      const res = await api.post("/chat", {
        mentor_id: mentorId,
        user_message: text
      });

      setMessages(prev => [
        ...prev,
        { from: "mentor", text: res.data.reply }
      ]);
    } catch {
      setMessages(prev => [
        ...prev,
        { from: "mentor", text: "Something went wrong." }
      ]);
    } finally {
      setTyping(false);
    }
  };

  return (
  <div className="relative w-full h-[80vh] max-h-[700px] rounded-2xl shadow-xl overflow-hidden">

    {/* Background */}
    <div
      className="absolute inset-0 bg-cover bg-center"
      style={{ backgroundImage: `url(${backgroundImage})` }}
    />

    {/* Blur overlay */}
    <div className="absolute inset-0 backdrop-blur-md bg-black/40" />

    {/* Chat content */}
    <div className="relative z-10 flex flex-col h-full">
      <ChatHeader mentorName={mentorName} mentorImage={mentorImage} />

      {/* ONLY THIS SCROLLS */}
      <div className="flex-1 overflow-y-auto px-6 py-6 space-y-4">
        {messages.map((m, i) => (
          <MessageBubble key={i} message={m} mentorName={mentorName} />
        ))}
        {typing && <TypingIndicator mentorName={mentorName} />}
        <div ref={bottomRef} />
      </div>

      {/* Fixed input */}
      <ChatInput onSend={sendMessage} />
    </div>
  </div>
);

}




