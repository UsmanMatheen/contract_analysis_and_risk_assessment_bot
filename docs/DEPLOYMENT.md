# 🚀 Deployment Guide

## Production Deployment Options

### Option 1: Streamlit Cloud (Recommended for Quick Deployment)

1. **Prepare Repository**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin <your-repo-url>
   git push -u origin main
   ```

2. **Setup Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Connect your GitHub repository
   - Select the repository and branch
   - Set app file: `app.py`

3. **Configure Secrets**
   - In Streamlit Cloud dashboard, go to App Settings → Secrets
   - Add your environment variables:
   ```toml
   LLM_PROVIDER = "openai"
   OPENAI_API_KEY = "your-api-key-here"
   SECRET_KEY = "your-secret-key-here"
   ```

4. **Deploy**
   - Click "Deploy"
   - Your app will be live at: `https://your-app-name.streamlit.app`

### Option 2: Docker Deployment

1. **Create Dockerfile**
   ```dockerfile
   FROM python:3.10-slim
   
   WORKDIR /app
   
   # Install system dependencies
   RUN apt-get update && apt-get install -y \
       build-essential \
       && rm -rf /var/lib/apt/lists/*
   
   # Copy requirements
   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt
   
   # Download spaCy model
   RUN python -m spacy download en_core_web_lg
   
   # Copy application
   COPY . .
   
   # Expose port
   EXPOSE 8501
   
   # Health check
   HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health
   
   # Run app
   CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
   ```

2. **Create docker-compose.yml**
   ```yaml
   version: '3.8'
   
   services:
     contract-analyzer:
       build: .
       ports:
         - "8501:8501"
       environment:
         - LLM_PROVIDER=${LLM_PROVIDER}
         - OPENAI_API_KEY=${OPENAI_API_KEY}
         - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
       volumes:
         - ./data:/app/data
         - ./logs:/app/logs
       restart: unless-stopped
   ```

3. **Build and Run**
   ```bash
   # Build image
   docker build -t contract-analyzer .
   
   # Run container
   docker-compose up -d
   
   # View logs
   docker-compose logs -f
   ```

### Option 3: AWS EC2 Deployment

1. **Launch EC2 Instance**
   - AMI: Ubuntu 22.04 LTS
   - Instance Type: t3.medium or larger
   - Storage: 20 GB
   - Security Group: Allow ports 22 (SSH), 8501 (Streamlit)

2. **Connect and Setup**
   ```bash
   # SSH into instance
   ssh -i your-key.pem ubuntu@your-ec2-ip
   
   # Update system
   sudo apt update && sudo apt upgrade -y
   
   # Install Python and dependencies
   sudo apt install -y python3-pip python3-venv git
   
   # Clone repository
   git clone <your-repo-url>
   cd contract_analysis_and_risk_assessment_bot
   
   # Create virtual environment
   python3 -m venv venv
   source venv/bin/activate
   
   # Install dependencies
   pip install -r requirements.txt
   python -m spacy download en_core_web_lg
   
   # Configure environment
   cp .env.example .env
   nano .env  # Add your API keys
   ```

3. **Setup Systemd Service**
   ```bash
   sudo nano /etc/systemd/system/contract-analyzer.service
   ```
   
   Add:
   ```ini
   [Unit]
   Description=Contract Analysis Bot
   After=network.target
   
   [Service]
   Type=simple
   User=ubuntu
   WorkingDirectory=/home/ubuntu/contract_analysis_and_risk_assessment_bot
   Environment="PATH=/home/ubuntu/contract_analysis_and_risk_assessment_bot/venv/bin"
   ExecStart=/home/ubuntu/contract_analysis_and_risk_assessment_bot/venv/bin/streamlit run app.py --server.port=8501 --server.address=0.0.0.0
   Restart=always
   
   [Install]
   WantedBy=multi-user.target
   ```
   
   Enable and start:
   ```bash
   sudo systemctl enable contract-analyzer
   sudo systemctl start contract-analyzer
   sudo systemctl status contract-analyzer
   ```

