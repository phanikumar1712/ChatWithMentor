import { useSearchParams } from "react-router-dom";
import mentors from "../data/mentors";
import MentorGrid from "../components/mentor/MentorGrid";

export default function AllMentors() {
  const [params] = useSearchParams();
  const category = params.get("category");

  const filtered = category
    ? mentors.filter(
        m => m.category.toLowerCase().includes(category)
      )
    : mentors;

  return (
    <section className="max-w-7xl mx-auto px-6 py-10">
      <h2 className="text-3xl font-bold mb-6">
        {category ? category.toUpperCase() : "All Mentors"}
      </h2>
      <MentorGrid mentors={filtered} />
    </section>
  );
}
