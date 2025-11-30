import { useState } from "react";
import Grid from "./components/Grid";
import LogPanel from "./components/LogPanel";
import ControlPanel from "./components/ControlPanel";
import StatusBar from "./components/StatusBar";

function App() {
  const [isAiPlaying, setIsAiPlaying] = useState(false);
  const [gameState, setGameState] = useState(true);
  const [logs, setLogs] = useState([]);

  const addLog = (message) => {
    setLogs((prev) => [
      ...prev,
      [`[${new Date().toLocaleDateString()}] - ${message}`],
    ]);
  };
  return (
    <div className="min-h-screen bg-slate-900 text-white">
      <nav className="bg-slate-800 border-b border-slate-700 px-6 py-4">
        <div className="max-w-7xl mx-auto text-center">
          <h1 className="text-2xl font-bold text-green-400">WUMPUS WORLD</h1>
        </div>
      </nav>

      <div className="max-w-7xl mx-auto px-6 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
          <div className="lg:col-span-7">
            <div className="bg-slate-800 rounded-lg p-4 border border-slate-700">
              <h2 className="text-lg font-semibold mb-4 text-center text-slate-300">
                Cave Map (4x4)
              </h2>
              <div className="flex justify-center">
                <Grid gameState={gameState} />
              </div>
            </div>
          </div>

          <div className="lg:col-span-5 space-y-6">
            <div className="bg-slate-800 rounded-lg p-6 border border-slate-700">
              <h3 className="text-lg font-semibold mb-4 text-slate-300">
                Control Center
              </h3>
              <ControlPanel
                gameState={gameState}
                setGameState={setGameState}
                addLog={addLog}
                isAiPlaying={isAiPlaying}
                setIsAiPlaying={setIsAiPlaying}
              />
            </div>

            <div className="bg-slate-800 rounded-lg border border-slate-700 h-96">
              <LogPanel logs={logs} />
            </div>
          </div>
        </div>
      </div>

      {gameState && <StatusBar gameState={gameState} />}
    </div>
  );
}

export default App;
