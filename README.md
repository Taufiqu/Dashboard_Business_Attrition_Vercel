# 📊 Dashboard Business Attrition Analytics

Aplikasi web modern untuk menganalisis dan memprediksi employee attrition (tingkat keluar karyawan) menggunakan machine learning model Random Forest yang sudah dilatih.

## 🎯 Overview

Dashboard ini dirancang untuk membantu HR dan manajemen dalam:
- **Analisis Employee Attrition**: Dashboard visual dengan integrasi Google Looker Studio
- **Prediksi ML Real-time**: Machine learning prediction menggunakan Random Forest
- **Risk Assessment**: Penilaian risiko karyawan berdasarkan 47 faktor berbeda
- **Feature Importance**: Identifikasi faktor-faktor utama yang mempengaruhi attrition

## 🏗️ Tech Stack

### Frontend
- **Framework**: Next.js 14 dengan React
- **Styling**: Tailwind CSS dengan konfigurasi custom
- **Icons**: Lucide React
- **Deployment**: Optimized untuk Vercel

### Backend & ML
- **API Routes**: Next.js API routes
- **ML Model**: Random Forest (scikit-learn) dengan 47 features
- **Python**: pandas, scikit-learn, joblib, numpy
- **Data**: CSV processing dan analytics

## 📁 Struktur Project

```
Dashboard_Business_Attrition_Vercel/
├── components/
│   ├── ClientOnly.js           # Client-side rendering wrapper
│   ├── Layout.js               # Main layout dengan sidebar
│   ├── LookerEmbed.js          # Google Looker Studio integration
│   └── PredictionForm.js       # ML prediction form
├── pages/
│   ├── api/
│   │   ├── analytics.js        # CSV data analytics API
│   │   ├── predict.js          # Main prediction API
│   │   └── predict-model.js    # Direct ML model API
│   ├── index.js                # Homepage
│   ├── dashboard.js            # Looker dashboard
│   ├── prediction.js           # ML prediction page
│   └── settings.js
├── scripts/
│   ├── predict_with_model.py   # Main ML prediction script
│   └── check_model_features.py # Feature debugging script
├── models/
│   ├── rf_model.pkl           # Trained Random Forest model
│   └── scaler.pkl             # StandardScaler untuk preprocessing
├── public/data/
│   └── hasil_output_DSP (2).csv # Employee dataset
└── .venv/                     # Python virtual environment
```

## 🚀 Installation & Setup

### 1. Clone Repository
```bash
git clone https://github.com/Taufiqu/Dashboard_Business_Attrition_Vercel.git
cd Dashboard_Business_Attrition_Vercel
```

### 2. Install Dependencies
```bash
# Install Node.js dependencies
npm install

# Setup Python virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac

# Install Python dependencies
pip install -r requirements.txt
```

### 3. Run Development Server
```bash
npm run dev
```

