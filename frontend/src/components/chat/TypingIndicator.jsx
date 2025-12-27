export default function TypingIndicator({ mentorName }) {
  return (
    <div className="flex items-center gap-2 text-sm text-gray-400 px-2">
      <span className="font-medium">{mentorName}</span>
      <span className="flex gap-1">
        <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" />
        <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-150" />
        <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-300" />
      </span>
    </div>
  );
}
