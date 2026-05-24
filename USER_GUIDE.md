# Trading Chart Analyzer - User Guide

**Version**: 3.0.0  
**Last Updated**: May 24, 2026

---

## Table of Contents

1. [Getting Started](#getting-started)
2. [Features Overview](#features-overview)
3. [Default Mode (Formula-Based)](#default-mode-formula-based)
4. [AI Mode (Vision-Based)](#ai-mode-vision-based)
5. [Using AI Chat](#using-ai-chat)
6. [Understanding Results](#understanding-results)
7. [Tips & Tricks](#tips--tricks)
8. [FAQ](#faq)

---

## Getting Started

### Installation

1. **Install Extension**:
   - Download from Chrome Web Store (when available)
   - Or load from source: `chrome://extensions/` → Load unpacked → Select `extension/public`

2. **Verify Backend**:
   - Backend should be running at `http://localhost:8000`
   - Extension will display connection status

3. **API Key Setup** (for AI mode):
   - Obtain OpenAI API key: https://platform.openai.com/api-keys
   - Key is configured in backend `.env` file

### First Use

1. Open a trading chart in your browser (TradingView, etc.)
2. Click extension icon in toolbar
3. Select analysis mode (Default or AI)
4. Click "Analyze" button
5. View results

---

## Features Overview

### Two Analysis Modes

#### 🔷 Default Mode
- **Speed**: Instant (< 100ms)
- **Cost**: Free
- **Requirements**: No API key needed
- **Best For**: Quick analysis, learning, offline use

#### 🤖 AI Mode
- **Speed**: A few seconds (3-5s)
- **Cost**: Uses OpenAI credits
- **Requirements**: OpenAI API key
- **Best For**: Detailed analysis, follow-up questions

### Core Features

✅ **Technical Indicators**
- EMA (Exponential Moving Average)
- RSI (Relative Strength Index)
- MACD (Moving Average Convergence Divergence)
- ATR (Average True Range)
- Support/Resistance Detection

✅ **AI Analysis**
- GPT-4 Vision chart interpretation
- Market structure analysis
- Pattern recognition
- Risk/reward scenarios

✅ **Interactive Chat**
- Ask follow-up questions
- Maintain chart context
- Multiple conversations
- Session-based history

✅ **Professional Output**
- Entry/exit recommendations
- Stop loss levels
- Take profit targets
- Confidence scoring
- Signal validation

---

## Default Mode (Formula-Based)

### How It Works

Default mode uses mathematical formulas to analyze charts without any external API.

### Quick Analysis

1. **Select Mode**: Click "Default" in mode selector
2. **Analyze**: Click "Analyze" button
3. **View Results**: Analysis appears instantly

### Reading Results

#### Trend
- **BULLISH** (📈): Price likely to rise
- **BEARISH** (📉): Price likely to fall
- **NEUTRAL** (➡️): Uncertain direction

#### Confidence Level
- **75-100%**: Very confident signal
- **50-75%**: Moderate confidence
- **25-50%**: Mixed signals
- **0-25%**: Weak signal

#### Entry Zone
- **Minimum (min)**: Lowest entry price
- **Maximum (max)**: Highest entry price
- *Enter between these levels*

#### Stop Loss
- Price level where you admit you were wrong
- Set it below the entry zone
- Limit your potential loss

#### Take Profit Targets
- TP1: Conservative exit (retest support)
- TP2: Moderate exit (mid-range)
- Price levels to close positions

#### Indicators
- **EMA 20/50/200**: Trend indicators
  - Price > EMA20 > EMA50 > EMA200 = Strong uptrend
- **RSI**: Momentum (0-100 scale)
  - Above 70: Overbought (potential pullback)
  - Below 30: Oversold (potential bounce)
  - 30-70: Normal range
- **MACD**: Momentum crossover
- **ATR**: Volatility measure

### Example Interpretation

```
Trend: BULLISH
Confidence: 75%
Entry: 64,000 - 64,500
Stop Loss: 63,500
TP1: 65,000
TP2: 66,000
TP3: 67,000

Signals:
✓ EMA20 > EMA50
✓ RSI > 50
✓ Volume increasing
✗ MACD not confirmed
```

**Interpretation**: Moderately bullish setup. Good risk/reward at 75% confidence. Watch for volume to confirm breakout.

---

## AI Mode (Vision-Based)

### How It Works

AI Mode uses GPT-4 Vision to "see" the chart like a professional trader.

### Setup

1. **Add API Key**:
   - Edit `backend/.env`
   - Add: `OPENAI_API_KEY=sk_your_key_here`
   - Restart backend server

2. **Verify Connection**:
   - Go to `http://localhost:8000/api/health`
   - Should show healthy status

### Full AI Analysis

1. **Select Mode**: Click "AI" in mode selector
2. **Analyze**: Click "Analyze" button
3. **Wait**: Processing takes 3-5 seconds
4. **Read Results**: Detailed AI analysis displays

### AI Analysis Components

#### Market Structure
AI describes the current price pattern and trend structure

```
"BTC is in a higher-high, higher-low pattern with support 
at 63,500 and resistance at 65,500. Price consolidated above 
the 200-day MA, showing strength."
```

#### Technical Observations
Analysis of key technical elements

```
Indicators:
- RSI showing strength above 60, not overbought
- MACD positive histogram expanding
- Volume higher on up days

Patterns:
- Ascending triangle forming
- Multiple tests of resistance
```

#### Entry Strategy
Recommended entry points with rationale

```
Primary: Enter on pullback to 64,000 (test of MA support)
Alternative: Aggressive entry on breakout above 64,500
Reasoning: Confluence of multiple reversal factors
```

#### Risk Management
Stop loss and profit targets

```
Stop Loss: 63,500 (breaks MA200, invalidates setup)
Targets:
- TP1: 65,000 (previous resistance)
- TP2: 65,500 (major resistance)
- TP3: 66,500 (structural target)
```

#### Scenarios
What happens in different market conditions

```
Bullish Case: If support holds at 64K, target 67K
Bearish Case: If breaks 63.5K, next support 62.5K
```

#### Confidence
Overall confidence in the analysis (0-100%)

---

## Using AI Chat

### Starting a Chat

1. **After AI Analysis**:
   - Click "💬 Enable AI Chat" button
   - Chat interface appears

2. **Ask Questions**:
   - Type your question
   - Press Enter or click Send

### Great Chat Questions

**About the entries**:
- "Why is the entry point at 64,000?"
- "What would be a more aggressive entry?"
- "At what price would you exit this setup?"

**About the analysis**:
- "Why did you say the trend is bullish?"
- "How confident are you in this analysis?"
- "What are the key levels to watch?"

**About risk management**:
- "Where is the stop loss and why?"
- "What's the risk/reward ratio?"
- "How much should I risk on this trade?"

**About confirmation**:
- "What would invalidate this analysis?"
- "What price action would confirm the signal?"
- "Do higher timeframes support this view?"

### Chat Tips

- **Be Specific**: Instead of "explain the analysis," ask "why is RSI bullish?"
- **Ask Progressively**: Build questions from basic → detailed
- **Use Context**: AI remembers previous questions
- **Get Confirmation**: Always ask for invalidation levels

### Example Chat

```
You: "Is this a good entry?"
AI: "Yes, 64,000 provides good risk/reward with support 
     from MA200 and recent price action."

You: "What would make you wrong?"
AI: "Break below 63,500 would invalidate the bullish 
     structure. Below 63,000 would confirm a reversal."

You: "Should I wait for confirmation?"
AI: "If aggressive, enter now. Conservative traders should 
     wait for a pullback to 64,000 to confirm support holds."
```

---

## Understanding Results

### Confidence Scores

**Color Coding**:
- 🟢 **Green (75-100%)**: High confidence, good risk/reward
- 🟡 **Yellow (50-75%)**: Moderate confidence, worth considering
- 🔴 **Red (0-50%)**: Low confidence, weak signal

### Reading Signals

**✓ Confirming Signals** (bullish momentum):
- EMA20 > EMA50 > EMA200
- RSI > 50 and rising
- MACD positive
- Volume increasing toward target

**✗ Non-Confirming** (bearish pressure):
- EMA20 < EMA50 < EMA200
- RSI < 50 and falling
- MACD negative
- Volume decreasing or on down days

### Risk/Reward Analysis

```
Entry: 64,000
Stop: 63,500
Target: 65,000

Risk: 500 points
Reward: 1,000 points
Risk/Reward Ratio: 1:2 (Good!)
```

**Rule of Thumb**:
- Risk/Reward > 1:2 = Good trade setup
- Risk/Reward > 1:3 = Excellent setup
- Risk/Reward < 1:1 = Avoid

---

## Tips & Tricks

### Best Practices

✅ **Do**:
- Screenshot charts clearly (full screen)
- Use appropriate timeframes (1h, 4h, daily)
- Analyze major support/resistance areas
- Confirm with volume
- Set stop losses before entering

❌ **Don't**:
- Trade blurry or partial charts
- Ignore the stop loss
- Over-leverage small setups
- Chase price into entries
- Ignore invalidation levels

### Screenshot Tips

Good screenshots:
- Full chart visible
- Clear candles/bars
- Indicators visible
- Proper aspect ratio

Bad screenshots:
- Partial chart cut off
- Zoomed in too much
- Blurry image
- Missing price scale

### Analysis Best Practices

1. **Identify Trend**: Is price above/below key MAs?
2. **Find Support**: Where would price bounce?
3. **Find Resistance**: Where would price reject?
4. **Confirm Indicators**: Do indicators align?
5. **Plan Entry**: Where's the best entry?
6. **Set Stop Loss**: Where does it break?
7. **Take Profits**: Target prices?

### Market Conditions

**Trending Market**:
- Favor entries in direction of trend
- Use MAs for entries/exits
- Higher probability of success

**Ranging Market**:
- Entries at support/resistance
- Look for bounces
- Be prepared for breakouts

**Volatile Market**:
- Use larger stop losses
- Reduce position size
- Wait for consolidation

---

## FAQ

### General Questions

**Q: Do I need an OpenAI API key?**  
A: Only for AI mode. Default mode is completely free.

**Q: How much does AI mode cost?**  
A: Costs depend on OpenAI pricing. Typical analysis uses ~$0.01 per image.

**Q: How long does analysis take?**  
A: Default mode: <100ms. AI mode: 3-5 seconds.

**Q: Can I use this on mobile?**  
A: Extension is Chrome-only (desktop). Mobile support planned for v4.

### Technical Questions

**Q: Where is my data stored?**  
A: Sessions stored in memory for 60 minutes. Not persisted to disk.

**Q: Can I export analysis?**  
A: Not yet. Export feature coming in v4.

**Q: How many messages can I save?**  
A: All messages in current session until session expires (60 min).

**Q: Can I share analysis?**  
A: Screenshot the results and share manually. Direct sharing coming in v4.

### Trading Questions

**Q: Should I follow all recommendations?**  
A: Use as a tool, not gospel. Always trade your own strategy.

**Q: What timeframes work best?**  
A: 1h, 4h, daily work well. Adjust for your trading style.

**Q: How reliable is the analysis?**  
A: AI analysis is educational. Backtest before trading.

**Q: What about commissions/slippage?**  
A: Account for these in your analysis!

### Troubleshooting

**Q: "Backend connection failed"**  
A: Ensure backend running at http://localhost:8000

**Q: "API key invalid"**  
A: Check API key in .env file, redeploy backend

**Q: "Session not found"**  
A: Session expired (60 min limit). Start new analysis.

**Q: "Image too blurry"**  
A: Take a clearer screenshot at higher resolution

---

## Learning Resources

### Technical Analysis Basics
- EMA crossovers for trend
- RSI for momentum
- Support/resistance for entries/exits
- Volume for confirmation

### Risk Management
- Always use stop losses
- Risk only 1-2% per trade
- Target 2:1 reward/risk minimum
- Never average down on losing trades

### Trading Psychology
- Have a plan before entering
- Follow your rules
- Don't chase price
- Take losses quickly

---

## Getting Help

### Within the Extension
- Check API docs: http://localhost:8000/api/docs
- View health: http://localhost:8000/api/health
- Check browser console: F12 → Console tab

### External Resources
- TradingView Education: https://www.tradingview.com/education/
- Investopedia: https://www.investopedia.com/
- OpenAI Docs: https://platform.openai.com/docs

---

## Version History

**v3.0.0** (May 2024): AI chat system launched
**v2.0.0** (Apr 2024): AI mode added
**v1.0.0** (Mar 2024): Initial release

---

**Happy Trading! 📈**

*Disclaimer: This tool is for educational purposes. Always conduct your own analysis and never risk more than you can afford to lose.*
