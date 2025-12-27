

// import { useNavigate } from "react-router-dom";

// export default function ChatHeader({ mentorName, mentorImage }) {
//   const navigate = useNavigate();

//   return (
//     <div className="flex items-center gap-3 px-4 py-3 bg-white/90 backdrop-blur border-b">

//       {/* ← Back Button */}
//       <button
//         onClick={() => navigate("/mentors")}
//         className="text-gray-600 hover:text-gray-900 text-xl font-semibold"
//         aria-label="Back to mentors"
//       >
//         ←
//       </button>

//       {/* Mentor Avatar */}
//       <img
//         src={mentorImage}
//         alt={mentorName}
//         className="h-10 w-10 rounded-full object-cover border"
//       />

//       {/* Mentor Info */}
//       <div className="flex flex-col">
//         <span className="font-semibold text-gray-900 leading-tight">
//           {mentorName}
//         </span>
//         <span className="text-xs text-green-600">
//           Online
//         </span>
//       </div>
//     </div>
//   );
// }



import { useNavigate } from "react-router-dom";
import backIcon from "../../assets/back.png";

export default function ChatHeader({ mentorName, mentorImage }) {
  const navigate = useNavigate();

  return (
    <div className="flex items-center gap-3 px-4 py-4 bg-white/90 backdrop-blur border-b">

      {/* Back Button */}
      <button
        onClick={() => navigate("/mentors")}
        className="p-2 rounded-full hover:bg-gray-100 active:bg-gray-200 transition"
        aria-label="Back to mentors"
      >
        <img
          src={backIcon}
          alt="Back"
          className="h-5 w-5 object-contain"
        />
      </button>

      {/* Mentor Avatar */}
      <img
        src={mentorImage}
        alt={mentorName}
        className="h-10 w-10 rounded-full object-cover border"
      />

      {/* Mentor Info */}
      <div className="flex flex-col">
        <span className="font-semibold text-gray-900 leading-tight">
          {mentorName}
        </span>
        <span className="text-xs text-green-600">
          Online
        </span>
      </div>
    </div>
  );
}
