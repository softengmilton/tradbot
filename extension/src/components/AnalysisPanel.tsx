import React from "react";

interface Props {
  onAnalyze: () => void;
  disabled?: boolean;
  loading?: boolean;
}

export const AnalysisPanel: React.FC<Props> = ({ onAnalyze, disabled, loading }) => {
  return (
    <div className="analysis-panel">
      <button
        onClick={onAnalyze}
        disabled={disabled || loading}
        className="analyze-btn"
      >
        {loading ? "Analyzing..." : "Analyze"}
      </button>
    </div>
  );
};
