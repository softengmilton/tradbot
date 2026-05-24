# Trading Chart Analyzer - API Documentation

**Version**: 3.0.0  
**Last Updated**: May 24, 2026

---

## Overview

The Trading Chart Analyzer API provides two analysis modes for trading charts:

- **Default Mode**: Fast, formula-based technical analysis using indicators
- **AI Mode**: GPT-4 Vision-based analysis with follow-up chat capabilities

## Base URL

```
http://localhost:8000
```

## Authentication

The API uses OpenAI API keys for AI mode. Provide your key in the `.env` file:

```
OPENAI_API_KEY=sk_...
```

Default mode requires no authentication.

---

## API Endpoints

### 1. Health Check

**Endpoint**: `GET /api/health`

**Description**: Check API health and performance metrics

**Response**:

```json
{
  "status": "healthy",
  "version": "3.0.0",
  "metrics": {
    "total_requests": 125,
    "total_analysis_time": 45000.5,
    "average_response_time": 360.0,
    "cache_hits": 12,
    "errors": 0
  }
}
```

**Status Codes**:

- `200 OK` - API is healthy

---

### 2. Analyze Chart

**Endpoint**: `POST /api/analyze`

**Description**: Analyze a trading chart using either default or AI mode

**Request Body**:

```json
{
  "mode": "default|ai",
  "image": "base64_encoded_image_string",
  "symbol": "BTCUSD",
  "timeframe": "1h"
}
```

**Parameters**:
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| mode | string | Yes | Analysis mode: "default" or "ai" |
| image | string | Yes (for AI mode) | Base64 encoded PNG/JPG image |
| symbol | string | No | Trading pair symbol (e.g., BTCUSD) |
| timeframe | string | No | Chart timeframe (e.g., 1h, 4h) |

**DEFAULT MODE Response**:

```json
{
  "mode": "default",
  "trend": "BULLISH",
  "confidence": 75,
  "entry_zone": {
    "min": 64000,
    "max": 64500
  },
  "stop_loss": 63500,
  "take_profit_1": 65000,
  "take_profit_2": 66000,
  "support": 63000,
  "resistance": 65500,
  "signals": ["EMA20 > EMA50", "RSI > 50", "Volume increasing"],
  "indicators": {
    "ema20": 64250,
    "ema50": 64100,
    "ema200": 63800,
    "rsi": 62,
    "atr": 250
  }
}
```

**AI MODE Response**:

```json
{
  "mode": "ai",
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "analysis": {
    "market_structure": "Higher High, Higher Low pattern forming...",
    "technical_observations": {
      "indicators": "RSI showing strength above 60...",
      "patterns": "Ascending triangle breakout...",
      "volume": "Volume confirming the move..."
    },
    "entry_strategy": {
      "primary": "Enter on pullback to 64000...",
      "alternative": "Breakout above 64500...",
      "reasoning": "Multiple confluence factors..."
    },
    "stop_loss": {
      "level": 63500,
      "reasoning": "Below recent support..."
    },
    "targets": [65000, 65500, 66000],
    "scenarios": {
      "bullish": "Strong momentum continuation...",
      "bearish": "Rejection at resistance..."
    },
    "confidence": 78
  },
  "tokens_used": 456,
  "timestamp": "2024-05-24T10:30:00Z"
}
```

**Status Codes**:

- `200 OK` - Analysis successful
- `400 Bad Request` - Invalid mode or missing required fields
- `422 Unprocessable Entity` - Validation error
- `500 Internal Server Error` - Server error

**Example cURL Request** (Default Mode):

```bash
curl -X POST "http://localhost:8000/api/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "mode": "default",
    "image": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==",
    "symbol": "BTCUSD",
    "timeframe": "1h"
  }'
```

---

### 3. Get Session

**Endpoint**: `GET /api/session/{session_id}`

**Description**: Retrieve session data and chat context

**Parameters**:
| Field | Type | Description |
|-------|------|-------------|
| session_id | string | Session UUID from initial AI analysis |

