interface Props {
  score: number;
  size?: number;
  label?: string;
}

export default function ScoreRing({ score, size = 60, label = "Score" }: Props) {
  const radius = (size - 8) / 2;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - (score / 100) * circumference;

  return (
    <div className="flex flex-col items-center gap-1">
      <svg width={size} height={size} className="-rotate-90">
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          stroke="#4A4A6A"
          strokeWidth="4"
          fill="none"
        />
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          stroke="#6C63FF"
          strokeWidth="4"
          fill="none"
          strokeDasharray={circumference}
          strokeDashoffset={offset}
          strokeLinecap="round"
          className="transition-all duration-700"
        />
      </svg>
      <div className="text-center">
        <p className="text-xs font-semibold text-text-main">{score.toFixed(0)}%</p>
        <p className="text-xs text-muted">{label}</p>
      </div>
    </div>
  );
}
