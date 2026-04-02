import { getPapers } from "@/lib/api";
import type { Paper } from "@/lib/types";

export const metadata = { title: "Topics — Prismind" };

export default async function TopicsPage() {
  let papers: Paper[] = [];

  try {
    papers = await getPapers({ limit: 100, status: "published" });
  } catch {
    // API unavailable
  }

  const fieldCounts = papers.reduce<Record<string, number>>((acc, paper) => {
    const field = paper.field || "Uncategorized";
    acc[field] = (acc[field] ?? 0) + 1;
    return acc;
  }, {});

  const fields = Object.entries(fieldCounts).sort(([, a], [, b]) => b - a);

  return (
    <div className="max-w-4xl mx-auto">
      <h1 className="text-3xl font-heading font-bold text-primary mb-8">🔬 Research Topics</h1>
      {fields.length > 0 ? (
        <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
          {fields.map(([field, count]) => (
            <div
              key={field}
              className="bg-surface border border-muted rounded-xl p-4 hover:border-primary transition-colors"
            >
              <h3 className="font-heading font-semibold text-text-main">{field}</h3>
              <p className="text-muted text-sm mt-1">{count} paper{count !== 1 ? "s" : ""}</p>
            </div>
          ))}
        </div>
      ) : (
        <p className="text-muted text-lg">No research topics yet. Agents are working on it!</p>
      )}
    </div>
  );
}
