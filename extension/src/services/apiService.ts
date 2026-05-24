/**
 * API Service
 * Handles all communication with the backend API
 */

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || "http://localhost:8000";

// Request/Response Types
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

export interface HealthCheckResponse {
  status: string;
  version: string;
  uptime: string;
}

export type APIResponse = AnalysisResponse | AIAnalysisResponse;

// Custom Error Class
export class APIError extends Error {
  constructor(
    public statusCode: number,
    public details: string,
    message: string
  ) {
    super(message);
    this.name = "APIError";
  }
}

/**
 * Analyze a chart image
 */
export const analyzeChart = async (
  request: AnalysisRequest
): Promise<APIResponse> => {
  try {
    const response = await fetch(`${BACKEND_URL}/api/analyze`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new APIError(
        response.status,
        errorData.detail || errorData.message || response.statusText,
        `Analysis failed: ${response.statusText}`
      );
    }

    const data: APIResponse = await response.json();

    // For AI responses, ensure analysis is parsed
    if (data.mode === "ai" && "analysis" in data && typeof data.analysis === "string") {
      try {
        (data as AIAnalysisResponse).analysis = JSON.parse(data.analysis);
      } catch (e) {
        console.error("Failed to parse AI analysis JSON:", e instanceof Error ? e.message : String(e));
        throw new Error("Invalid AI response format");
      }
    }

    return data;
  } catch (error) {
    console.error("API error:", error);
    if (error instanceof APIError) {
      throw error;
    }
    throw new APIError(
      0,
      "Network error",
      error instanceof Error ? error.message : "Unknown API error"
    );
  }
};

/**
 * Check backend health status
 */
export const healthCheck = async (): Promise<HealthCheckResponse> => {
  try {
    const response = await fetch(`${BACKEND_URL}/api/health`);

    if (!response.ok) {
      throw new APIError(
        response.status,
        response.statusText,
        "Health check failed"
      );
    }

    const data: HealthCheckResponse = await response.json();
    return data;
  } catch (error) {
    console.error("Health check error:", error);
    throw new APIError(
      0,
      "Network error",
      error instanceof Error ? error.message : "Health check failed"
    );
  }
};

/**
 * Get API status and version
 */
export const getAPIStatus = async (): Promise<{
  isHealthy: boolean;
  version?: string;
  uptime?: string;
}> => {
  try {
    const health = await healthCheck();
    return {
      isHealthy: health.status === "healthy",
      version: health.version,
      uptime: health.uptime,
    };
  } catch {
    return { isHealthy: false };
  }
};
