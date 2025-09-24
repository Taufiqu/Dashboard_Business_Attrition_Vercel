# Business Attrition Analytics Dashboard

Dashboard analytics komprehensif untuk menganalisis attrition karyawan dengan integrasi Google Looker Studio, dioptimalkan untuk deployment di Vercel.

## 🚀 Fitur Utama

- **Dashboard Interaktif**: Visualisasi data attrition yang comprehensive
- **Google Looker Integration**: Embed dashboard langsung dari Google Looker Studio
- **Responsive Design**: Optimal untuk desktop dan mobile
- **Real-time Data**: Sinkronisasi data secara real-time
- **Export Functionality**: Fitur export data dan laporan
- **Modern UI**: Interface yang clean dan professional

## 🛠️ Tech Stack

- **Framework**: Next.js 14
- **Styling**: Tailwind CSS
- **Icons**: Lucide React
- **Deployment**: Vercel
- **Analytics**: Google Looker Studio

## 📦 Installation

1. Clone repository ini:
```bash
git clone <repository-url>
cd Dashboard_Business_Attrition_Vercel
```

2. Install dependencies:
```bash
npm install
```

3. Jalankan development server:
```bash
npm run dev
```

4. Buka [http://localhost:3000](http://localhost:3000) di browser

## 🔧 Setup Google Looker Embed

1. Buka dashboard Anda di Google Looker Studio
2. Klik tombol "Share" di kanan atas
3. Pilih "Embed report"
4. Copy kode iframe yang diberikan
5. Di aplikasi, klik tombol "Setup Embed" pada halaman dashboard
6. Paste kode embed ke dalam form

## 📱 Halaman Utama

### Home Page (/)
- Overview metrics utama
- Quick insights
- Key performance indicators
- Navigation ke dashboard detail

### Analytics Dashboard (/dashboard)
- Embedded Google Looker dashboard
- Interactive controls
- Real-time data refresh
- Export functionality

## 🚀 Deployment ke Vercel

### Otomatis via GitHub:
1. Push code ke GitHub repository
2. Import project di Vercel dashboard
3. Deploy akan otomatis

### Manual via Vercel CLI:
```bash
npm install -g vercel
vercel login
vercel --prod
```

### Environment Variables (Opsional)
Jika diperlukan, tambahkan environment variables di Vercel dashboard:
- `NEXT_PUBLIC_DASHBOARD_TITLE`: Custom title untuk dashboard
- `NEXT_PUBLIC_COMPANY_NAME`: Nama perusahaan

## 📁 Struktur Project

```
├── pages/
│   ├── index.js          # Homepage dengan overview
│   ├── dashboard.js      # Main dashboard dengan Looker embed
│   └── _app.js          # App configuration
├── components/
│   ├── Layout.js        # Main layout dengan navigation
│   └── LookerEmbed.js   # Component untuk embed Looker
├── styles/
│   └── globals.css      # Global styles
├── public/              # Static assets
├── package.json
├── next.config.js
├── tailwind.config.js
└── vercel.json         # Vercel deployment config
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

## 🔒 Security

- Secure embed implementation
- Environment variable management
- Production-ready configuration
- CORS handling untuk embedded content

## 🐛 Troubleshooting

### Dashboard tidak muncul:
1. Pastikan embed code sudah benar
2. Check console browser untuk error
3. Verifikasi Google Looker sharing settings

### Styling issues:
1. Clear browser cache
2. Check Tailwind compilation
3. Verify CSS imports

## 📞 Support

Untuk pertanyaan atau issues, silakan buat issue di repository ini atau hubungi tim development.

## 📄 License

MIT License - bebas untuk digunakan dan dimodifikasi sesuai kebutuhan.