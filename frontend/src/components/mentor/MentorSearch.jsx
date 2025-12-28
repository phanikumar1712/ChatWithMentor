 
import { useState, useEffect } from "react";

export default function MentorSearch({ onSearch }) {
  const [inputValue, setInputValue] = useState("");

  useEffect(() => {
    const timer = setTimeout(() => {
      onSearch(inputValue);
    }, 300);

    return () => clearTimeout(timer);
  }, [inputValue, onSearch]);

  return (
    <input
      type="text"
      className="w-full mb-6 px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500"
      placeholder="Search mentors by name, tagline, or category..."
      value={inputValue}
      onChange={(e) => setInputValue(e.target.value)}
    />
  );
}