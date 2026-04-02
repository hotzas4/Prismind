"use client";

import { useEffect, useRef } from "react";
import * as d3 from "d3";
import type { Citation } from "@/lib/types";

interface Node {
  id: string;
  title: string;
  citations: number;
}

interface Link {
  source: string;
  target: string;
}

interface Props {
  citations: Citation[];
  paperTitles?: Record<string, string>;
  width?: number;
  height?: number;
}

export default function KnowledgeGraph({
  citations,
  paperTitles = {},
  width = 600,
  height = 400,
}: Props) {
  const svgRef = useRef<SVGSVGElement>(null);

  useEffect(() => {
    if (!svgRef.current || citations.length === 0) return;

    const nodeIds = new Set<string>();
    citations.forEach((c) => {
      nodeIds.add(c.citing_paper_id);
      nodeIds.add(c.cited_paper_id);
    });

    const nodes: Node[] = Array.from(nodeIds).map((id) => ({
      id,
      title: paperTitles[id] ?? id.slice(0, 8),
      citations: citations.filter((c) => c.cited_paper_id === id).length,
    }));

    const links: Link[] = citations.map((c) => ({
      source: c.citing_paper_id,
      target: c.cited_paper_id,
    }));

    const svg = d3.select(svgRef.current);
    svg.selectAll("*").remove();

    const simulation = d3
      .forceSimulation(nodes as d3.SimulationNodeDatum[])
      .force("link", d3.forceLink(links).id((d: d3.SimulationNodeDatum) => (d as Node).id).distance(80))
      .force("charge", d3.forceManyBody().strength(-200))
      .force("center", d3.forceCenter(width / 2, height / 2));

    const link = svg
      .append("g")
      .selectAll("line")
      .data(links)
      .join("line")
      .attr("stroke", "#4A4A6A")
      .attr("stroke-width", 1.5)
      .attr("marker-end", "url(#arrow)");

    svg
      .append("defs")
      .append("marker")
      .attr("id", "arrow")
      .attr("viewBox", "0 -5 10 10")
      .attr("refX", 15)
      .attr("markerWidth", 6)
      .attr("markerHeight", 6)
      .attr("orient", "auto")
      .append("path")
      .attr("d", "M0,-5L10,0L0,5")
      .attr("fill", "#6C63FF");

    const node = svg
      .append("g")
      .selectAll("circle")
      .data(nodes)
      .join("circle")
      .attr("r", (d) => 6 + d.citations * 2)
      .attr("fill", "#6C63FF")
      .attr("fill-opacity", 0.8)
      .attr("stroke", "#00D4FF")
      .attr("stroke-width", 1);

    const labels = svg
      .append("g")
      .selectAll("text")
      .data(nodes)
      .join("text")
      .text((d) => d.title)
      .attr("font-size", "10px")
      .attr("fill", "#E8E8F0")
      .attr("text-anchor", "middle")
      .attr("dy", -10);

    simulation.on("tick", () => {
      link
        .attr("x1", (d: d3.SimulationLinkDatum<d3.SimulationNodeDatum>) => {
          const s = d.source as d3.SimulationNodeDatum & { x: number };
          return s.x;
        })
        .attr("y1", (d: d3.SimulationLinkDatum<d3.SimulationNodeDatum>) => {
          const s = d.source as d3.SimulationNodeDatum & { y: number };
          return s.y;
        })
        .attr("x2", (d: d3.SimulationLinkDatum<d3.SimulationNodeDatum>) => {
          const t = d.target as d3.SimulationNodeDatum & { x: number };
          return t.x;
        })
        .attr("y2", (d: d3.SimulationLinkDatum<d3.SimulationNodeDatum>) => {
          const t = d.target as d3.SimulationNodeDatum & { y: number };
          return t.y;
        });

      node
        .attr("cx", (d: d3.SimulationNodeDatum) => (d as { x: number }).x)
        .attr("cy", (d: d3.SimulationNodeDatum) => (d as { y: number }).y);

      labels
        .attr("x", (d: d3.SimulationNodeDatum) => (d as { x: number }).x)
        .attr("y", (d: d3.SimulationNodeDatum) => (d as { y: number }).y);
    });

    return () => {
      simulation.stop();
    };
  }, [citations, paperTitles, width, height]);

  if (citations.length === 0) {
    return (
      <div className="flex items-center justify-center h-32 text-muted text-sm">
        No citation data to visualize
      </div>
    );
  }

  return (
    <svg
      ref={svgRef}
      width={width}
      height={height}
      className="bg-bg rounded-xl border border-muted"
    />
  );
}
