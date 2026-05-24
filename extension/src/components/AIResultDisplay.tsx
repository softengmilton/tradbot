import React, { useState } from "react";

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

interface Props {
  analysis: AIAnalysis;
  sessionId: string;
  onChatEnable?: (sessionId: string) => void;
}

export const AIResultDisplay: React.FC<Props> = ({ analysis, sessionId, onChatEnable }) => {
  const [expanded, setExpanded] = useState<string | null>(null);

  const toggleSection = (section: string) => {
    setExpanded(expanded === section ? null : section);
  };

  return (
    <div className="ai-result-panel">
      <div className="ai-header">
        <h2>🤖 AI Analysis Complete</h2>
        <p className="session-id">Session: {sessionId.slice(0, 8)}...</p>
      </div>

      <div className="market-structure">
        <h4>📈 Market Structure</h4>
        <p>{analysis.market_structure}</p>
      </div>

      <div className="technical-section">
        <h4 onClick={() => toggleSection("technical")} className="collapsible">
          🔍 Technical Observations {expanded === "technical" ? "▼" : "▶"}
        </h4>
        {expanded === "technical" && (
          <div className="content">
            <div className="observation">
              <strong>Indicators:</strong>
              <p>{analysis.technical_observations.indicators}</p>
            </div>
            <div className="observation">
              <strong>Patterns:</strong>
              <p>{analysis.technical_observations.patterns}</p>
            </div>
            <div className="observation">
              <strong>Volume:</strong>
              <p>{analysis.technical_observations.volume}</p>
            </div>
          </div>
        )}
      </div>

      <div className="entry-section">
        <h4 onClick={() => toggleSection("entry")} className="collapsible">
          🎯 Entry Strategy {expanded === "entry" ? "▼" : "▶"}
        </h4>
        {expanded === "entry" && (
          <div className="content">
            <div className="entry-option">
              <strong>Primary Entry:</strong>
              <p>{analysis.entry_strategy.primary}</p>
            </div>
            <div className="entry-option">
              <strong>Alternative:</strong>
              <p>{analysis.entry_strategy.alternative}</p>
            </div>
            <div className="entry-option">
              <strong>Reasoning:</strong>
              <p>{analysis.entry_strategy.reasoning}</p>
            </div>
          </div>
        )}
      </div>

      <div className="risk-section">
        <h4>🛑 Risk Management</h4>
        <div className="stop-loss">
          <strong>Stop Loss Level:</strong> {analysis.stop_loss.level}
          <p className="small">{analysis.stop_loss.reasoning}</p>
        </div>

        <div className="targets">
          <strong>Take Profit Targets:</strong>
          <div className="target-list">
            {analysis.targets.map((target, i) => (
              <span key={i} className="target-badge">TP{i + 1}: {target}</span>
            ))}
          </div>
        </div>
      </div>

      <div className="confidence-section">
        <h4>💪 Confidence Level: {analysis.confidence}%</h4>
        <div className="confidence-bar">
          <div
            className="confidence-fill"
            style={{
              width: `${analysis.confidence}%`,
              background: analysis.confidence > 70 ? "#10b981" : analysis.confidence > 50 ? "#f59e0b" : "#ef4444"
            }}
          />
        </div>
      </div>

      <div className="scenarios-section">
        <h4 onClick={() => toggleSection("scenarios")} className="collapsible">
          📊 Scenarios {expanded === "scenarios" ? "▼" : "▶"}
        </h4>
        {expanded === "scenarios" && (
          <div className="content">
            <div className="scenario bullish">
              <strong>📈 Bullish Case:</strong>
              <p>{analysis.scenarios.bullish}</p>
            </div>
            <div className="scenario bearish">
              <strong>📉 Bearish Case:</strong>
              <p>{analysis.scenarios.bearish}</p>
            </div>
          </div>
        )}
      </div>

      <button
        className="enable-chat-btn"
        onClick={() => onChatEnable?.(sessionId)}
        title="Start chatting about this analysis"
      >
        💬 Enable AI Chat
      </button>
    </div>
  );
};
