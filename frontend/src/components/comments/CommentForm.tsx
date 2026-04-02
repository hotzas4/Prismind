"use client";

import { useState } from "react";
import type { Comment } from "@/lib/types";
import { createComment } from "@/lib/api";

interface Props {
  paperId: string;
  userId?: string;
  onCommentAdded: (comment: Comment) => void;
}

export default function CommentForm({ paperId, userId, onCommentAdded }: Props) {
  const [content, setContent] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!content.trim()) return;
    setSubmitting(true);
    setError(null);
    try {
      const comment = await createComment({
        content: content.trim(),
        paper_id: paperId,
        user_id: userId ?? null,
      });
      onCommentAdded(comment);
      setContent("");
    } catch {
      setError("Failed to post comment. Please try again.");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-3">
      <textarea
        value={content}
        onChange={(e) => setContent(e.target.value)}
        placeholder="Share your thoughts on this research..."
        rows={3}
        className="w-full bg-bg border border-muted rounded-lg px-4 py-3 text-text-main placeholder:text-muted text-sm focus:outline-none focus:border-primary resize-none transition-colors"
        disabled={submitting}
      />
      {error && <p className="text-red-400 text-sm">{error}</p>}
      <button
        type="submit"
        disabled={submitting || !content.trim()}
        className="bg-primary text-white font-medium text-sm px-4 py-2 rounded-lg hover:bg-primary/80 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
      >
        {submitting ? "Posting..." : "Post Comment"}
      </button>
    </form>
  );
}
