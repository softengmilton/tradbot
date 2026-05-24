import React from "react";

interface Props {
  onModeSelect: (mode: "default" | "ai") => void;
  selectedMode: "default" | "ai" | null;
}

export const ModeSelector: React.FC<Props> = ({ onModeSelect, selectedMode }) => {
  return (
    <div className="mode-selector">
      <h3>Select Analysis Mode</h3>

      <button
        className={`mode-btn ${selectedMode === "default" ? "active" : ""}`}
        onClick={() => onModeSelect("default")}
      >
        <div className="mode-name">📊 Default Mode</div>
        <div className="mode-desc">Fast • Formula-Based • No API</div>
      </button>

      <button
        className={`mode-btn ${selectedMode === "ai" ? "active" : ""}`}
        onClick={() => onModeSelect("ai")}
        disabled
        title="AI Mode available in Phase 2"
      >
        <div className="mode-name">🤖 AI Mode</div>
        <div className="mode-desc">Smart • AI-Powered • Chat Enabled (Coming Soon)</div>
      </button>
    </div>
  );
};
