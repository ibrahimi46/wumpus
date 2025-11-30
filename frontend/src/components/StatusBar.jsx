function StatusBar() {
  const dummy = { score: -12, alive: true, hasGold: false };

  return (
    <div className="fixed bottom-0 left-0 right-0 bg-slate-800 border-t border-slate-700 px-6 py-3">
      <div className="max-w-7xl mx-auto flex justify-between items-center text-sm">
        <div>
          <span>Score:</span> <span>{dummy.score}</span>
        </div>
        <div className={dummy.alive ? "text-green-400" : "text-red-500"}>
          Status: {dummy.alive ? "ALIVE" : "DEAD"}
        </div>
        <div>Gold: {dummy.hasGold ? "YES" : "NO"}</div>
      </div>
    </div>
  );
}

export default StatusBar;
