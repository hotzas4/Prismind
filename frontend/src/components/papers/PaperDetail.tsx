import type { Paper } from "@/lib/types";
import Badge from "@/components/ui/Badge";
import PaperStats from "@/components/papers/PaperStats";
import ReactMarkdown from "react-markdown";

interface Props {
  paper: Paper;
}

export default function PaperDetail({ paper }: Props) {
  return (
    <article className="max-w-4xl mx-auto">
      {/* Header */}
      <div className="mb-8">
        {paper.field && (
          <div className="mb-3">
            <Badge label={paper.field} />
          </div>
        )}
        <h1 className="text-3xl font-heading font-bold text-text-main mb-4">{paper.title}</h1>
        <PaperStats
          reads={paper.reads_count}
          citations={paper.citations_count}
          score={paper.confidence_score}
        />
        <div className="mt-4 flex gap-4 text-sm text-muted">
          {paper.peer_reviewed && (
            <span className="text-green-400 font-medium">✓ Peer Reviewed</span>
          )}
          <span>Confidence: {paper.confidence_score.toFixed(1)}%</span>
          <span>Reproducibility: {paper.reproducibility_score.toFixed(1)}%</span>
        </div>
      </div>

      {/* Sections */}
      <div className="space-y-8 prose prose-invert max-w-none">
        {paper.abstract && (
          <section>
            <h2 className="text-xl font-heading font-semibold text-primary">Abstract</h2>
            <ReactMarkdown>{paper.abstract}</ReactMarkdown>
          </section>
        )}
        {paper.introduction && (
          <section>
            <h2 className="text-xl font-heading font-semibold text-primary">Introduction</h2>
            <ReactMarkdown>{paper.introduction}</ReactMarkdown>
          </section>
        )}
        {paper.methodology && (
          <section>
            <h2 className="text-xl font-heading font-semibold text-primary">Methodology</h2>
            <ReactMarkdown>{paper.methodology}</ReactMarkdown>
          </section>
        )}
        {paper.results && (
          <section>
            <h2 className="text-xl font-heading font-semibold text-primary">Results</h2>
            <ReactMarkdown>{paper.results}</ReactMarkdown>
          </section>
        )}
        {paper.discussion && (
          <section>
            <h2 className="text-xl font-heading font-semibold text-primary">Discussion</h2>
            <ReactMarkdown>{paper.discussion}</ReactMarkdown>
          </section>
        )}
        {paper.conclusion && (
          <section>
            <h2 className="text-xl font-heading font-semibold text-primary">Conclusion</h2>
            <ReactMarkdown>{paper.conclusion}</ReactMarkdown>
          </section>
        )}

        {paper.references && paper.references.length > 0 && (
          <section>
            <h2 className="text-xl font-heading font-semibold text-primary">References</h2>
            <ol className="list-decimal list-inside space-y-1 text-muted text-sm">
              {paper.references.map((ref, i) => (
                <li key={i}>{ref}</li>
              ))}
            </ol>
          </section>
        )}
      </div>
    </article>
  );
}
