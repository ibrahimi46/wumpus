function Grid({ gameState }) {
  const size = 4;
  return (
    <div className="inline-block">
      <div
        className="grid gap-1 p-4 bg-slate-900/60 rounded-lg border border-slate-600"
        style={{ gridTemplateColumns: `repeat(${size}, minmax(0, 1fr))` }}
      >
        {gameState?.grid?.map((row, y) =>
          row.map((cell, x) => (
            <div
              key={`${x}-${y}`}
              className={`
                w-20 h-20 rounded relative flex items-center justify-center text-3xl font-bold
                border-2 transition-all duration-300
                ${cell.visited ? "bg-slate-700" : "bg-slate-800"}
                ${
                  cell.safe
                    ? "border-green-500 shadow-lg shadow-green-500/30"
                    : ""
                }
                ${
                  cell.danger
                    ? "border-red-500 shadow-lg shadow-red-500/40"
                    : ""
                }
                ${
                  !cell.visited && !cell.safe && !cell.danger
                    ? "border-slate-600"
                    : "border-slate-500"
                }
              `}
            >
              {cell.hasAgent && (
                <span className="absolute inset-0 flex items-center justify-center text-yellow-400 text-4xl animate-pulse">
                  {cell.agentDir === "right" && "→"}
                  {cell.agentDir === "down" && "↓"}
                  {cell.agentDir === "left" && "←"}
                  {cell.agentDir === "up" && "↑"}
                </span>
              )}

              <div className="absolute inset-0 flex flex-wrap items-center justify-center gap-1 text-xs">
                {cell.hasPit && (
                  <span className="text-red-600 text-5xl">🕳️</span>
                )}
                {cell.hasWumpus && (
                  <span className="text-red-500 text-5xl">👹</span>
                )}
                {cell.hasGold && (
                  <span className="text-yellow-300 text-5xl">🏆</span>
                )}
              </div>

              {cell.pit && <span className="text-red-600">☠</span>}
              {cell.wumpus && <span className="text-red-500 text-4xl">W</span>}
            </div>
          ))
        )}
      </div>
    </div>
  );
}

export default Grid;
