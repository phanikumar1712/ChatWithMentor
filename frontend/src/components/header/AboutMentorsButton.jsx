// src/components/header/AboutMentorsButton.jsx
import { Link } from "react-router-dom";

export default function AboutMentorsButton() {
  return (
    <Link
      to="/about-mentors"
      className="px-5 py-2.5 rounded-xl bg-indigo-600 text-white text-sm font-semibold
                 hover:bg-indigo-700 active:scale-95 transition"
    >
      About Mentors
    </Link>
  );
}