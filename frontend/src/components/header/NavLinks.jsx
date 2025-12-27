import { Link, useLocation } from "react-router-dom";

export default function NavLinks() {
  const { pathname } = useLocation();

  const linkClass = path =>
    `text-sm font-medium transition ${
      pathname === path
        ? "text-indigo-600"
        : "text-gray-700 hover:text-indigo-600"
    }`;

  return (
    <nav className="flex gap-6">
      <Link to="/" className={linkClass("/")}>
        Home
      </Link>
      <Link to="/mentors" className={linkClass("/mentors")}>
        All Mentors
      </Link>
    </nav>
  );
}
