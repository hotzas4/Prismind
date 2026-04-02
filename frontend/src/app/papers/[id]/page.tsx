import PaperDetail from "@/components/papers/PaperDetail";
import { getPaper } from "@/lib/api";
import { notFound } from "next/navigation";

interface Props {
  params: { id: string };
}

export default async function PaperDetailPage({ params }: Props) {
  try {
    const paper = await getPaper(params.id);
    return <PaperDetail paper={paper} />;
  } catch {
    notFound();
  }
}
