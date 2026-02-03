# 🚀 Deploying to Hugging Face Spaces

Complete guide to deploy your Contract Analysis Platform to Hugging Face Spaces.

## 📋 Prerequisites

1. **Hugging Face Account**: Create free account at https://huggingface.co/
2. **API Keys**: OpenAI API key or Anthropic API key
3. **GitHub Repository**: Your code pushed to GitHub (✅ Already done!)

## 🎯 Deployment Steps

### Step 1: Create New Space

1. Go to https://huggingface.co/spaces
2. Click **"Create new Space"**
3. Fill in details:
   - **Name**: `contract-analysis-risk-assessment` (or your preferred name)
   - **License**: MIT
   - **SDK**: Select **Streamlit**
   - **Hardware**: Free CPU (sufficient for this app)
   - **Visibility**: Public

4. Click **"Create Space"**

### Step 2: Connect Your GitHub Repository

**Option A: Import from GitHub (Recommended)**

1. In your new Space, click **"Settings"** tab
2. Scroll to **"Repository"** section
3. Click **"Import repository"**
4. Enter: `https://github.com/UsmanMatheen/contract_analysis_and_risk_assessment_bot.git`
5. Click **"Import"**

**Option B: Push Directly to HF**

```bash
# Add Hugging Face remote
git remote add hf https://huggingface.co/spaces/YOUR-USERNAME/YOUR-SPACE-NAME

# Push to Hugging Face
git push hf main
```

### Step 3: Replace README.md with HF Version

After importing, you need to use the Hugging Face-compatible README:

1. In your Space's **"Files and versions"** tab
2. Click on `README.md`
3. Replace entire content with content from `README_HF.md`
4. Commit the change

OR via command line:
```bash
# Backup current README
mv README.md README_GITHUB.md

# Use HF README
cp README_HF.md README.md

# Commit and push
git add README.md README_GITHUB.md
git commit -m "Add Hugging Face Space README"
git push hf main
```

### Step 4: Configure Secrets (API Keys)

1. Go to your Space's **"Settings"** tab
2. Scroll to **"Repository secrets"** section
3. Add the following secrets:

**Required Secrets:**
```
OPENAI_API_KEY = your-openai-api-key-here
LLM_PROVIDER = openai
OPENAI_MODEL = gpt-4o-mini
```

**Optional Secrets (if using Claude):**
```
ANTHROPIC_API_KEY = your-anthropic-api-key-here
LLM_PROVIDER = anthropic
ANTHROPIC_MODEL = claude-3-sonnet-20240229
```

**Additional Configuration:**
```
APP_NAME = Contract Analysis & Risk Assessment
APP_VERSION = 1.0.0
ENVIRONMENT = production
DEBUG = false
SECRET_KEY = your-random-secret-key-here
SUPPORTED_LANGUAGES = en,hi
MAX_UPLOAD_SIZE_MB = 10
ALLOWED_EXTENSIONS = pdf,docx,doc,txt
RISK_THRESHOLD_MEDIUM = 40
RISK_THRESHOLD_HIGH = 70
LOG_LEVEL = INFO
```

4. Click **"Save"** after adding each secret

### Step 5: Install System Dependencies

The `packages.txt` file is already included and will automatically install:
- python3-dev
- build-essential

These are needed for spaCy and other NLP libraries.

### Step 6: Wait for Build

1. Go to **"App"** tab
2. Hugging Face will automatically:
   - Install dependencies from `requirements.txt`
   - Install system packages from `packages.txt`
   - Download spaCy model
   - Start your Streamlit app

3. Build typically takes **3-5 minutes**

4. Watch the build logs in the **"Logs"** section

### Step 7: Test Your Deployment

1. Once build completes, your app will be live at:
   ```
   https://huggingface.co/spaces/YOUR-USERNAME/YOUR-SPACE-NAME
   ```

2. Test all features:
   - Upload a contract
   - Run analysis
   - Check risk assessment
   - Generate PDF report
   - Browse templates

### Step 8: Troubleshooting

**If spaCy model download fails:**

Create `setup.py` in root:
```python
import subprocess
import sys

def setup():
    subprocess.check_call([sys.executable, "-m", "spacy", "download", "en_core_web_lg"])

if __name__ == "__main__":
    setup()
```

Then add to `requirements.txt`:
```
spacy==3.7.2
en-core-web-lg @ https://github.com/explosion/spacy-models/releases/download/en_core_web_lg-3.7.1/en_core_web_lg-3.7.1-py3-none-any.whl
```

**If app times out:**

Increase timeout in `.streamlit/config.toml`:
```toml
[server]
maxUploadSize = 10
enableXsrfProtection = false
```

## ✅ Verification Checklist

- [ ] Space created on Hugging Face
- [ ] GitHub repository imported
- [ ] README.md replaced with HF version
- [ ] API keys configured in secrets
- [ ] App building successfully
- [ ] spaCy model downloaded
- [ ] App accessible at public URL
- [ ] File upload working
- [ ] Analysis functioning
- [ ] PDF reports generating

## 🌐 Your Live URLs

After deployment, you'll have:

1. **Hugging Face Space URL**: 
   ```
   https://huggingface.co/spaces/YOUR-USERNAME/YOUR-SPACE-NAME
   ```

2. **Direct App URL**:
   ```
   https://YOUR-USERNAME-YOUR-SPACE-NAME.hf.space
   ```

3. **Embed Code** (available in Space settings)

## 📊 Post-Deployment

### Enable Analytics (Optional)
1. Go to Space Settings
2. Enable **"Analytics"**
3. Track visitors and usage

### Add to Portfolio
1. Pin Space to your profile
2. Add to README of GitHub repo
3. Share on social media

### Monitor Performance
1. Check **"Community"** tab for feedback
2. Review **"Logs"** for errors
3. Update based on user feedback

## 🔄 Updating Your Deployment

Whenever you push to GitHub:

```bash
# Make changes locally
git add .
git commit -m "Update features"

# Push to GitHub
git push origin main

# If using HF remote directly
git push hf main
```

Hugging Face will automatically rebuild and redeploy!

## 💡 Pro Tips

1. **Use GPT-4o-mini** for cost-effective API usage
2. **Monitor API usage** to avoid unexpected bills
3. **Add rate limiting** if needed for public access
4. **Keep secrets secure** - never commit to repo
5. **Test thoroughly** before sharing submission URL

## 🆘 Support

If you encounter issues:
- Check Hugging Face Spaces documentation
- Review build logs for errors
- Verify API keys are correct
- Ensure all dependencies installed

## 🎉 Success!

Once deployed, your app will be:
- ✅ Publicly accessible 24/7
- ✅ No sleep issues (always on)
- ✅ Professional URL
- ✅ Perfect for your submission!

---

**Ready for next step?** Copy your live URL and prepare your submission! 🚀
