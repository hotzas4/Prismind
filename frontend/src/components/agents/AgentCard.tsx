import Link from "next/link";
import type { Agent } from "@/lib/types";
import AgentStats from "@/components/agents/AgentStats";

interface Props {
  agent: Agent;
}

export default function AgentCard({ agent }: Props) {
  return (
    <Link href={`/agents/${agent.id}`}>
      <div className="bg-surface border border-muted rounded-xl p-5 hover:border-secondary transition-all duration-200 cursor-pointer h-full flex flex-col">
        {/* Header */}
        <div className="flex items-start justify-between mb-3">
          <div>
            <h3 className="font-heading font-semibold text-text-main">{agent.name}</h3>
            <p className="text-muted text-sm">{agent.nationality}</p>
          </div>
          <span
            className={`w-2 h-2 rounded-full mt-1 flex-shrink-0 ${
              agent.is_active ? "bg-green-400" : "bg-muted"
            }`}
            title={agent.is_active ? "Active" : "Inactive"}
          />
        </div>

        {/* Specialization */}
        {agent.specialization && (
          <p className="text-secondary text-xs mb-3 font-medium">{agent.specialization}</p>
        )}

        {/* Bio preview */}
        {agent.bio && (
          <p className="text-muted text-sm line-clamp-2 flex-1 mb-4">{agent.bio}</p>
        )}

        {/* Stats */}
        <AgentStats agent={agent} />
      </div>
    </Link>
  );
}
