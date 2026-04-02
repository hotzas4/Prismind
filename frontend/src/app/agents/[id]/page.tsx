import AgentProfile from "@/components/agents/AgentProfile";
import { getAgent } from "@/lib/api";
import { notFound } from "next/navigation";

interface Props {
  params: Promise<{ id: string }>;
}

export default async function AgentDetailPage({ params }: Props) {
  const { id } = await params;
  try {
    const agent = await getAgent(id);
    return <AgentProfile agent={agent} />;
  } catch {
    notFound();
  }
}
