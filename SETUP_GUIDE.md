# Trading Chart Analyzer - Setup Guide

**Version**: 3.0.0  
**Last Updated**: May 24, 2026

---

## Table of Contents

1. [System Requirements](#system-requirements)
2. [Quick Start](#quick-start)
3. [Backend Setup](#backend-setup)
4. [Frontend Setup](#frontend-setup)
5. [Configuration](#configuration)
6. [Running Tests](#running-tests)
7. [Development](#development)
8. [Troubleshooting](#troubleshooting)

---

## System Requirements

### Minimum Requirements
- **Python**: 3.8+
- **Node.js**: 16+ LTS
- **npm**: 8+
- **Memory**: 2GB RAM
- **Disk**: 500MB free space

### Recommended Requirements
- **Python**: 3.10+
- **Node.js**: 18+ LTS
- **Memory**: 4GB RAM
- **Browser**: Chrome/Chromium 90+

### Supported Platforms
- ✅ Windows 10/11
- ✅ macOS 10.15+
- ✅ Linux (Ubuntu 20.04+)

---

## Quick Start

### 1. Clone Repository

```bash
git clone https://github.com/softengmilton/tradbot.git
cd tradbot
```

### 2. Backend Quick Start

```bash
cd backend

# Windows
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python main.py

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

Server runs at: `http://localhost:8000`

### 3. Frontend Quick Start

```bash
cd extension

npm install
npm run dev

# Or build for production
npm run build
```

### 4. Load Extension in Chrome

1. Open Chrome → `chrome://extensions/`
2. Enable "Developer mode" (top right)
3. Click "Load unpacked"
4. Select `extension/public` folder
5. Extension now in Chrome toolbar

---

## Backend Setup

### Prerequisites Installation

#### Windows

```bash
# Install Python from https://www.python.org/downloads/
# Verify installation
python --version

# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

#### macOS

```bash
# Install Python via Homebrew
brew install python@3.10

# Create virtual environment
python3 -m venv venv

# Activate
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### Linux (Ubuntu/Debian)

```bash
# Update package manager
sudo apt update
sudo apt install python3 python3-venv python3-pip

# Create virtual environment
python3 -m venv venv

# Activate
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Backend Directory Structure

```
backend/
├── main.py                 # FastAPI app entry point
├── config.py              # Environment configuration
├── requirements.txt       # Python dependencies
├── .env.example          # Example environment file
├── security.py           # Security utilities
├── api/
│   ├── routes.py         # API endpoints
│   ├── models.py         # Pydantic models
│   └── __init__.py
├── analysis/
│   ├── default_analyzer.py
│   ├── confidence.py
│   ├── support_resistance.py
│   └── indicators/
│       ├── ema.py
│       ├── rsi.py
│       ├── macd.py
│       └── atr.py
├── ai/
│   ├── openai_client.py
│   ├── prompts.py
│   └── __init__.py
├── memory/
│   ├── session_store.py
│   └── __init__.py
├── test_indicators.py     # Unit tests
├── test_ai.py            # AI tests
└── test_integration.py   # Integration tests
```

### Environment Configuration

Create `backend/.env` file:

```env
# FastAPI Configuration
LOG_LEVEL=INFO
DEBUG=False

# OpenAI Configuration (required for AI mode)
OPENAI_API_KEY=sk_your_api_key_here

# Optional
API_PORT=8000
API_HOST=0.0.0.0
```

Get your OpenAI API key from: https://platform.openai.com/api-keys

### Start Backend Server

```bash
# Development mode (with auto-reload)
python main.py

# Production mode (with uvicorn)
pip install uvicorn
uvicorn main:app --host 0.0.0.0 --port 8000

# With custom settings
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4 --log-level info
```

**Server will run at**: `http://localhost:8000`  
**API Docs at**: `http://localhost:8000/api/docs`  
**Health Check**: `http://localhost:8000/api/health`

---

## Frontend Setup

### Prerequisites Installation

#### Windows/macOS/Linux

```bash
# Download Node.js from https://nodejs.org/
# or use package manager
# Windows: choco install nodejs
# macOS: brew install node
# Linux: sudo apt install nodejs npm

# Verify installation
node --version
npm --version
```

### Frontend Directory Structure

```
extension/
├── public/
│   ├── manifest.json     # Extension manifest
│   ├── popup.html        # Popup UI
│   ├── background.js     # Service worker
│   └── icons/
│       ├── icon-16.png
│       ├── icon-48.png
│       └── icon-128.png
├── src/
│   ├── App.tsx           # Main app component
│   ├── index.tsx         # Entry point
│   ├── types.ts          # TypeScript types
│   ├── components/
│   │   ├── ChatPanel.tsx
│   │   ├── AIResultDisplay.tsx
│   │   ├── ModeSelector.tsx
│   │   ├── ResultDisplay.tsx
│   │   └── AnalysisPanel.tsx
│   ├── services/
│   │   ├── apiService.ts
│   │   ├── chatService.ts
│   │   ├── screenshotService.ts
│   │   └── storageService.ts
│   └── styles/
│       ├── globals.css
│       └── chat.css
├── package.json          # Dependencies
├── tsconfig.json         # TypeScript config
└── webpack.config.js     # Build config
```

### Install Dependencies

```bash
cd extension

# Install npm packages
npm install

# Verify installation
npm list
```

### Build Frontend

```bash
# Development build (with source maps)
npm run dev

# Production build (minified)
npm run build

# Watch mode (auto-rebuild on changes)
npm run watch
```

### Load in Chrome

1. **Enable Developer Mode**:
   - Open Chrome
   - Go to `chrome://extensions/`
   - Toggle "Developer mode" (top right)

2. **Load Unpacked**:
   - Click "Load unpacked"
   - Select `extension/public` folder
   - Extension appears in toolbar

3. **Verify**:
   - Click extension icon
   - UI should appear
   - Check backend connection

---

## Configuration

### Backend Configuration (`.env`)

```env
# Logging
LOG_LEVEL=INFO              # DEBUG, INFO, WARNING, ERROR, CRITICAL
DEBUG=False                 # Enable debug mode

# OpenAI
OPENAI_API_KEY=sk_...      # Required for AI mode
OPENAI_MODEL=gpt-4-vision-preview  # Vision model
OPENAI_CHAT_MODEL=gpt-4    # Chat model

# Cache
CACHE_MAX_SIZE=100         # Max cached analyses
CACHE_TTL_SECONDS=3600     # Cache lifetime

# Rate Limiting
RATE_LIMIT_REQUESTS=100    # Max requests
RATE_LIMIT_WINDOW=60       # Time window (seconds)

# Security
ALLOWED_ORIGINS=http://localhost:3000,chrome-extension://*
CORS_MAX_AGE=600

# API
API_PORT=8000
API_HOST=0.0.0.0
```

### Frontend Configuration

In `extension/src/config.ts` (if exists):

```typescript
export const config = {
  BACKEND_URL: process.env.REACT_APP_BACKEND_URL || 'http://localhost:8000',
  API_TIMEOUT: 30000,  // 30 seconds
  CACHE_ANALYSIS: true,
  LOG_LEVEL: 'info'
};
```

---

## Running Tests

### Backend Tests

```bash
cd backend

# Run all tests
python test_ai.py
python test_indicators.py
python test_integration.py

# Run with unittest
python -m unittest test_ai.py

# Run with pytest (if installed)
pip install pytest
pytest test_*.py -v

# Run specific test
python -m unittest test_ai.TestSessionStore.test_session_store_create
```

### Frontend Tests

```bash
cd extension

# Install test dependencies
npm install --save-dev jest @testing-library/react

# Run tests
npm test

# Run with coverage
npm test -- --coverage

# Run specific test
npm test -- ChatPanel.test.tsx
```

### Integration Tests

```bash
cd backend

# Install test dependencies
pip install pytest pytest-asyncio

# Run integration tests
pytest test_integration.py -v

# Run specific test class
pytest test_integration.py::TestAnalysisEndpoint -v
```

---

## Development

### Hot Reload

**Backend (FastAPI)**:
- Auto-reload enabled by default with `python main.py`
- Edit `.py` files, server restarts automatically

**Frontend (React)**:
- Hot reload enabled with `npm run dev`
- Edit `.tsx` files, browser updates automatically

### Debugging

**Backend Debug Mode**:

```python
# In main.py or any module
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.debug("Debug message")
```

**Frontend Debug Mode**:

```typescript
// In Chrome DevTools
console.log('Debug message');

// Or enable React DevTools extension
// https://chrome.google.com/webstore/detail/react-developer-tools
```

### Code Style

**Python** (PEP 8):
```bash
pip install black flake8
black backend/
flake8 backend/
```

**TypeScript** (ESLint):
```bash
cd extension
npm install --save-dev eslint
npx eslint src/
```

---

## Troubleshooting

### Backend Issues

**Port Already in Use**:
```bash
# Change port
uvicorn main:app --port 8001

# Or kill process using port 8000
# Windows: netstat -ano | findstr :8000
# Linux/macOS: lsof -i :8000
```

**Module Not Found**:
```bash
# Ensure virtual environment activated
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

**OpenAI API Error**:
```
- Check OPENAI_API_KEY in .env
- Verify API key is valid: https://platform.openai.com/api-keys
- Check API account has credits
- Ensure internet connection
```

**CORS Error**:
```
- Check backend CORS configuration in main.py
- Verify extension origin matches ALLOWED_ORIGINS
- Check backend is running
```

### Frontend Issues

**Extension Not Loading**:
1. Clear cache: `chrome://extensions/` → Clear cache
2. Reload extension: F5 or refresh button
3. Rebuild: `npm run build`
4. Re-load in Chrome

**Connection Error**:
1. Verify backend running: `http://localhost:8000/api/health`
2. Check BACKEND_URL in code
3. Check CORS settings
4. Check browser console for errors

**Build Errors**:
```bash
# Clear node_modules and rebuild
rm -rf node_modules
npm install
npm run build
```

### Common Issues

| Issue | Solution |
|-------|----------|
| "Module 'openai' not found" | `pip install openai==1.3.0` |
| "Cannot find module 'react'" | `cd extension && npm install` |
| "Port 8000 already in use" | Use different port:  `--port 8001` |
| "TypeScript errors" | `npm install -g typescript` |
| "Chrome extension won't load" | Clear cache and reload |

---

## Verification Checklist

- [ ] Python 3.8+ installed
- [ ] Node.js 16+ installed
- [ ] Backend dependencies installed
- [ ] Frontend dependencies installed
- [ ] OpenAI API key configured
- [ ] Backend server running (`http://localhost:8000`)
- [ ] Extension loaded in Chrome
- [ ] Default mode analysis working
- [ ] AI mode analysis working
- [ ] Chat functionality working
- [ ] All tests passing

---

## Next Steps

1. **Start backend**: `python backend/main.py`
2. **Start frontend**: `npm run dev` in extension folder
3. **Load extension**: Chrome → `chrome://extensions/`
4. **Test base functionality**: Analyze a chart
5. **Run tests**: Verify everything works

---

## Getting Help

- **API Docs**: `http://localhost:8000/api/docs`
- **Chrome DevTools**: F12 in browser
- **Server Logs**: Check terminal output
- **Git Issues**: Report problems on GitHub

---

**Version**: 3.0.0  
**Last Updated**: May 24, 2026
