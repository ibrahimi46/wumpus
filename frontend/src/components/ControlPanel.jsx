import { useEffect } from "react";
import { newGame, aiMove } from "../lib/api";

function ControlPanel({ setGameState, addLog, isAiPlaying, setIsAiPlaying }) {
  const handleNewGame = async () => {
    setIsAiPlaying(false);
    const data = await newGame();
    setGameState(data);
    addLog("New Game started!");
  };

  const toggleAi = () => {
    setIsAiPlaying((prev) => !prev);
  };

  useEffect(() => {
    let timeoutId;

    const makeMove = async () => {
      if (!isAiPlaying) return;

      try {
        const data = await aiMove();
        setGameState(data);

        if (data.gameOver || data.won) {
          setIsAiPlaying(false);
          addLog(data.won ? "AI Won!" : "AI Lost!");
        } else {
          timeoutId = setTimeout(makeMove, 500);
        }
      } catch (error) {
        console.error("AI Move failed:", error);
        setIsAiPlaying(false);
        addLog("AI Error: Stopped");
      }
    };

    if (isAiPlaying) {
      addLog("AI Agent playing");
      makeMove();
    } else {
      addLog("AI stopped");
    }

    return () => clearTimeout(timeoutId);
  }, [isAiPlaying, setGameState, addLog, setIsAiPlaying]);

  return (
    <div className="space-y-5">
      <div className="grid grid-cols-2 gap-3">
        <button
          onClick={handleNewGame}
          className="px-5 py-3 bg-green-600 hover:bg-green-500 text-white font-semibold rounded shadow-lg transition"
        >
          NEW GAME
        </button>

        <button
          onClick={toggleAi}
          className={`px-5 py-3 font-semibold rounded shadow-lg transition ${
            isAiPlaying
              ? "bg-red-600 hover:bg-red-500"
              : "bg-blue-600 hover:bg-blue-500"
          } text-white`}
        >
          {isAiPlaying ? "STOP AI" : "LET AI PLAY"}
        </button>
      </div>

      <div className="text-xs text-center text-slate-500 font-mono">
        {isAiPlaying ? "AI is thinking..." : "Ready"}
      </div>
    </div>
  );
}

export default ControlPanel;
