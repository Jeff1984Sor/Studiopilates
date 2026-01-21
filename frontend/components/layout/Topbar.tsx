export default function Topbar() {
  return (
    <div className="flex items-center justify-between">
      <div className="rounded-full bg-white/70 px-4 py-2 text-sm">Hoje: agenda ativa</div>
      <div className="flex items-center gap-2">
        <div className="h-10 w-10 rounded-full bg-gradient-to-br from-sky-400 to-coral" />
        <div>
          <p className="text-sm font-medium">Admin</p>
          <p className="text-xs text-gray-500">studio@pilates.local</p>
        </div>
      </div>
    </div>
  );
}
