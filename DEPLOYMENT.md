# 🚀 Vercel Deployment Guide

## Pre-deployment Checklist

✅ **Fixed Issues:**
- Updated `vercel.json` with Python runtime configuration
- Fixed Python serverless function format in `api/python/predict.py`
- Added proper CORS headers
- Created `requirements.txt` in root directory
- Fixed `predict-model.js` to work without spawn()
- Added `.vercelignore` to exclude unnecessary files

## Deployment Steps

### 1. Install Vercel CLI
```bash
npm install -g vercel
```

### 2. Login to Vercel
```bash
vercel login
```

### 3. Deploy to Vercel
```bash
# From project root directory
vercel

# For production deployment
vercel --prod
```

### 4. Environment Variables (Optional)
If you need any environment variables, set them in Vercel dashboard or via CLI:
```bash
vercel env add VARIABLE_NAME
```

## 📋 API Endpoints After Deployment

- **Main Prediction API**: `https://your-domain.vercel.app/api/predict`
  - Uses Python ML model with fallback to rule-based prediction
  - Handles CORS and error handling

- **Python ML API**: `https://your-domain.vercel.app/api/python/predict`
  - Direct access to Python ML model (serverless function)

- **Analytics API**: `https://your-domain.vercel.app/api/analytics`
  - CSV data processing and statistics

- **Legacy Predict API**: `https://your-domain.vercel.app/api/predict-model`
  - Redirects to main predict API (Vercel compatible)

## 🧪 Testing After Deployment

Test your prediction API:
```bash
curl -X POST https://your-domain.vercel.app/api/predict \
  -H "Content-Type: application/json" \
  -d '{
    "Age": 35,
    "DistanceFromHome": 10,
    "MonthlyIncome": 5000,
    "YearsAtCompany": 3,
    "JobSatisfaction": 4,
    "WorkLifeBalance": 3,
    "OverTime": "No"
  }'
```

## 🔧 Key Configuration Files

1. **vercel.json**: Runtime configuration for Python functions
2. **requirements.txt**: Python dependencies (pandas, scikit-learn, etc.)
3. **.vercelignore**: Files to exclude from deployment
4. **next.config.js**: Next.js configuration

## 📊 Features Available

- ✅ Employee Attrition Dashboard
- ✅ ML-based Risk Prediction (Random Forest)
- ✅ Google Looker Studio Integration
- ✅ Real-time Analytics
- ✅ Responsive UI with Tailwind CSS
- ✅ Serverless Architecture (Python + Node.js)

## 🐛 Troubleshooting

**If Python ML fails:**
- The system automatically falls back to rule-based prediction
- Check Vercel function logs for Python errors
- Ensure all model files are included in deployment

**If build fails:**
- Check that all dependencies are listed in package.json and requirements.txt
- Verify file paths are correct for serverless environment
- Check Vercel build logs for specific errors