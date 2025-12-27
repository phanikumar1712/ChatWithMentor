    import { useNavigate } from "react-router-dom";


export default function Footer() {

  return (
    <footer className="bg-gray-900 text-gray-300">
      <div className="max-w-7xl mx-auto px-6 py-10 grid md:grid-cols-3 gap-6">
        <div>
          <h3 className="font-semibold text-white">AI Mentor</h3>
          <p className="text-sm mt-2">
            Guidance inspired by wisdom across time.
          </p>
        </div>
        <div>
          <h4 className="font-semibold text-white">Explore</h4>
          <p className="text-sm mt-2">Spiritual • Science • Leadership</p>
        </div>
        <div className="text-sm">
          © 2025 AI Mentor
        </div>
      </div>
    </footer>
  );
}