**Response**:

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "created_at": "2024-05-24T10:30:00Z",
  "last_accessed": "2024-05-24T10:35:00Z",
  "image": "base64_image_data...",
  "analysis": "{...JSON analysis...}",
  "symbol": "BTCUSD",
  "messages": [
    {
      "role": "user",
      "content": "What is the entry price?",
      "timestamp": "2024-05-24T10:31:00Z"
    },
    {
      "role": "assistant",
      "content": "The primary entry is at 64000...",
      "timestamp": "2024-05-24T10:31:05Z"
    }
  ]
}
```

**Status Codes**:

- `200 OK` - Session found
- `404 Not Found` - Session not found or expired
- `500 Internal Server Error` - Server error

---

### 4. Get Session Messages

**Endpoint**: `GET /api/session/{session_id}/messages`

**Description**: Retrieve only message history from a session

**Response**:

```json
[
  {
    "role": "user",
    "content": "Why bearish?",
    "timestamp": "2024-05-24T10:31:00Z"
  },
  {
    "role": "assistant",
    "content": "Because price is below EMA200...",
    "timestamp": "2024-05-24T10:31:05Z"
  }
]
```

**Status Codes**:

- `200 OK` - Messages retrieved
- `404 Not Found` - Session not found

---

### 5. Chat

**Endpoint**: `POST /api/chat`

**Description**: Send follow-up question and get AI response

**Request Body**:

```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "message": "What support level should I watch?"
}
```

**Parameters**:
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| session_id | string | Yes | Session ID from initial analysis |
| message | string | Yes | User question/message (max 5000 chars) |

**Response**:

```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "response": "The key support level is at 63500, which is the 200-day moving average...",
  "tokens_used": 128,
  "timestamp": "2024-05-24T10:31:05Z"
}
```

**Status Codes**:

- `200 OK` - Response generated
- `400 Bad Request` - Invalid message format
- `404 Not Found` - Session not found
- `422 Unprocessable Entity` - Validation error
- `500 Internal Server Error` - AI API error

**Example Message** (What to ask):

- "Why is this a bearish setup?"
- "What would invalidate this analysis?"
- "What's your risk/reward ratio?"
- "How does volume confirm this signal?"
- "What are the key levels to watch?"

---

## Error Responses

All errors follow this format:

```json
{
  "detail": "Error message describing what went wrong"
}
```

### Common Errors

**Invalid Mode**:

```json
{
  "detail": "Invalid mode"
}
```

**Missing Image** (AI mode):

```json
{
  "detail": "Image required for AI analysis"
}
```

**Session Not Found**:

```json
{
  "detail": "Session not found"
}
```

**Invalid JSON**:

```json
{
  "detail": "Invalid request format"
}
```

---

## Rate Limiting

- Default limit: 100 requests per 60 seconds per IP
- AI analysis: Higher limits for authenticated requests
- Chat: 200 messages per session

Responses include rate limit headers:

```
RateLimit-Limit: 100
RateLimit-Remaining: 95
RateLimit-Reset: 1716551400
```

---

## Session Management

### Session Lifecycle

1. **Creation**: Session created on first AI analysis
2. **Active**: Session remains active for 60 minutes of inactivity
3. **Expired**: Sessions older than 60 minutes are cleaned up automatically
4. **Message History**: All messages in session available until expiration

### Best Practices

- Cache session_id after initial analysis
- Use session_id for all follow-up chat requests
- Session expires after 60 minutes of inactivity
- Message history is cleared with session expiration
- Create new session for new analysis

---

## Performance Characteristics

| Operation        | Avg Time | Max Time |
| ---------------- | -------- | -------- |
| Default Analysis | 50ms     | 200ms    |
| AI Analysis      | 3-5s     | 10s\*    |
| Chat Response    | 2-3s     | 8s\*     |
| Session Retrieve | 10ms     | 50ms     |

\*Depends on OpenAI API performance

---

## Image Format Requirements

**Supported Formats**: PNG, JPG, JPEG

**Specifications**:

- Minimum Resolution: 640x480
- Maximum Size: 20MB
- Aspect Ratio: Any
- Color Space: RGB or Grayscale

**Encoding**: Base64 string of raw image bytes

**Example**:

```
data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAA...
// or just
iVBORw0KGgoAAAANSUhEUgAAA...
```

---

## WebSocket Support (Future)

Real-time chat is planned for future releases using WebSocket:

```
ws://localhost:8000/api/ws/{session_id}
```

---

## API Documentation

**Interactive Docs**: `GET /api/docs`  
**OpenAPI Schema**: `GET /api/openapi.json`

Visit `http://localhost:8000/api/docs` for interactive API testing.

---

## Code Examples

### JavaScript/TypeScript

```typescript
// Default Mode Analysis
const response = await fetch("http://localhost:8000/api/analyze", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    mode: "default",
    image: base64Image,
    symbol: "BTCUSD",
  }),
});
const result = await response.json();

// AI Mode Analysis
const aiResponse = await fetch("http://localhost:8000/api/analyze", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    mode: "ai",
    image: base64Image,
    symbol: "BTCUSD",
  }),
});
const aiResult = await aiResponse.json();
const sessionId = aiResult.session_id;

// Chat
const chatResponse = await fetch("http://localhost:8000/api/chat", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    session_id: sessionId,
    message: "What is your confidence level?",
  }),
});
const chatResult = await chatResponse.json();
```

### Python

```python
import requests
import base64

BASE_URL = "http://localhost:8000"

# Default mode
response = requests.post(f"{BASE_URL}/api/analyze", json={
    "mode": "default",
    "image": image_base64,
    "symbol": "BTCUSD"
})
result = response.json()

# AI mode
ai_response = requests.post(f"{BASE_URL}/api/analyze", json={
    "mode": "ai",
    "image": image_base64,
    "symbol": "BTCUSD"
})
ai_result = ai_response.json()
session_id = ai_result["session_id"]

# Chat
chat_response = requests.post(f"{BASE_URL}/api/chat", json={
    "session_id": session_id,
    "message": "Why is this setup bullish?"
})
chat_result = chat_response.json()
```

---

## Changelog

### Version 3.0.0

- Added AI chat system with session management
- Enhanced security and CORS configuration
- Added performance monitoring
- Added input validation
- Improved error handling

### Version 2.0.0

- Added AI mode with GPT-4 Vision
- Session storage implementation
- Chat endpoint preparation

### Version 1.0.0

- Default mode formula-based analysis
- REST API endpoints
- Basic error handling

---

## Support & Issues

For API issues, check:

1. API health: GET `/api/health`
2. API docs: GET `/api/docs`
3. Backend logs: Check console output
4. OpenAI status: https://status.openai.com

---

**Last Updated**: May 24, 2026  
**Maintained by**: Trading Chart Analyzer Team
