import PaperCard from "@/components/papers/PaperCard";
import { getPapers } from "@/lib/api";
import type { Paper } from "@/lib/types";

export const metadata = { title: "Papers — Prismind" };

export default async function PapersPage() {
  let papers: Paper[] = [];

  try {
    papers = await getPapers({ limit: 50, status: "published" });
  } catch {
    // API unavailable
  }

  return (
    <div className="max-w-5xl mx-auto">
      <h1 className="text-3xl font-heading font-bold text-primary mb-8">📄 Published Papers</h1>
      {papers.length > 0 ? (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {papers.map((paper) => (
            <PaperCard key={paper.id} paper={paper} />
          ))}
        </div>
      ) : (
        <p className="text-muted text-lg">No papers published yet.</p>
      )}
    </div>
  );
}
