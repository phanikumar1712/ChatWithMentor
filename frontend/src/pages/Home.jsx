// import mentors from "../data/mentors";
// import MentorGrid from "../components/mentor/MentorGrid";

// export default function Home() {
//   return (
//     <section className="max-w-7xl mx-auto px-6 py-10">
//       <h1 className="text-3xl font-bold mb-6">
//         Choose Your Mentor
//       </h1>
//       <MentorGrid mentors={mentors} />
//     </section>
//   );
// }

// import { useState } from "react";
// import mentors from "../data/mentors";
// import MentorGrid from "../components/mentor/MentorGrid";
// import MentorSearch from "../components/mentor/MentorSearch";

// export default function Home() {
//   const [searchTerm, setSearchTerm] = useState("");

//   const filteredMentors = mentors.filter((mentor) => {
//     const term = searchTerm.toLowerCase();
//     return (
//       mentor.name.toLowerCase().includes(term) ||
//       mentor.tagline.toLowerCase().includes(term) ||
//       mentor.category.toLowerCase().includes(term)
//     );
//   });

//   const handleSearch = (value) => {
//     setSearchTerm(value);
//   };

//   return (
//     <section className="max-w-7xl mx-auto px-6 py-10">
//       <h1 className="text-3xl font-bold mb-6">Choose Your Mentor</h1>

//       <MentorSearch onSearch={handleSearch} />

//       <MentorGrid mentors={filteredMentors} />
//     </section>
//   );
// }


// src/pages/Home.jsx
import { useState } from "react";
import mentors from "../data/mentors";
import MentorGrid from "../components/mentor/MentorGrid";
import MentorSearch from "../components/mentor/MentorSearch";

export default function Home() {
  const [searchTerm, setSearchTerm] = useState("");

  const filteredMentors = mentors.filter((mentor) => {
    const term = searchTerm.toLowerCase();
    return (
      mentor.name.toLowerCase().includes(term) ||
      mentor.tagline.toLowerCase().includes(term) ||
      mentor.category.toLowerCase().includes(term)
    );
  });

  const handleSearch = (value) => {
    setSearchTerm(value);
  };

  return (
    <section className="max-w-7xl mx-auto px-6 py-10">
      {/* Main Title */}
      <h1 className="text-4xl md:text-5xl font-bold text-center mb-4 text-gray-900">
        Choose Your Mentor
      </h1>

      {/* Minimal meaningful text - just above search */}
      <p className="text-center text-lg text-gray-600 mb-10 max-w-2xl mx-auto">
        Connect with mentors inspired by history’s greatest minds and gain guidance for life, decisions, and personal growth through AI conversations.
      </p>

      {/* Search Bar */}
      <MentorSearch onSearch={handleSearch} />

      {/* Mentor Grid */}
      <MentorGrid mentors={filteredMentors} />
    </section>
  );
}