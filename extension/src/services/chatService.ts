/**
 * Chat Service
 * Handles multi-turn conversation with chart analysis context
 */

const BACKEND_URL =
  process.env.REACT_APP_BACKEND_URL || "http://localhost:8000";

// Chat Types
export interface ChatMessage {
  role: "user" | "assistant";
  content: string;
  timestamp: string;
}

export interface ChatRequest {
  session_id: string;
  message: string;
}

export interface ChatResponse {
  session_id: string;
  response: string;
  tokens_used?: number;
  timestamp: string;
}

// Custom Chat Error
export class ChatError extends Error {
  constructor(
    public statusCode: number,
    public details: string,
    message: string
  ) {
    super(message);
    this.name = "ChatError";
  }
}

/**
 * Send a chat message and get AI response
 */
export const sendChatMessage = async (
  sessionId: string,
  message: string
): Promise<ChatResponse> => {
  try {
    if (!sessionId || !message) {
      throw new ChatError(400, "Invalid input", "Session ID and message are required");
    }

    const request: ChatRequest = {
      session_id: sessionId,
      message: message,
    };

    const response = await fetch(`${BACKEND_URL}/api/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({}));
      throw new ChatError(
        response.status,
        error.detail || error.message || response.statusText,
        `Chat failed: ${response.statusText}`
      );
    }

    const data: ChatResponse = await response.json();
    return data;
  } catch (error) {
    console.error("Chat service error:", error);
    if (error instanceof ChatError) {
      throw error;
    }
    throw new ChatError(
      0,
      "Network error",
      error instanceof Error ? error.message : "Unknown chat error"
    );
  }
};

/**
 * Get all messages for a session
 */
export const getSessionMessages = async (
  sessionId: string
): Promise<ChatMessage[]> => {
  try {
    if (!sessionId) {
      throw new ChatError(400, "Invalid input", "Session ID is required");
    }

    const response = await fetch(`${BACKEND_URL}/api/session/${sessionId}/messages`, {
      method: "GET",
      headers: { "Content-Type": "application/json" },
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({}));
      throw new ChatError(
        response.status,
        error.detail || error.message || response.statusText,
        `Failed to fetch session messages: ${response.statusText}`
      );
    }

    const data = await response.json();
    return data.messages || [];
  } catch (error) {
    console.error("Failed to fetch messages:", error);
    if (error instanceof ChatError) {
      throw error;
    }
    return [];
  }
};

/**
 * Create a new chat session
 */
export const createSession = async (): Promise<string> => {
  try {
    const response = await fetch(`${BACKEND_URL}/api/session`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ initial_message: "Session started" }),
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({}));
      throw new ChatError(
        response.status,
        error.detail || error.message || response.statusText,
        `Failed to create session: ${response.statusText}`
      );
    }

    const data = await response.json();
    return data.session_id;
  } catch (error) {
    console.error("Failed to create session:", error);
    throw new ChatError(
      0,
      "Network error",
      error instanceof Error ? error.message : "Failed to create session"
    );
  }
};
