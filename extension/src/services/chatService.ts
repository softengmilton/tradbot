const BACKEND_URL =
  process.env.REACT_APP_BACKEND_URL || "http://localhost:8000";

export interface ChatMessage {
  role: "user" | "assistant";
  content: string;
  timestamp: string;
}

export interface ChatResponse {
  session_id: string;
  response: string;
  tokens_used?: number;
  timestamp: string;
}

export const sendChatMessage = async (
  sessionId: string,
  message: string
): Promise<ChatResponse> => {
  try {
    const response = await fetch(`${BACKEND_URL}/api/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        session_id: sessionId,
        message: message,
      }),
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({}));
      throw new Error(
        error.detail || `Chat failed: ${response.statusText}`
      );
    }

    const data: ChatResponse = await response.json();
    return data;
  } catch (error) {
    throw error instanceof Error ? error : new Error("Unknown chat error");
  }
};

export const getSessionMessages = async (
  sessionId: string
): Promise<ChatMessage[]> => {
  try {
    const response = await fetch(`${BACKEND_URL}/api/session/${sessionId}`, {
      method: "GET",
      headers: { "Content-Type": "application/json" },
    });

    if (!response.ok) {
      throw new Error(`Failed to fetch session: ${response.statusText}`);
    }

    const session = await response.json();
    return session.messages || [];
  } catch (error) {
    console.error("Failed to fetch messages:", error);
    return [];
  }
};
