import MentorCard from "./MentorCard";

export default function MentorGrid({ mentors }) {
  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-6">
      {mentors.map(m => (
        <MentorCard key={m.id} mentor={m} />
      ))}
    </div>
  );
}
