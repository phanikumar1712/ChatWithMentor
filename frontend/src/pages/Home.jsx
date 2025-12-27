import mentors from "../data/mentors";
import MentorGrid from "../components/mentor/MentorGrid";

export default function Home() {
  return (
    <section className="max-w-7xl mx-auto px-6 py-10">
      <h1 className="text-3xl font-bold mb-6">
        Choose Your Mentor
      </h1>
      <MentorGrid mentors={mentors} />
    </section>
  );
}
