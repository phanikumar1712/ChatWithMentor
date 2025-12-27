 
import { useParams } from "react-router-dom";
import ChatWindow from "../components/chat/ChatWindow";
import mentors from "../data/mentors";

export default function ChatPage() {
  const { id } = useParams();
  const mentor = mentors.find(m => m.id === id);

  return (
       <div className="w-full flex justify-center items-center px-6 py-8">
      <div className="w-full max-w-5xl">
        <ChatWindow
          mentorId={id}
          mentorName={mentor?.name}
          mentorImage={mentor?.image}
          backgroundImage={mentor?.background}
        />
      </div>
    </div>
  );
}