4. **Setup Nginx Reverse Proxy (Optional)**
   ```bash
   sudo apt install -y nginx
   sudo nano /etc/nginx/sites-available/contract-analyzer
   ```
   
   Add:
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;
       
       location / {
           proxy_pass http://localhost:8501;
           proxy_http_version 1.1;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header Host $host;
           proxy_set_header Upgrade $http_upgrade;
           proxy_set_header Connection "upgrade";
           proxy_read_timeout 86400;
       }
   }
   ```
   
   Enable:
   ```bash
   sudo ln -s /etc/nginx/sites-available/contract-analyzer /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl restart nginx
   ```

### Option 4: Heroku Deployment

1. **Create Heroku Files**
   
   `Procfile`:
   ```
   web: sh setup.sh && streamlit run app.py
   ```
   
   `setup.sh`:
   ```bash
   mkdir -p ~/.streamlit/
   echo "\
   [server]\n\
   headless = true\n\
   port = $PORT\n\
   enableCORS = false\n\
   \n\
   " > ~/.streamlit/config.toml
   ```

2. **Deploy**
   ```bash
   # Install Heroku CLI
   heroku login
   
   # Create app
   heroku create your-app-name
   
   # Set config vars
   heroku config:set LLM_PROVIDER=openai
   heroku config:set OPENAI_API_KEY=your-key
   
   # Deploy
   git push heroku main
   
   # Open app
   heroku open
   ```

## Security Considerations

### 1. API Key Protection
- Never commit `.env` file to git
- Use environment variables or secrets management
- Rotate API keys regularly
- Implement rate limiting

### 2. Data Privacy
- Ensure uploaded contracts are not logged
- Implement data retention policies
- Use HTTPS for all connections
- Add authentication if needed

### 3. Monitoring
```bash
# Setup monitoring
pip install prometheus-client

# Add health check endpoint
# Monitor CPU, memory, response times
# Set up alerts for failures
```

### 4. Backup Strategy
```bash
# Backup data directory
rsync -avz data/ backup/data_$(date +%Y%m%d)/

# Backup audit logs
tar -czf logs_backup_$(date +%Y%m%d).tar.gz logs/
```

## Performance Optimization

### 1. Caching
```python
# Enable Streamlit caching
@st.cache_data
def load_model():
    return load_heavy_model()
```

### 2. Load Balancing
- Use multiple instances behind load balancer
- Implement request queuing
- Add CDN for static assets

### 3. Database Optimization
- Use PostgreSQL for audit logs (optional)
- Index frequently queried fields
- Implement connection pooling

## Maintenance

### Daily Tasks
- Monitor logs for errors
- Check disk space
- Verify API key usage

### Weekly Tasks
- Review audit logs
- Update dependencies if needed
- Test backup restoration

### Monthly Tasks
- Security updates
- Performance review
- User feedback analysis

## Troubleshooting

### Issue: Out of Memory
```bash
# Increase instance size or
# Add swap space
sudo fallocate -l 4G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

### Issue: Slow Performance
- Enable caching
- Reduce LLM token limits
- Use faster spaCy model (en_core_web_sm)
- Implement request queuing

### Issue: API Rate Limits
- Implement exponential backoff
- Use multiple API keys with rotation
- Cache repeated requests

## Scaling Strategies

### Horizontal Scaling
1. Deploy multiple instances
2. Use load balancer (AWS ALB, Nginx)
3. Implement session affinity
4. Share storage across instances

### Vertical Scaling
1. Increase instance size
2. Add more CPU/RAM
3. Use GPU instances for larger models

## Cost Optimization

1. **Choose appropriate instance sizes**
2. **Use spot instances for non-critical workloads**
3. **Implement request caching**
4. **Monitor API usage**
5. **Set up budget alerts**

---

**Ready for Production!** Choose the deployment option that best fits your needs.
