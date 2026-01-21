import Sidebar from "./Sidebar";
import Topbar from "./Topbar";

export default function AppShell({ children }: { children: React.ReactNode }) {
  return (
    <div className="min-h-screen grid grid-cols-[240px_1fr]">
      <Sidebar />
      <main className="p-8">
        <Topbar />
        <div className="mt-6">{children}</div>
      </main>
    </div>
  );
}
