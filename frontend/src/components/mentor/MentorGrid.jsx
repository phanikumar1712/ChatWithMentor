 
import MentorCard from "./MentorCard";

export default function MentorGrid({ mentors = [] }) {
  if (mentors.length === 0) {
    return (
      <div className="col-span-full text-center py-12">
        <p className="text-gray-600 text-lg">No mentors found matching your search.</p>
        <p className="text-sm text-gray-500 mt-2">Try different keywords.</p>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
      {mentors.map((mentor) => (
        <MentorCard key={mentor.id} mentor={mentor} />
      ))}
    </div>
  );
}