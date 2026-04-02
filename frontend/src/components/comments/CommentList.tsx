import type { Comment } from "@/lib/types";

interface Props {
  comments: Comment[];
}

function formatDate(dateStr: string): string {
  return new Date(dateStr).toLocaleDateString("en-US", {
    year: "numeric",
    month: "short",
    day: "numeric",
  });
}

export default function CommentList({ comments }: Props) {
  if (comments.length === 0) {
    return <p className="text-muted text-sm">No comments yet. Be the first to share your thoughts!</p>;
  }

  return (
    <div className="space-y-4">
      {comments.map((comment) => (
        <div key={comment.id} className="bg-surface border border-muted rounded-xl p-4">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs text-muted">
              {comment.user_id ? "Human Researcher" : "Anonymous"}
            </span>
            <span className="text-xs text-muted">{formatDate(comment.created_at)}</span>
          </div>
          <p className="text-text-main text-sm">{comment.content}</p>

          {/* Agent reply */}
          {comment.agent_reply && (
            <div className="mt-3 ml-4 border-l-2 border-primary pl-4">
              <p className="text-xs text-primary font-medium mb-1">
                🤖 Agent Reply · {comment.agent_replied_at ? formatDate(comment.agent_replied_at) : ""}
              </p>
              <p className="text-text-main text-sm">{comment.agent_reply}</p>
            </div>
          )}
        </div>
      ))}
    </div>
  );
}
