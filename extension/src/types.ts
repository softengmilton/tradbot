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

export interface AIAnalysis {
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

export interface Session {
  id: string;
  image: string;
  analysis: AIAnalysis | string;
  symbol: string;
  messages: Message[];
}

export interface Message {
  role: "user" | "assistant";
  content: string;
  timestamp: string;
}
