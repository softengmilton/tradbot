const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || "http://localhost:8000";

export interface AnalysisRequest {
  mode: "default" | "ai";
  image?: string; // base64
  symbol?: string;
  timeframe?: string;
}

export interface EntryZone {
  min: number;
  max: number;
}

export interface Indicators {
  ema20: number;
  ema50: number;
  ema200: number;
  rsi: number;
  atr: number;
}

export interface AnalysisResponse {
  mode: string;
  trend: string;
  confidence: number;
  entry_zone: EntryZone;
  stop_loss: number;
  take_profit_1: number;
  take_profit_2: number;
  support: number;
  resistance: number;
  signals: string[];
  indicators: Indicators;
}

export const analyzeChart = async (
  request: AnalysisRequest,
): Promise<AnalysisResponse> => {
  try {
    const response = await fetch(`${BACKEND_URL}/api/analyze`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      throw new Error(`Analysis failed: ${response.statusText}`);
    }

    return response.json();
  } catch (error) {
    console.error('API error:', error);
    throw error;
  }
};

export const healthCheck = async (): Promise<boolean> => {
  try {
    const response = await fetch(`${BACKEND_URL}/api/health`);
    return response.ok;
  } catch (error) {
    console.error('Health check failed:', error);
    return false;
  }
};
