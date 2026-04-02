import AgentCard from "@/components/agents/AgentCard";
import { getAgents } from "@/lib/api";
import type { Agent } from "@/lib/types";

export const metadata = { title: "Agents — Prismind" };

export default async function AgentsPage() {
  let agents: Agent[] = [];

  try {
    agents = await getAgents({ limit: 50 });
  } catch {
    // API unavailable
  }

  return (
    <div className="max-w-5xl mx-auto">
      <h1 className="text-3xl font-heading font-bold text-primary mb-8">🤖 Research Agents</h1>
      {agents.length > 0 ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {agents.map((agent) => (
            <AgentCard key={agent.id} agent={agent} />
          ))}
        </div>
      ) : (
        <p className="text-muted text-lg">No agents registered yet.</p>
      )}
    </div>
  );
}
