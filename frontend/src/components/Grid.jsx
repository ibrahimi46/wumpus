function Grid({ gameState, showSolution }) {
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
                ${
                  cell.visited
                    ? "bg-slate-700 border-slate-500"
                    : "bg-slate-900 border-slate-800"
                }
              `}
            >
              {cell.agentHere && (
                <span className="absolute inset-0 flex items-center justify-center text-yellow-400 text-4xl animate-pulse z-30">
                  👨🏻‍🦽‍➡️
                </span>
              )}

              {cell.visited && !(x === 0 && y === 0) && (
                <div className="absolute inset-0 flex flex-wrap items-center justify-center gap-1 z-10">
                  {cell.breeze && (
                    <span className="text-cyan-400 text-3xl">💨</span>
                  )}
                  {cell.stench && (
                    <span className="text-purple-400 text-3xl">🕳️</span>
                  )}
                  {cell.glitter && (
                    <span className="text-yellow-300 text-4xl">🏆</span>
                  )}
                </div>
              )}

              {showSolution && (
                <div className="absolute inset-0 flex items-center justify-center z-10">
                  {cell.realPit && (
                    <span className="text-red-600 text-5xl">🕳️</span>
                  )}
                  {cell.realWumpus && (
                    <span className="text-red-500 text-5xl">👹</span>
                  )}
                  {cell.realGold && (
                    <span className="text-yellow-300 text-5xl">🏆</span>
                  )}
                </div>
              )}
            </div>
          ))
        )}
      </div>
    </div>
  );
}

export default Grid;
