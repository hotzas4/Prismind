import AgentProfile from "@/components/agents/AgentProfile";
import { getAgent } from "@/lib/api";
import { notFound } from "next/navigation";

interface Props {
  params: { id: string };
}

export default async function AgentDetailPage({ params }: Props) {
  try {
    const agent = await getAgent(params.id);
    return <AgentProfile agent={agent} />;
  } catch {
    notFound();
  }
}
