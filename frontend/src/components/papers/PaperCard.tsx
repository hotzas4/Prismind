import Link from "next/link";
import type { Paper } from "@/lib/types";
import Badge from "@/components/ui/Badge";
import PaperStats from "@/components/papers/PaperStats";

interface Props {
  paper: Paper;
}

const NATIONALITY_FLAGS: Record<string, string> = {
  Greek: "🇬🇷",
  American: "🇺🇸",
  British: "🇬🇧",
  French: "🇫🇷",
  German: "🇩🇪",
  Japanese: "🇯🇵",
  Chinese: "🇨🇳",
  Indian: "🇮🇳",
};

function getFlag(nationality: string): string {
  return NATIONALITY_FLAGS[nationality] ?? "🌍";
}

export default function PaperCard({ paper }: Props) {
  return (
    <Link href={`/papers/${paper.id}`}>
      <div className="bg-surface border border-muted rounded-xl p-5 hover:border-primary transition-all duration-200 cursor-pointer h-full flex flex-col">
        {/* Field badge */}
        {paper.field && (
          <div className="mb-3">
            <Badge label={paper.field} />
          </div>
        )}

        {/* Title */}
        <h3 className="font-heading font-semibold text-text-main text-base mb-2 line-clamp-2">
          {paper.title}
        </h3>

        {/* Abstract preview */}
        <p className="text-muted text-sm line-clamp-3 flex-1 mb-4">
          {paper.abstract || "No abstract available."}
        </p>

        {/* Agent info */}
        {paper.agent && (
          <div className="flex items-center gap-2 mb-3 text-sm text-muted">
            <span>{getFlag(paper.agent.nationality)}</span>
            <span className="font-medium text-text-main">{paper.agent.name}</span>
          </div>
        )}

        {/* Stats */}
        <PaperStats
          reads={paper.reads_count}
          citations={paper.citations_count}
          score={paper.confidence_score}
        />
      </div>
    </Link>
  );
}
