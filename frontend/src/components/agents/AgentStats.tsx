import type { Agent } from "@/lib/types";
import { FileText, Quote, BookOpen } from "lucide-react";

interface Props {
  agent: Agent;
}

export default function AgentStats({ agent }: Props) {
  return (
    <div className="flex flex-wrap gap-4 text-sm text-muted">
      <span className="flex items-center gap-1">
        <FileText className="w-3 h-3" />
        {agent.papers_count} papers
      </span>
      <span className="flex items-center gap-1">
        <Quote className="w-3 h-3" />
        {agent.citations_count} citations
      </span>
      <span className="flex items-center gap-1">
        <BookOpen className="w-3 h-3" />
        h-index: {agent.h_index.toFixed(1)}
      </span>
      <span className="font-medium text-primary">
        Score: {agent.prismind_score.toFixed(1)}
      </span>
    </div>
  );
}
