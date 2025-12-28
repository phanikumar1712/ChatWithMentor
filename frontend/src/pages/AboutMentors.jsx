 
// src/pages/AboutMentors.jsx
import { useNavigate } from "react-router-dom";
import mentors from "../data/mentors";

export default function AboutMentors() {
  const navigate = useNavigate();

  const scrollLeft = () => {
    document.getElementById("mentor-carousel")?.scrollBy({ left: -350, behavior: "smooth" });
  };

  const scrollRight = () => {
    document.getElementById("mentor-carousel")?.scrollBy({ left: 350, behavior: "smooth" });
  };

  return (
    <section className="max-w-7xl mx-auto px-6 py-16">
      <div className="text-center mb-12">
        <h1 className="text-4xl font-bold text-gray-900 mb-4">
          Meet Your AI Mentors
        </h1>
        <p className="text-lg text-gray-600 max-w-3xl mx-auto">
          Wisdom from legendary figures, revived through AI. Scroll to explore and start a conversation with the mentor who inspires you.
        </p>
      </div>

      {/* Carousel Container */}
      <div className="relative group">
        {/* Left Arrow */}
        <button
          onClick={scrollLeft}
          className="absolute left-0 top-1/2 -translate-y-1/2 z-10 bg-white/80 backdrop-blur rounded-full p-3 shadow-lg hover:shadow-xl transition opacity-0 group-hover:opacity-100"
        >
          <svg className="w-6 h-6 text-gray-800" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
          </svg>
        </button>

        {/* Right Arrow */}
        <button
          onClick={scrollRight}
          className="absolute right-0 top-1/2 -translate-y-1/2 z-10 bg-white/80 backdrop-blur rounded-full p-3 shadow-lg hover:shadow-xl transition opacity-0 group-hover:opacity-100"
        >
          <svg className="w-6 h-6 text-gray-800" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
          </svg>
        </button>

        {/* Scrollable Carousel */}
        <div
          id="mentor-carousel"
          className="flex overflow-x-auto scroll-smooth gap-8 pb-8 scrollbar-hide snap-x snap-mandatory"
          style={{ scrollbarWidth: "none", msOverflowStyle: "none" }}
        >
          {mentors.map((mentor) => (
            <div
              key={mentor.id}
              className="min-w-[320px] sm:min-w-[360px] snap-center bg-white rounded-2xl shadow-lg overflow-hidden hover:shadow-2xl transition-all duration-300 cursor-pointer"
              onClick={() => navigate(`/chat/${mentor.id}`)}
            >
              {/* Hero Image */}
              <div className="h-48 overflow-hidden">
                <img
                  src={mentor.background || "https://via.placeholder.com/400x200?text=AI+Mentor"}
                  alt={mentor.name}
                  className="w-full h-full object-cover"
                />
              </div>

              {/* Content */}
              <div className="p-6">
                <h3 className="text-xl font-bold text-gray-900 mb-2">
                  {mentor.name}
                </h3>
                <p className="text-gray-600 text-sm leading-relaxed mb-4">
                  {mentor.tagline}
                  <br />
                  Guiding you with eternal wisdom and insight.
                </p>

                <div className="flex items-center justify-between text-sm">
                  <div>
                    <span className="text-gray-500">Mentor in</span>
                    <span className="ml-1 font-medium text-indigo-600">{mentor.category}</span>
                  </div>
                  {/* <span className="text-gray-400">Timeless wisdom</span> */}
                </div>

                {/* CTA Button */}
                <button className="mt-6 w-full py-2.5 bg-indigo-600 text-white font-medium rounded-lg hover:bg-indigo-700 transition">
                  Start Chat
                </button>
              </div>
            </div>
          ))}
        </div>

        {/* Dots Indicator */}
        <div className="flex justify-center gap-2 mt-6">
          {mentors.map((_, i) => (
            <div
              key={i}
              className="w-2 h-2 bg-gray-300 rounded-full transition-all duration-300 hover:bg-indigo-600"
            />
          ))}
          <div className="w-8 h-2 bg-indigo-600 rounded-full mx-1" /> {/* Active dot */}
        </div>
      </div>
    </section>
  );
}