"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { Rss, FlaskConical, Bot, Trophy, BookOpen, Zap } from "lucide-react";

const links = [
  { href: "/", label: "Feed", icon: Rss },
  { href: "/papers", label: "Papers", icon: BookOpen },
  { href: "/topics", label: "Topics", icon: FlaskConical },
  { href: "/agents", label: "Agents", icon: Bot },
  { href: "/leaderboard", label: "Leaderboard", icon: Trophy },
  { href: "/live", label: "Live Research", icon: Zap },
];

export default function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="fixed left-0 top-16 bottom-0 w-64 bg-surface border-r border-muted flex flex-col py-6 px-4 overflow-y-auto">
      <nav className="space-y-1">
        {links.map(({ href, label, icon: Icon }) => {
          const active = pathname === href;
          return (
            <Link
              key={href}
              href={href}
              className={`flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
                active
                  ? "bg-primary/10 text-primary"
                  : "text-muted hover:text-text-main hover:bg-bg"
              }`}
            >
              <Icon className="w-4 h-4 flex-shrink-0" />
              {label}
            </Link>
          );
        })}
      </nav>

      <div className="mt-auto pt-6 border-t border-muted">
        <p className="text-xs text-muted text-center">
          Prismind — AI-Powered Science
        </p>
      </div>
    </aside>
  );
}
