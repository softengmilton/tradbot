# Trading Chart Analyzer

A browser extension for AI-powered and formula-based trading chart analysis with two distinct modes.

## 🚀 Features

### Phase 1: Default Mode (Formula-Based)
- Fast technical analysis without API dependencies
- EMA 20/50/200 crossover signals
- RSI (Relative Strength Index) analysis
- MACD indicator computation
- ATR (Average True Range) for volatility
- Support/Resistance detection
- Entry/exit zones with stop loss and take profit levels
- Confidence scoring system

### Phase 2: AI Mode (Vision-Based)
- OpenAI GPT-4 Vision integration
- Chart image analysis
- Detailed market structure analysis
- AI-generated trading signals
- Session-based chat history (prepared for Phase 3)
- Risk/reward scenario analysis

## 📋 Prerequisites

- Python 3.8+
- Node.js 16+ (for frontend development)
- Google Chrome/Chromium
- OpenAI API key (for AI mode only)

## 🔧 Installation & Setup

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment:
```bash
python -m venv venv
```

3. Activate virtual environment:
```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Configure environment:
```bash
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY if using AI mode
```

### Frontend Setup

1. Navigate to extension directory:
```bash
cd extension
```

2. Install dependencies:
```bash
npm install
```

3. Build the extension:
```bash
npm run build
```

## ▶️ Running the Project

### Start Backend Server

```bash
python backend/main.py
```

The API will be available at `http://localhost:8000`

### Load Extension in Chrome

1. Open Chrome and go to `chrome://extensions/`
2. Enable "Developer mode" (top right)
3. Click "Load unpacked"
4. Select the `extension/public` folder
5. The extension will appear in your Chrome toolbar

### Run Tests

**Backend indicators tests:**
```bash
python backend/test_indicators.py
```

**AI/Session store tests:**
```bash
python backend/test_ai.py
```

## 📁 Project Structure

```
tradbot/
├── backend/
│   ├── api/
│   │   ├── routes.py        # API endpoints
│   │   └── models.py        # Pydantic schemas
│   ├── analysis/
│   │   ├── indicators/      # EMA, RSI, MACD, ATR
│   │   ├── default_analyzer.py
│   │   ├── confidence.py
│   │   └── support_resistance.py
│   ├── ai/
│   │   ├── openai_client.py # OpenAI integration
│   │   └── prompts.py       # Analysis prompts
│   ├── memory/
│   │   └── session_store.py # Session management
│   │
│   ├── main.py              # FastAPI app entry
│   ├── config.py            # Configuration
│   ├── requirements.txt
│   ├── test_indicators.py
│   └── test_ai.py
│
├── extension/
│   ├── public/
│   │   ├── manifest.json    # Extension config
│   │   ├── popup.html       # Popup UI
│   │   └── background.js    # Service worker
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── services/        # API & screenshot services
│   │   ├── styles/          # CSS
│   │   ├── App.tsx
│   │   ├── index.tsx
│   │   └── types.ts
│   ├── package.json
│   └── tsconfig.json
│
└── .instruction.md          # Full project specification
```

## 🔑 API Endpoints

### Default Mode Analysis
```bash
POST /api/analyze
Content-Type: application/json

{
  "mode": "default",
  "image": "base64_encoded_image"
}
```

### AI Mode Analysis
```bash
POST /api/analyze
Content-Type: application/json

{
  "mode": "ai",
  "image": "base64_encoded_image",
  "symbol": "BTCUSD"
}
```

### Session Management
```bash
GET /api/session/{session_id}          # Get session data
GET /api/session/{session_id}/messages # Get chat history
POST /api/session/{session_id}/message # Add message
```

## 📝 Configuration

### Environment Variables

```env
# Backend
BACKEND_URL=http://localhost:8000
OPENAI_API_KEY=sk-your-key-here
ENVIRONMENT=development
LOG_LEVEL=INFO

# Frontend (in Chrome extension)
REACT_APP_BACKEND_URL=http://localhost:8000
```

## 🧪 Testing

All indicators have unit tests:

```bash
# Test all indicators
python backend/test_indicators.py

# Test AI and session management
python backend/test_ai.py
```

## 📊 Default Mode Indicators

| Indicator | Period | Usage |
|-----------|--------|-------|
| EMA       | 20, 50, 200 | Trend identification |
| RSI       | 14 | Overbought/Oversold |
| MACD      | 12, 26, 9 | Momentum |
| ATR       | 14 | Volatility & position sizing |

## 🤖 AI Mode Features

- OpenAI GPT-4 Vision for chart interpretation
- JSON-structured analysis responses
- Market structure assessment
- Technical observations
- Entry strategy recommendations
- Risk management guidance
- Bullish/bearish scenario planning
- 40-95% realistic confidence scoring

## 🔐 Security Notes

- Never commit your `.env` file with real API keys
- Keep OPENAI_API_KEY secure and private
- CORS is open in development; restrict in production
- Sessions timeout after 60 minutes of inactivity

## 🚧 Phase 3: AI Chat (Coming Soon)

- Multi-turn conversation with AI
- Follow-up questions
- Dynamic analysis refinement
- Message history persistence
- Real-time market discussion

## 📄 License

Part of the Trading Chart Analyzer project.

## 🤝 Contributing

This is a development project. See `.instruction.md` for detailed specifications.

## ⚠️ Disclaimer

This tool provides analysis assistance only. Always conduct your own research. Past performance doesn't guarantee future results. Trading involves risk of loss.
