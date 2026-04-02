interface Props {
  label: string;
}

const FIELD_COLORS: Record<string, string> = {
  Physics: "bg-blue-900/40 text-blue-300 border-blue-700",
  Biology: "bg-green-900/40 text-green-300 border-green-700",
  Chemistry: "bg-yellow-900/40 text-yellow-300 border-yellow-700",
  Mathematics: "bg-purple-900/40 text-purple-300 border-purple-700",
  "Computer Science": "bg-cyan-900/40 text-cyan-300 border-cyan-700",
  Psychology: "bg-pink-900/40 text-pink-300 border-pink-700",
  Economics: "bg-orange-900/40 text-orange-300 border-orange-700",
};

export default function Badge({ label }: Props) {
  const colorClass =
    FIELD_COLORS[label] ?? "bg-primary/10 text-primary border-primary/30";

  return (
    <span
      className={`inline-flex items-center px-2 py-0.5 rounded-md text-xs font-medium border ${colorClass}`}
    >
      {label}
    </span>
  );
}
