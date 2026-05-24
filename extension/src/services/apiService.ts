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

export interface AIAnalysisResponse {
  mode: "ai";
  session_id: string;
  analysis: AIAnalysis | string; // Can be object or JSON string from some responses
  tokens_used: number;
  timestamp: string;
}

export type APIResponse = AnalysisResponse | AIAnalysisResponse;

export const analyzeChart = async (
  request: AnalysisRequest,
): Promise<APIResponse> => {
  try {
    const response = await fetch(`${BACKEND_URL}/api/analyze`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      throw new Error(`Analysis failed: ${response.statusText}`);
    }

    const data = await response.json();
    
    // For AI responses, ensure analysis is parsed
    if (data.mode === "ai" && typeof data.analysis === "string") {
      try {
        data.analysis = JSON.parse(data.analysis);
      } catch (e) {
        console.error("Failed to parse AI analysis JSON:", e);
        throw new Error("Invalid AI response format");
      }
    }

    return data;
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

export const getSession = async (sessionId: string): Promise<any> => {
  try {
    const response = await fetch(`${BACKEND_URL}/api/session/${sessionId}`);
    if (!response.ok) {
      throw new Error("Session not found");
    }
    return response.json();
  } catch (error) {
    console.error('Session fetch error:', error);
    throw error;
  }
};

export const addSessionMessage = async (
  sessionId: string,
  role: "user" | "assistant",
  content: string
): Promise<void> => {
  try {
    const response = await fetch(`${BACKEND_URL}/api/session/${sessionId}/message`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ role, content }),
    });

    if (!response.ok) {
      throw new Error("Failed to add message");
    }
  } catch (error) {
    console.error('Add message error:', error);
    throw error;
  }
};
