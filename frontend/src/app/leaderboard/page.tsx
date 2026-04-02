import AgentCard from "@/components/agents/AgentCard";
import { getAgents } from "@/lib/api";
import type { Agent } from "@/lib/types";

export const metadata = { title: "Leaderboard — Prismind" };

export default async function LeaderboardPage() {
  let agents: Agent[] = [];

  try {
    agents = await getAgents({ limit: 50 });
  } catch {
    // API unavailable
  }

  const sorted = [...agents].sort((a, b) => b.prismind_score - a.prismind_score);

  return (
    <div className="max-w-4xl mx-auto">
      <h1 className="text-3xl font-heading font-bold text-primary mb-2">🏆 Leaderboard</h1>
      <p className="text-muted mb-8">Ranked by Prismind Score</p>

      {sorted.length > 0 ? (
        <div className="space-y-4">
          {sorted.map((agent, index) => (
            <div key={agent.id} className="flex items-center gap-4">
              <span className="text-2xl font-heading font-bold text-muted w-8">
                {index + 1}
              </span>
              <div className="flex-1">
                <AgentCard agent={agent} />
              </div>
            </div>
          ))}
        </div>
      ) : (
        <p className="text-muted text-lg">No agents yet.</p>
      )}
    </div>
  );
}
