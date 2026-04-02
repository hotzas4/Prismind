import { Eye, Quote, Star } from "lucide-react";

interface Props {
  reads: number;
  citations: number;
  score: number;
}

export default function PaperStats({ reads, citations, score }: Props) {
  return (
    <div className="flex items-center gap-4 text-sm text-muted">
      <span className="flex items-center gap-1">
        <Eye className="w-3 h-3" />
        {reads.toLocaleString()}
      </span>
      <span className="flex items-center gap-1">
        <Quote className="w-3 h-3" />
        {citations.toLocaleString()}
      </span>
      <span className="flex items-center gap-1">
        <Star className="w-3 h-3" />
        {score.toFixed(1)}
      </span>
    </div>
  );
}
