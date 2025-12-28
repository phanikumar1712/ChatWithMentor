import { useNavigate } from "react-router-dom";
import backIcon from "../../assets/back.png";

export default function ChatHeader({ mentorName, mentorImage }) {
  const navigate = useNavigate();

  return (
    <div className="flex items-center gap-4 px-5 py-4 
                    bg-white/80 backdrop-blur-md 
                    border-b border-gray-200">

      {/* Back Button */}
      <button
        onClick={() => navigate("/mentors")}
        aria-label="Back to mentors"
        className="
          group
          relative
          flex items-center justify-center
          h-10 w-10
          rounded-full
          bg-gray-100/70
          hover:bg-indigo-50
          active:bg-indigo-100
          transition-all duration-200
          hover:scale-105
          active:scale-95
          cursor-pointer
        "
      >
        <img
          src={backIcon}
          alt="Back"
          className="
            h-5 w-5
            object-contain
            transition-transform duration-200
            group-hover:-translate-x-0.5
          "
        />
      </button>

      {/* Mentor Avatar */}
      <img
        src={mentorImage}
        alt={mentorName}
        className="
          h-11 w-11
          rounded-full
          object-cover
          border border-gray-300
          shadow-sm
        "
      />

      {/* Mentor Name */}
      <span className="font-semibold text-gray-900">
        {mentorName}
      </span>
    </div>
  );
}
