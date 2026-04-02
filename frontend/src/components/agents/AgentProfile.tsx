import type { Agent } from "@/lib/types";
import AgentStats from "@/components/agents/AgentStats";
import Badge from "@/components/ui/Badge";

interface Props {
  agent: Agent;
}

export default function AgentProfile({ agent }: Props) {
  return (
    <div className="max-w-3xl mx-auto">
      {/* Header */}
      <div className="bg-surface border border-muted rounded-2xl p-8 mb-6">
        <div className="flex items-start gap-6">
          <div className="w-16 h-16 rounded-full bg-primary/20 flex items-center justify-center text-2xl font-heading font-bold text-primary flex-shrink-0">
            {agent.name.charAt(0)}
          </div>
          <div className="flex-1">
            <h1 className="text-3xl font-heading font-bold text-text-main mb-1">{agent.name}</h1>
            <p className="text-muted mb-2">{agent.nationality}</p>
            {agent.specialization && (
              <p className="text-secondary font-medium mb-4">{agent.specialization}</p>
            )}
            {agent.bio && <p className="text-text-main">{agent.bio}</p>}
          </div>
        </div>

        <div className="mt-6">
          <AgentStats agent={agent} />
        </div>
      </div>

      {/* Research Interests */}
      {agent.research_interests && agent.research_interests.length > 0 && (
        <div className="bg-surface border border-muted rounded-xl p-6 mb-6">
          <h2 className="font-heading font-semibold text-text-main mb-3">Research Interests</h2>
          <div className="flex flex-wrap gap-2">
            {agent.research_interests.map((interest) => (
              <Badge key={interest} label={interest} />
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
