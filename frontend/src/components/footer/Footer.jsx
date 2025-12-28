import { useNavigate } from "react-router-dom";

export default function Footer() {
  const navigate = useNavigate();

  return (
    <footer className="bg-gray-900 text-gray-300">
      <div className="max-w-7xl mx-auto px-6 py-10 grid gap-8 md:grid-cols-3">

        {/* Brand */}
        <div>
          <h3 className="font-semibold text-white text-lg">
            AI Mentor
          </h3>
          <p className="text-sm mt-2 leading-relaxed">
            A personal AI mentor inspired by great minds across history,
            helping users find clarity, strength, and direction through conversation.
          </p>
        </div>

        {/* Explore */}
        <div>
          <h4 className="font-semibold text-white">
            Explore Mentors
          </h4>
          <p className="text-sm mt-2">
            Spiritual Guides • Scientists • Freedom Fighters • Warrior Icons
          </p>
        </div>

        {/* Team */}
        <div className="text-sm">
          <p className="font-semibold text-white">
            Built by Tech-Avengers-Mvgr
          </p>
          <p className="mt-1">
            MVGR College of Engineering
          </p>
          <p className="mt-3 text-xs text-gray-400">
            © 2025 AI Mentor. All rights reserved.
          </p>
        </div>

      </div>
    </footer>
  );
}
