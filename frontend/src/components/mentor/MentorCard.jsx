import { useNavigate } from "react-router-dom";

export default function MentorCard({ mentor }) {
  const navigate = useNavigate();

  return (
    <div
      onClick={() => navigate(`/chat/${mentor.id}`)}
      className="cursor-pointer bg-white rounded-xl shadow hover:shadow-xl
                 hover:-translate-y-1 transition-all p-4"
    >
      <img
        src={mentor.image}
        alt={mentor.name}
        className="h-40 w-full object-cover rounded-lg"
      />
      <h3 className="mt-3 text-lg font-semibold">{mentor.name}</h3>
      <p className="text-sm text-gray-500">{mentor.tagline}</p>
      <span className="inline-block mt-2 text-xs bg-indigo-100
                       text-indigo-700 px-3 py-1 rounded-full">
        {mentor.category}
      </span>
    </div>
  );
}
