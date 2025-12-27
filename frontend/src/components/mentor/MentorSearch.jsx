export default function MentorSearch({ onSearch }) {
  return (
    <input
      className="w-full mb-6 px-4 py-3 border rounded-xl focus:ring-2 focus:ring-brand"
      placeholder="Search mentors..."
      onChange={e => onSearch(e.target.value)}
    />
  );
}
