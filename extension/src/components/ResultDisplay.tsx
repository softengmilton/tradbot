import React from "react";
import { AnalysisResponse } from "../services/apiService";

interface Props {
  result: AnalysisResponse | null;
  loading: boolean;
}

export const ResultDisplay: React.FC<Props> = ({ result, loading }) => {
  if (loading) {
    return <div className="loading">Analyzing chart...</div>;
  }

  if (!result) return null;

  return (
    <div className="result-panel">
      <div className="trend-section">
        <h4>TREND</h4>
        <p className="trend-value">{result.trend}</p>
      </div>

      <div className="entry-section">
        <h4>Entry Zone</h4>
        <p>{result.entry_zone.min.toFixed(2)} - {result.entry_zone.max.toFixed(2)}</p>
      </div>

      <div className="risk-section">
        <h4>Stop Loss</h4>
        <p>{result.stop_loss.toFixed(2)}</p>

        <h4>Take Profit 1</h4>
        <p>{result.take_profit_1.toFixed(2)}</p>

        <h4>Take Profit 2</h4>
        <p>{result.take_profit_2.toFixed(2)}</p>
      </div>

      <div className="confidence-section">
        <h4>Confidence: {result.confidence}%</h4>
        <div className="confidence-bar">
          <div className="fill" style={{width: `${result.confidence}%`}}></div>
        </div>
      </div>

      <div className="signals">
        <h4>Signals</h4>
        {result.signals.length > 0 ? (
          result.signals.map((sig, i) => <p key={i}>✓ {sig}</p>)
        ) : (
          <p>No signals</p>
        )}
      </div>

      <div className="indicators-section">
        <h4>Indicators</h4>
        <p>EMA 20: {result.indicators.ema20}</p>
        <p>EMA 50: {result.indicators.ema50}</p>
        <p>EMA 200: {result.indicators.ema200}</p>
        <p>RSI: {result.indicators.rsi}</p>
        <p>ATR: {result.indicators.atr}</p>
      </div>
    </div>
  );
};
