import React, { useState } from "react";
import { ModeSelector } from "./components/ModeSelector";
import { AnalysisPanel } from "./components/AnalysisPanel";
import { ResultDisplay } from "./components/ResultDisplay";
import { AIResultDisplay } from "./components/AIResultDisplay";
import { analyzeChart, AnalysisResponse } from "./services/apiService";
import { captureScreenshot } from "./services/screenshotService";
import "./styles/globals.css";

interface AIAnalysis {
  market_structure: string;
  technical_observations: {
    indicators: string;
    patterns: string;
    volume: string;
  };
  entry_strategy: {
    primary: string;
    alternative: string;
    reasoning: string;
  };
  stop_loss: { level: number; reasoning: string };
  targets: number[];
  scenarios: { bullish: string; bearish: string };
  confidence: number;
}

interface AIResponse {
  mode: "ai";
  session_id: string;
  analysis: AIAnalysis;
  tokens_used: number;
  timestamp: string;
}

const App: React.FC = () => {
  const [mode, setMode] = useState<"default" | "ai" | null>(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<AnalysisResponse | null>(null);
  const [aiResult, setAiResult] = useState<AIAnalysis | null>(null);
  const [sessionId, setSessionId] = useState<string | null>(null);
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

      if (mode === "default") {
        const response = await analyzeChart({
          mode: "default",
          image: screenshot
        });
        setResult(response as AnalysisResponse);
        setAiResult(null);
        setSessionId(null);
      } else if (mode === "ai") {
        const response = await analyzeChart({
          mode: "ai",
          image: screenshot
        });
        
        const aiResp = response as unknown as AIResponse;
        setAiResult(aiResp.analysis);
        setSessionId(aiResp.session_id);
        setResult(null);
      }
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : "Analysis failed";
      setError(errorMessage);
      console.error("Analysis error:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleChatEnable = (sid: string) => {
    // Placeholder for Phase 3 chat functionality
    console.log("Chat enabled for session:", sid);
    alert("AI Chat mode coming in Phase 3!");
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

      {mode === "default" && result && (
        <ResultDisplay result={result} loading={false} />
      )}

      {mode === "ai" && aiResult && sessionId && (
        <AIResultDisplay
          analysis={aiResult}
          sessionId={sessionId}
          onChatEnable={handleChatEnable}
        />
      )}
    </div>
  );
};

export default App;
