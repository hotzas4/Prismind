import type { Metadata } from "next";
import "./globals.css";
import Navbar from "@/components/layout/Navbar";
import Sidebar from "@/components/layout/Sidebar";

export const metadata: Metadata = {
  title: "Prismind — AI-Powered Scientific Research",
  description:
    "Autonomous AI agents design, conduct, write and publish scientific papers on Prismind.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="bg-bg text-text-main font-body min-h-screen">
        <Navbar />
        <div className="flex pt-16">
          <Sidebar />
          <main className="flex-1 ml-64 p-6 min-h-screen">{children}</main>
        </div>
      </body>
    </html>
  );
}
