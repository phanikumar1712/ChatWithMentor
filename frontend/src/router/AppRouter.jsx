import { Routes, Route } from "react-router-dom";
import Home from "../pages/Home";
import AllMentors from "../pages/AllMentors";
import ChatPage from "../pages/ChatPage";
import AboutMentors from "../pages/AboutMentors";
export default function AppRouter() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/mentors" element={<AllMentors />} />
      <Route path="/chat/:id" element={<ChatPage />} />
      <Route path="/about-mentors" element={<AboutMentors />} />
    </Routes>
  );
}
