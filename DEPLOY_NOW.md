# 🚀 QUICK DEPLOYMENT GUIDE - Hugging Face Spaces

## ✅ Pre-Deployment Checklist

All files are ready for deployment! Here's what has been prepared:

- ✅ `app.py` - Main Streamlit application
- ✅ `requirements.txt` - All Python dependencies
- ✅ `packages.txt` - System dependencies (python3-dev, build-essential)
- ✅ `README_HF.md` - Hugging Face Space description
- ✅ `.streamlit/config.toml` - Streamlit configuration
- ✅ `.streamlit/secrets.toml.example` - Secrets template
- ✅ `setup_hf.sh` - Setup script for spaCy model
- ✅ GitHub repository pushed and ready

---

## 🎯 DEPLOYMENT STEPS (10 Minutes)

### Step 1: Create Hugging Face Account (2 min)
1. Go to https://huggingface.co/
2. Click "Sign Up" (top right)
3. Use your email or GitHub account
4. Verify your email

### Step 2: Create New Space (3 min)
1. Go to https://huggingface.co/new-space
2. Fill in the form:
   - **Owner**: Your username
   - **Space name**: `contract-analysis-risk-assessment` (or your choice)
   - **License**: MIT
   - **Select the Space SDK**: Choose **Streamlit**
   - **Space hardware**: CPU basic (FREE)
   - **Repo type**: Public
3. Click **"Create Space"**

### Step 3: Import Your GitHub Repository (2 min)

**IMPORTANT: After Space is created, you'll see options to add files.**

Click on **"Files and versions"** tab, then:

1. Click the **"⋮"** menu (three dots) next to "Add file"
2. Select **"Import repository"**
3. Enter your GitHub repo URL:
   ```
   https://github.com/UsmanMatheen/contract_analysis_and_risk_assessment_bot
   ```
4. Click **"Import"**

**OR via Git (Alternative):**

```bash
# Clone your HF Space
git clone https://huggingface.co/spaces/YOUR-USERNAME/contract-analysis-risk-assessment
cd contract-analysis-risk-assessment

# Add your GitHub repo as remote and pull
git remote add github https://github.com/UsmanMatheen/contract_analysis_and_risk_assessment_bot.git
git pull github main

# Push to HF
git push origin main
```

### Step 4: Replace README.md (1 min)

**CRITICAL STEP - Don't skip!**

The imported README.md is for GitHub. You need the Hugging Face version:

1. In your Space, go to **"Files and versions"** tab
2. Click on `README.md` file
3. Click **"Edit"** button
4. **Delete ALL content**
5. Copy and paste the **entire content** from `README_HF.md`
6. Click **"Commit changes to main"**

### Step 5: Configure API Keys (2 min)

1. Go to your Space's **"Settings"** tab
2. Scroll down to **"Repository secrets"** section
3. Click **"New secret"** for each of these:

**Minimum Required:**
```
Name: OPENAI_API_KEY
Value: [paste your OpenAI API key]

Name: LLM_PROVIDER
Value: openai

Name: OPENAI_MODEL
Value: gpt-4o-mini
```

**Recommended Additional Secrets:**
```
Name: APP_NAME
Value: Contract Analysis & Risk Assessment

Name: ENVIRONMENT
Value: production

Name: MAX_UPLOAD_SIZE_MB
Value: 10

Name: LOG_LEVEL
Value: INFO
```

4. Click **"Save"** after each secret

### Step 6: Wait for Build (3-5 min)

1. Go to **"App"** tab
2. You'll see "Building..." message
3. Watch the logs for progress
4. Wait for:
   - Dependencies installation
   - spaCy model download
   - App startup

**Common log messages you'll see:**
```
Installing dependencies from requirements.txt...
Installing packages from packages.txt...
Downloading spaCy model...
Starting Streamlit app...
```

### Step 7: Test Your Deployment (2 min)

Once build completes, test:
1. ✅ App loads without errors
2. ✅ Upload a sample contract (PDF/DOCX)
3. ✅ Run analysis
4. ✅ Check results display
5. ✅ Generate PDF report
6. ✅ Browse templates

---

## 🌐 YOUR LIVE URLs

After successful deployment:

**Main Space URL:**
```
https://huggingface.co/spaces/YOUR-USERNAME/contract-analysis-risk-assessment
```

**Direct App URL:**
```
https://YOUR-USERNAME-contract-analysis-risk-assessment.hf.space
```

**For Submission: Use the Direct App URL** ✅

---

## ⚠️ TROUBLESHOOTING

### Issue: "Cannot find module 'en_core_web_lg'"

**Solution:**
The spaCy model might not have downloaded. Add this to `requirements.txt`:

```
en-core-web-lg @ https://github.com/explosion/spacy-models/releases/download/en_core_web_lg-3.7.1/en_core_web_lg-3.7.1-py3-none-any.whl
```

### Issue: "API key not configured"

**Solution:**
1. Go to Settings > Repository secrets
2. Verify `OPENAI_API_KEY` is added
3. Click **"Factory reboot"** in Settings to restart

### Issue: "Application error" or timeout

**Solution:**
1. Check logs in the "Logs" section
2. Verify all dependencies installed
3. Try "Factory reboot" in Settings

### Issue: Build takes too long

**Solution:**
- Normal build time: 3-5 minutes
- If stuck >10 minutes, refresh page or reboot Space
- Check Hugging Face status page

---

## 📸 TAKE SCREENSHOTS FOR SUBMISSION

Once deployed and tested, capture:
1. ✅ Homepage of your app
2. ✅ Contract upload interface
3. ✅ Analysis results page
4. ✅ Risk assessment section
5. ✅ Generated PDF report

---

## 🎬 NEXT STEPS AFTER DEPLOYMENT

### 1. Record Demo Video (Required for submission)
- Show app loading
- Upload sample contract
- Walk through analysis
- Show all features
- Export PDF report
- Upload to YouTube (unlisted is fine)

### 2. Prepare Submission
- ✅ Live URL: `https://YOUR-USERNAME-contract-analysis-risk-assessment.hf.space`
- ✅ GitHub: https://github.com/UsmanMatheen/contract_analysis_and_risk_assessment_bot
- ✅ Demo Video: [YouTube link]
- ✅ Description: Use from PROJECT_COMPLETE.md

### 3. Final Verification
- [ ] App is publicly accessible
- [ ] No login required to use
- [ ] All features working
- [ ] API key configured
- [ ] Demo video uploaded
- [ ] GitHub repo public
- [ ] Submission form filled

---

## 📋 SUBMISSION DETAILS TO PROVIDE

**Live URL:**
```
https://YOUR-USERNAME-contract-analysis-risk-assessment.hf.space
```

**GitHub Repository:**
```
https://github.com/UsmanMatheen/contract_analysis_and_risk_assessment_bot
```

**Video Demo:**
```
https://www.youtube.com/watch?v=YOUR-VIDEO-ID
```

**Project Description:**
```
Enterprise-grade GenAI-powered contract analysis platform that helps SMEs understand complex legal agreements, identify risks, and make informed decisions. Built with GPT-4, spaCy, Streamlit, featuring multi-format document parsing, intelligent clause analysis, comprehensive risk assessment, and professional PDF report generation. Supports English and Hindi contracts with plain-language explanations.
```

---

## 🎉 YOU'RE READY TO DEPLOY!

Follow the steps above and you'll have your app live in ~10 minutes!

**Need help? Check:**
- DEPLOYMENT_HF.md (detailed guide)
- README_HF.md (Space description)
- Hugging Face Docs: https://huggingface.co/docs/hub/spaces

**Good luck with your submission! 🚀**
