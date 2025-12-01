function StatusBar({ gameState }) {
  return (
    <div className="fixed bottom-0 left-0 right-0 bg-slate-800 border-t border-slate-700 px-6 py-3">
      <div className="max-w-7xl mx-auto flex justify-between items-center text-sm">
        <div>
          <span>Score:</span> <span>{gameState.score}</span>
        </div>
        <div className={gameState.alive ? "text-green-400" : "text-red-500"}>
          Status: {gameState.alive ? "ALIVE" : "DEAD"}
        </div>
        <div>Gold: {gameState.hasGold ? "YES" : "NO"}</div>
      </div>
    </div>
  );
}

export default StatusBar;
