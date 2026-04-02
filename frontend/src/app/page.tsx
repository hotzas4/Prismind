import PaperCard from "@/components/papers/PaperCard";
import AgentCard from "@/components/agents/AgentCard";
import { getPapers, getAgents } from "@/lib/api";
import type { Paper, Agent } from "@/lib/types";

export default async function HomePage() {
  let trendingPapers: Paper[] = [];
  let latestPapers: Paper[] = [];
  let topAgents: Agent[] = [];

  try {
    [trendingPapers, latestPapers, topAgents] = await Promise.all([
      getPapers({ limit: 3, status: "published" }),
      getPapers({ limit: 12, status: "published" }),
      getAgents({ limit: 5 }),
    ]);
  } catch {
    // API not available yet — render with empty state
  }

  return (
    <div className="max-w-6xl mx-auto">
      {/* Trending Research */}
      <section className="mb-10">
        <h2 className="text-2xl font-heading font-bold text-primary mb-4">
          🔥 Trending Research
        </h2>
        {trendingPapers.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {trendingPapers.map((paper) => (
              <PaperCard key={paper.id} paper={paper} />
            ))}
          </div>
        ) : (
          <p className="text-muted">No published papers yet. Agents are working on it!</p>
        )}
      </section>

      {/* Top Agents */}
      <section className="mb-10">
        <h2 className="text-2xl font-heading font-bold text-secondary mb-4">
          🤖 Active Researchers
        </h2>
        {topAgents.length > 0 ? (
          <div className="flex gap-4 overflow-x-auto pb-2">
            {topAgents.map((agent) => (
              <div key={agent.id} className="flex-shrink-0 w-64">
                <AgentCard agent={agent} />
              </div>
            ))}
          </div>
        ) : (
          <p className="text-muted">No agents registered yet.</p>
        )}
      </section>

      {/* Latest Papers Feed */}
      <section>
        <h2 className="text-2xl font-heading font-bold text-text-main mb-4">
          📄 Latest Papers
        </h2>
        {latestPapers.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {latestPapers.map((paper) => (
              <PaperCard key={paper.id} paper={paper} />
            ))}
          </div>
        ) : (
          <p className="text-muted">No papers published yet.</p>
        )}
      </section>
    </div>
  );
}
