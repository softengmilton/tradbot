export type AnalysisMode = "default" | "ai";

export interface ChartData {
  closes: number[];
  highs: number[];
  lows: number[];
  volumes: number[];
}

export interface AnalysisResult {
  mode: string;
  trend: string;
  confidence: number;
  entry_zone: {
    min: number;
    max: number;
  };
  stop_loss: number;
  take_profit_1: number;
  take_profit_2: number;
  support: number;
  resistance: number;
  signals: string[];
  indicators: {
    ema20: number;
    ema50: number;
    ema200: number;
    rsi: number;
    atr: number;
  };
}
