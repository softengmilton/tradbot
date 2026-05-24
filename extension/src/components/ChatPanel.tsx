import React, { useState, useEffect, useRef } from "react";
import { sendChatMessage, ChatMessage as ChatMessageType } from "../services/chatService";

interface Props {
  sessionId: string;
  initialMessages?: ChatMessageType[];
  onClose?: () => void;
}

export const ChatPanel: React.FC<Props> = ({
  sessionId,
  initialMessages = [],
  onClose,
}) => {
  const [messages, setMessages] = useState<ChatMessageType[]>(initialMessages);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async () => {
    if (!input.trim() || loading) return;

    const userMessage = input;
    setInput("");
    setError(null);

    // Add user message locally
    const newUserMessage: ChatMessageType = {
      role: "user",
      content: userMessage,
      timestamp: new Date().toISOString(),
    };
    setMessages((prev) => [...prev, newUserMessage]);

    setLoading(true);

    try {
      const response = await sendChatMessage(sessionId, userMessage);

      const assistantMessage: ChatMessageType = {
        role: "assistant",
        content: response.response,
        timestamp: response.timestamp,
      };
      setMessages((prev) => [...prev, assistantMessage]);
    } catch (err) {
      const errorMessage =
        err instanceof Error ? err.message : "Unable to get response";
      setError(errorMessage);
      console.error("Chat error:", err);

      // Add error message to chat
      const errorChatMessage: ChatMessageType = {
        role: "assistant",
        content: `Error: ${errorMessage}. Please try again.`,
        timestamp: new Date().toISOString(),
      };
      setMessages((prev) => [...prev, errorChatMessage]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  return (
    <div className="chat-panel">
      <div className="chat-header">
        <h3>💬 AI Analysis Chat</h3>
        <p className="session-info">Session: {sessionId.slice(0, 8)}...</p>
        {onClose && (
          <button className="close-btn" onClick={onClose} title="Close chat">
            ✕
          </button>
        )}
      </div>

      <div className="chat-history">
        {messages.length === 0 && (
          <div className="empty-state">
            <p>Ask follow-up questions about the analysis.</p>
            <p className="hint">Example: "Why is RSI showing oversold?"</p>
          </div>
        )}

        {messages.map((msg, i) => (
          <div key={i} className={`message ${msg.role}`}>
            <div className="message-bubble">
              <div className="message-content">{msg.content}</div>
            </div>
            <div className="message-time">
              {new Date(msg.timestamp).toLocaleTimeString([], {
                hour: "2-digit",
                minute: "2-digit",
              })}
            </div>
          </div>
        ))}

        {loading && (
          <div className="message assistant">
            <div className="message-bubble">
              <div className="message-content loading-dots">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          </div>
        )}

        {error && (
          <div className="error-message">
            <p>{error}</p>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      <div className="chat-input">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Ask a follow-up question..."
          disabled={loading}
          autoFocus
        />
        <button
          onClick={handleSendMessage}
          disabled={loading || !input.trim()}
          className="send-btn"
          title={loading ? "Waiting for response..." : "Send message"}
        >
          {loading ? "..." : "→"}
        </button>
      </div>
    </div>
  );
};