Buka [http://localhost:3000](http://localhost:3000) untuk melihat aplikasi.

## 🔧 ML Model Specifications

### Model Features (47 total)

#### Numerical Features (26):
```
EmployeeId, Age, DailyRate, DistanceFromHome, Education, 
EmployeeCount, EnvironmentSatisfaction, HourlyRate, JobInvolvement,
JobLevel, JobSatisfaction, MonthlyIncome, MonthlyRate,
NumCompaniesWorked, PercentSalaryHike, PerformanceRating,
RelationshipSatisfaction, StandardHours, StockOptionLevel,
TotalWorkingYears, TrainingTimesLastYear, WorkLifeBalance,
YearsAtCompany, YearsInCurrentRole, YearsSinceLastPromotion,
YearsWithCurrManager
```

#### Categorical Features (21 - One-Hot Encoded):
```
BusinessTravel_*, Department_*, EducationField_*, Gender_Male,
JobRole_*, MaritalStatus_*, OverTime_Yes
```

### Model Performance
- **Algorithm**: Random Forest Classifier
- **Preprocessing**: StandardScaler normalization
- **Output**: Binary classification (Stay/Leave) + probability scores
- **Features**: 47 engineered features dengan categorical encoding

## 📱 Features

### ✅ Implemented
- **🤖 ML Prediction**: Random Forest model dengan 47 features
- **📊 Visual Dashboard**: Google Looker Studio integration
- **🎨 Modern UI**: Responsive design dengan Tailwind CSS
- **⚡ Real-time Processing**: Fast API responses dengan Python integration
- **🛡️ Fallback System**: Rule-based backup prediction
- **📈 Feature Importance**: Top contributing factors analysis
- **🔍 Risk Assessment**: High/Medium/Low risk categorization

### 🔄 In Development
- **📊 Historical Tracking**: Prediction history dan trends
- **🔧 Model Versioning**: MLflow integration
- **📝 Advanced Analytics**: Detailed employee insights

## 🛠️ API Endpoints

### `/api/predict` (POST)
Main prediction endpoint dengan fallback system.

**Request:**
```json
{
  "Age": 25,
  "MonthlyIncome": 5000,
  "YearsAtCompany": 2,
  "DistanceFromHome": 10,
  "JobSatisfaction": 3,
  "WorkLifeBalance": 2,
  "OverTime": "Yes"
}
```

**Response:**
```json
{
  "success": true,
  "prediction": 0,
  "prediction_label": "Will Stay",
  "probability": 0.23,
  "risk_level": "Low",
  "feature_importance": {
    "MonthlyIncome": 0.15,
    "Age": 0.12,
    "YearsAtCompany": 0.10
  }
}
```

### `/api/analytics` (GET)
Employee data analytics dari CSV dataset.

## 🔧 Setup Google Looker Embed

1. Buka dashboard Anda di Google Looker Studio
2. Klik tombol "Share" di kanan atas
3. Pilih "Embed report"
4. Copy kode iframe yang diberikan
5. Di aplikasi, klik tombol "Setup Embed" pada halaman dashboard
6. Paste kode embed ke dalam form

## 🎯 Usage

### 1. Dashboard Analytics
- Navigasi ke `/dashboard` untuk melihat Looker Studio dashboard
- Analisis trends dan patterns employee attrition
- Interactive data visualization

### 2. ML Prediction
- Navigasi ke `/prediction` untuk prediksi individual
- Input employee data (minimal: Age, MonthlyIncome, YearsAtCompany, DistanceFromHome)
- Dapatkan prediction, probability score, dan risk assessment
- Lihat feature importance untuk insights

### 3. Settings
- Konfigurasi dashboard preferences
- Model parameter adjustments (future feature)

## 🐛 Troubleshooting

### Common Issues

**1. Python Module Error:**
```bash
# Pastikan virtual environment aktif
.venv\Scripts\activate
pip install -r requirements.txt
```

**2. Model File Missing:**
```bash
# Pastikan model files ada di folder models/
ls models/
# Should contain: rf_model.pkl, scaler.pkl
```

**3. API Timeout:**
- Check Python script execution
- Verify virtual environment path
- Check error logs di browser console

### Dashboard tidak muncul:
1. Pastikan embed code sudah benar
2. Check console browser untuk error
3. Verifikasi Google Looker sharing settings

## 📊 Data Flow

```
User Input → Frontend Validation → API Call → Python Script → 
Model Loading → Data Preprocessing → ML Prediction → 
Result Processing → JSON Response → Frontend Display
```

## 🚀 Deployment

### Vercel Deployment
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel --prod
```

### Environment Variables
Pastikan setting environment variables untuk:
- Python path configuration
- Model file paths
- API endpoints

### Manual via Vercel CLI:
```bash
npm install -g vercel
vercel login
vercel --prod
```

## 🎨 Customization

### Mengubah Tema:
Edit file `tailwind.config.js` untuk mengubah color scheme:

```javascript
colors: {
  primary: {
    // Ganti dengan warna brand Anda
  }
}
```

### Menambah Metrics:
Edit array `stats` di `pages/index.js` untuk menambah atau mengubah metrics.

### Custom Layout:
Modifikasi `components/Layout.js` untuk mengubah struktur navigasi.

## 📊 Monitoring & Analytics

Dashboard ini mendukung:
- Real-time data monitoring
- Historical trend analysis
- Departmental breakdown
- Predictive insights
- Export ke berbagai format

## 🤝 Contributing

1. Fork repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 🔒 Security

- Secure embed implementation
- Environment variable management
- Production-ready configuration
- CORS handling untuk embedded content

## 📄 License

MIT License - bebas untuk digunakan dan dimodifikasi sesuai kebutuhan.

## 👥 Team

- **Taufiqu** - Project Lead & ML Engineer
- **Contributors** - [Add your name here]

## 📞 Support

Untuk pertanyaan atau support:
- GitHub Issues: [Create an issue](https://github.com/Taufiqu/Dashboard_Business_Attrition_Vercel/issues)
- Email: [your-email@example.com]

---

*Built with ❤️ using Next.js and Machine Learning*