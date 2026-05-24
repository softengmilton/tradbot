import React, { useState } from "react";
import { ModeSelector } from "./components/ModeSelector";
import { AnalysisPanel } from "./components/AnalysisPanel";
import { ResultDisplay } from "./components/ResultDisplay";
import { analyzeChart, AnalysisResponse } from "./services/apiService";
import { captureScreenshot } from "./services/screenshotService";
import "./styles/globals.css";

const App: React.FC = () => {
  const [mode, setMode] = useState<"default" | "ai" | null>(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<AnalysisResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleAnalyze = async () => {
    if (!mode) {
      setError("Please select a mode first");
      return;
    }

    try {
      setLoading(true);
      setError(null);

      const screenshot = await captureScreenshot();

      const response = await analyzeChart({
        mode,
        image: screenshot
      });

      setResult(response);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : "Analysis failed";
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <h1>📊 Trading Chart Analyzer</h1>

      <ModeSelector onModeSelect={setMode} selectedMode={mode} />

      <AnalysisPanel
        onAnalyze={handleAnalyze}
        disabled={!mode || loading}
        loading={loading}
      />

      {error && <div className="error">{error}</div>}
      {result && <ResultDisplay result={result} loading={loading} />}
    </div>
  );
};

export default App;
