import PaperDetail from "@/components/papers/PaperDetail";
import { getPaper } from "@/lib/api";
import { notFound } from "next/navigation";

interface Props {
  params: Promise<{ id: string }>;
}

export default async function PaperDetailPage({ params }: Props) {
  const { id } = await params;
  try {
    const paper = await getPaper(id);
    return <PaperDetail paper={paper} />;
  } catch {
    notFound();
  }
}
