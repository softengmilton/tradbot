# Trading Chart Analyzer - Deployment Guide

**Version**: 3.0.0  
**Last Updated**: May 24, 2026

---

## Table of Contents

1. [Production Checklist](#production-checklist)
2. [Backend Deployment](#backend-deployment)
3. [Frontend Deployment](#frontend-deployment)
4. [Chrome Web Store Publication](#chrome-web-store-publication)
5. [Monitoring & Maintenance](#monitoring--maintenance)
6. [Scaling](#scaling)
7. [Security Hardening](#security-hardening)
8. [Disaster Recovery](#disaster-recovery)

---

## Production Checklist

Before deploying to production, verify all items:

### Security

- [ ] Remove DEBUG=True from .env
- [ ] Use strong OPENAI_API_KEY
- [ ] Update ALLOWED_ORIGINS in CORS config
- [ ] Enable HTTPS/SSL certificates
- [ ] Disable /api/docs in production
- [ ] Set secure session cookies
- [ ] Implement rate limiting (done)
- [ ] Input validation enabled (done)

### Performance

- [ ] Frontend minified (npm run build)
- [ ] Backend using gunicorn/uvicorn workers
- [ ] Caching configured
- [ ] CDN configured (for static assets)
- [ ] Database optimized (when added)
- [ ] Load testing completed

### Testing

- [ ] Unit tests passing (100%)
- [ ] Integration tests passing
- [ ] Load tests at 1000+ requests/sec
- [ ] Security audit completed
- [ ] UAT signed off

### Documentation

- [ ] API documentation complete
- [ ] Deployment runbook created
- [ ] Incidents procedures documented
- [ ] Support contacts defined

### Monitoring

- [ ] Logging configured
- [ ] Metrics collection setup
- [ ] Alerts configured
- [ ] Dashboards created

---

## Backend Deployment

### Option 1: Heroku Deployment

**Prerequisites**:

- Heroku account (https://www.heroku.com)
- Heroku CLI installed

**Steps**:

```bash
# 1. Create Heroku app
heroku create trading-chart-analyzer

# 2. Add OpenAI API key secret
heroku config:set OPENAI_API_KEY=sk_...

# 3. Deploy
git push heroku main

# 4. Check logs
heroku logs --tail

# 5. Verify
curl https://trading-chart-analyzer.herokuapp.com/api/health
```

**Procfile** (create in root):

```
web: uvicorn backend.main:app --host 0.0.0.0 --port $PORT --workers 4
```

### Option 2: DigitalOcean Deployment

**Steps**:

1. **Create Droplet**:
   - Image: Ubuntu 22.04
   - Size: $5-10/month minimum
   - Region: Closest to users

2. **SSH into Droplet**:

```bash
ssh root@your_droplet_ip
```

3. **Setup Environment**:

```bash
apt update
apt install python3 python3-pip python3-venv git nginx

# Clone repository
git clone https://github.com/softengmilton/tradbot.git
cd tradbot/backend

# Setup virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install gunicorn

# Create .env file
nano .env
# Add: OPENAI_API_KEY=sk_...
```

4. **Configure Gunicorn**:

```bash
# Create gunicorn service
sudo nano /etc/systemd/system/trading-analyzer.service
```

Add:

```ini
[Unit]
Description=Trading Chart Analyzer
After=network.target

[Service]
Type=notify
User=root
WorkingDirectory=/root/tradbot/backend
ExecStart=/root/tradbot/backend/venv/bin/gunicorn main:app \
    --workers 4 \
    --bind 127.0.0.1:8000 \
    --timeout 120

[Install]
WantedBy=multi-user.target
```

Start service:

```bash
sudo systemctl start trading-analyzer
sudo systemctl enable trading-analyzer
```

5. **Configure Nginx**:

```bash
sudo nano /etc/nginx/sites-available/trading-analyzer
```

Add:

```nginx
server {
    listen 80;
    server_name trading-analyzer.com www.trading-analyzer.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # API docs
    location /api/docs {
        deny all;  # Disable in production
    }
}
```

Enable site:

```bash
sudo ln -s /etc/nginx/sites-available/trading-analyzer /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

6. **Enable HTTPS** (Let's Encrypt):

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d trading-analyzer.com
```

7. **Setup Firewall**:

```bash
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

### Option 3: AWS Deployment

**Using AWS Lambda + API Gateway**:

1. **Prepare**:

```bash
pip install zappa

# In backend directory
zappa init

# Deploy
zappa deploy production

# Update
zappa update production
```

**Using AWS EC2**:

1. Launch EC2 instance (Ubuntu 22.04)
2. Follow DigitalOcean steps above (same Linux setup)
3. Configure Route 53 for domain
4. Use AWS Certificate Manager for HTTPS

### Option 4: Docker Deployment

**Create Dockerfile**:

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY backend/requirements.txt .
RUN pip install -r requirements.txt

COPY backend/ .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Docker Compose**:

```yaml
version: "3.8"
services:
  api:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      OPENAI_API_KEY: ${OPENAI_API_KEY}
      LOG_LEVEL: INFO
    restart: unless-stopped
```

Deploy:

```bash
docker-compose up -d
```

---

## Frontend Deployment

### Option 1: Chrome Web Store

See **Chrome Web Store Publication** section below.

### Option 2: Self-Hosted

1. **Build**:

```bash
cd extension
npm run build
```

2. **Upload to CDN** (AWS S3, Cloudflare, etc):

```bash
# Example: S3
aws s3 sync public/ s3://my-bucket/extension/
```

3. **Host manifest.json**:
   Update manifest to point to hosted resources

### Option 3: Direct Distribution

Share `.crx` file (Chrome extension package):

```bash
# In Chrome DevTools
# More tools → Extensions → Pack extension
# Select extension folder
```

---

## Chrome Web Store Publication

### Prerequisites

1. **Chrome Developer Account**:
   - Go to https://chrome.google.com/webstore/devconsole
   - Pay $5 one-time registration fee
   - Create developer profile

2. **Prepare Extension**:
   - Version bumped in manifest.json
   - Build latest: `npm run build`
   - All tests passing
   - Screenshots ready (1280x800)
   - Store listing written

### Submission Steps

1. **Create Store Listing**:

```json
{
  "name": "Trading Chart Analyzer - AI Powered",
  "short_description": "AI-powered chart analysis with GPT-4 Vision",
  "description": "Professional trading analysis using AI and technical indicators...",
  "category": "Productivity",
  "language": "en",
  "detailed_description": "Full description here..."
}
```

2. **Upload in Console**:
   - Go to https://chrome.google.com/webstore/devconsole
   - Click "New item"
   - Upload extension folder (public/)
   - Fill in store listing
   - Upload screenshots

3. **Store Listing Details**:

**Short Description** (132 chars):

```
Professional trading chart analysis with AI and technical indicators
```

**Full Description** (4000 chars max):

```
Trading Chart Analyzer provides instant professional trading analysis:

✨ Features:
• Fast technical analysis (EMA, RSI, MACD, ATR)
• AI-powered GPT-4 Vision analysis
• Interactive follow-up questions
• Entry/exit recommendations
• Risk management guidance
• Support/resistance detection

🚀 Two Analysis Modes:
• Default: Free, instant formula-based analysis
• AI: GPT-4 Vision detailed analysis with chat

📊 Indicators:
• EMA 20/50/200 crossovers
• RSI momentum
• MACD trend
• ATR volatility
• Volume analysis

💡 For traders who want:
• Instant chart analysis
• AI-powered insights
• Follow-up questions
• Professional signals
• Education

Note: Requires OpenAI API key for AI mode (free tier available).
```

4. **Screenshots** (1280x800 PNG):

- Screenshot 1: Default mode analysis
- Screenshot 2: AI analysis results
- Screenshot 3: Chat interface
- Screenshot 4: Entry/exit levels

5. **Icon Assets**:

- 128x128 (app icon)
- 16x16 (favicon)
- PNG format, transparent background

6. **Review Requirements**:
   - Clear permissions usage
   - Privacy policy
   - Support email
   - Legitimate purpose

7. **Privacy Policy**:

Create `PRIVACY.md`:

```markdown
# Privacy Policy

We do not collect user data. Images analyzed are:

- Stored temporarily in memory
- Not saved or transmitted
- Deleted after 60 minutes

OpenAI API calls send images to OpenAI's servers.
Review OpenAI's privacy policy for details.
```

8. **Submit**:
   - Click "Submit"
   - Review takes 24-48 hours
   - Check email for approval/rejections

---

## Monitoring & Maintenance

### Logging & Alerts

**Setup Monitoring**:

```python
# backend/monitoring.py
import logging
import sys

class ProductionLogger:
    @staticmethod
    def setup():
        logger = logging.getLogger("trading-analyzer")
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

logger = ProductionLogger.setup()
```

**Alert on Errors**:

```python
# Send alerts to email/Slack
if error_rate > 0.05:  # 5% error rate
    send_alert("High error rate detected")
```

### Health Checks

```bash
# Monitor endpoint
curl https://api.trading-analyzer.com/api/health

# Expected response:
# {"status": "healthy", "metrics": {...}}
```

### Log Aggregation

**ELK Stack** or **CloudWatch**:

```bash
# Forward logs to centralized system
docker run logspout:latest \
  -e "ROUTE_SOURCES=syslog://api.trading-analyzer.com:5000"
```

---

## Scaling

### Horizontal Scaling

**Load Balancer** (nginx/HAProxy):

```bash
# Multiple API instances
api1.trading-analyzer.com:8000
api2.trading-analyzer.com:8000
api3.trading-analyzer.com:8000

# Load balancer
nginx
  → api1
  → api2
  → api3
```

**Configuration**:

```nginx
upstream api {
    server api1.trading-analyzer.com:8000;
    server api2.trading-analyzer.com:8000;
    server api3.trading-analyzer.com:8000;
}

server {
    listen 443 ssl;
    server_name api.trading-analyzer.com;

    location /api/ {
        proxy_pass http://api;
    }
}
```

### Database

**Session Storage** (upgrade from memory):

```python
# PostgreSQL
from sqlalchemy import create_engine

engine = create_engine(
    'postgresql://user:pass@localhost/trading_analyzer'
)

# Redis for caching
import redis
cache = redis.Redis(host='localhost', port=6379)
```

### CDN for Static Assets

```bash
# CloudFlare or AWS CloudFront
# Serve extension from edge servers
```

---

## Security Hardening

### HTTPS/TLS

```bash
# Generate certificate
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365

# Use in gunicorn
gunicorn main:app --certfile=cert.pem --keyfile=key.pem
```

### API Security Headers

```python
# Enabled in security.py
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
Content-Security-Policy: default-src 'self'
Strict-Transport-Security: max-age=31536000
```

### API Key Security

```python
# Never log API keys
logger.info(f"API key: {api_key[:10]}...")  # OK
logger.info(f"API key: {api_key}")  # WRONG
```

### CORS Restriction

```python
# Whitelist only trusted origins
ALLOWED_ORIGINS = [
    "https://trading-analyzer.com",
    "https://www.trading-analyzer.com"
]
```

---

## Disaster Recovery

### Backup Strategy

```bash
# Daily backups
0 2 * * * /backup/backup.sh

# Backup script
#!/bin/bash
tar -czf backup-$(date +%Y%m%d).tar.gz /app
aws s3 cp backup-*.tar.gz s3://backups/trading-analyzer/
```

### Restore Procedure

```bash
# Download backup
aws s3 cp s3://backups/trading-analyzer/backup-20240524.tar.gz .

# Extract
tar -xzf backup-20240524.tar.gz

# Restart services
systemctl restart trading-analyzer
```

---

## Maintenance Windows

**Recommended Schedule**:

- Tuesday 2-4 AM UTC
- Notify users 1 week ahead
- Keep downtime < 30 minutes

**Steps**:

1. Announce maintenance
2. Set maintenance page
3. Run migrations
4. Update dependencies
5. Restart services
6. Test all endpoints
7. Resume traffic

---

## Deployment Checklist

- [ ] Tests passing (100%)
- [ ] Performance benchmarked
- [ ] Security audit passed
- [ ] Documentation updated
- [ ] Backup verified
- [ ] Health checks configured
- [ ] Alerts configured
- [ ] Monitoring setup
- [ ] Rollback plan ready
- [ ] Team trained

---

**Ready to deploy! 🚀**

For support: deployment@tradbot.com
