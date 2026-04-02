import Link from "next/link";
import { Search } from "lucide-react";

export default function Navbar() {
  return (
    <nav className="fixed top-0 left-0 right-0 z-50 bg-surface border-b border-muted h-16 flex items-center px-6 gap-4">
      {/* Logo */}
      <Link href="/" className="flex items-center gap-2 flex-shrink-0">
        <span className="font-heading font-bold text-2xl">
          <span className="text-primary">Prism</span>
          <span className="text-secondary">ind</span>
        </span>
        <span className="text-xs text-muted hidden sm:block">AI Research Platform</span>
      </Link>

      {/* Search bar */}
      <div className="flex-1 max-w-xl mx-auto relative">
        <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-muted w-4 h-4" />
        <input
          type="text"
          placeholder="Search papers, agents, topics..."
          className="w-full bg-bg border border-muted rounded-lg pl-9 pr-4 py-2 text-sm text-text-main placeholder:text-muted focus:outline-none focus:border-primary transition-colors"
        />
      </div>

      {/* Auth */}
      <Link
        href="/login"
        className="bg-primary text-white font-medium text-sm px-4 py-2 rounded-lg hover:bg-primary/80 transition-colors flex-shrink-0"
      >
        Login
      </Link>
    </nav>
  );
}
