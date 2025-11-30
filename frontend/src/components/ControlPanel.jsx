function ControlPanel({ addLog, isAiPlaying, setIsAiPlaying }) {
  return (
    <div className="space-y-5">
      <div className="grid grid-cols-2 gap-3">
        <button className="px-5 py-3 bg-green-600 hover:bg-green-500 text-white font-semibold rounded shadow-lg transition">
          NEW GAME
        </button>

        <button
          onClick={() => {
            setIsAiPlaying(!isAiPlaying);
            addLog(isAiPlaying ? "AI stopped" : "AI agent started!");
          }}
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
