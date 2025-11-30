function LogPanel({ logs }) {
  return (
    <div className="h-full flex flex-col">
      <div className="px-5 py-3 border-b border-slate-600">
        <h3 className="text-green-400 font-mono text-sm">AGENT LOG</h3>
      </div>
      <div className="flex-1 overflow-y-auto p-4 font-mono text-xs space-y-1">
        {logs.length === 0 ? (
          <p className="text-slate-500">No activity yet...</p>
        ) : (
          logs.map((log, i) => (
            <div key={i} className="text-slate-300">
              <span className="text-cyan-400">→</span> {log}
            </div>
          ))
        )}
      </div>
    </div>
  );
}

export default LogPanel;
