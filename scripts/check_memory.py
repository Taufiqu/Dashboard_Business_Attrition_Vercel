import tracemalloc
import json
import sys
import time
from pathlib import Path

# 1. Mulai pelacakan SEBELUM mengimpor library berat
tracemalloc.start()

print("Memulai pelacakan memori...", file=sys.stderr)
start_time = time.time()

# 2. Impor semua library berat yang digunakan skrip utama Anda
# Ini adalah bagian BESAR dari penggunaan memori "cold start"
try:
    import pandas as pd
    import numpy as np
    import joblib
    from sklearn.preprocessing import StandardScaler
    from sklearn.ensemble import RandomForestClassifier # Impor ini untuk memastikan sklearn dimuat penuh
    
    # Impor fungsi dari skrip prediksi Anda
    # Asumsikan check_memory.py ada di folder 'scripts'
    from predict_with_model import load_model_and_scaler, preprocess_input_data
    
except ImportError as e:
    print(f"Error import: {e}. Pastikan .venv Anda aktif.", file=sys.stderr)
    tracemalloc.stop()
    sys.exit(1)

lib_import_time = time.time()
print(f"Library diimpor. (Waktu: {lib_import_time - start_time:.2f}s)", file=sys.stderr)

# 3. Ambil snapshot memori setelah impor
snap_after_imports = tracemalloc.take_snapshot()
current_imports, peak_imports = tracemalloc.get_traced_memory()
print(f"Memori puncak setelah impor: {peak_imports / (1024*1024):.2f} MB", file=sys.stderr)


# 4. Muat model dan scaler (langkah berat kedua)
print("Memuat model dan scaler...", file=sys.stderr)
model, scaler = load_model_and_scaler()

if model is None or scaler is None:
    print("Gagal memuat model atau scaler.", file=sys.stderr)
    tracemalloc.stop()
    sys.exit(1)

model_load_time = time.time()
print(f"Model dimuat. (Waktu: {model_load_time - lib_import_time:.2f}s)", file=sys.stderr)

# 5. Ambil snapshot memori setelah model dimuat ("Warm Start")
# Ini adalah memori yang akan digunakan jika fungsi Vercel tetap "hangat"
snap_after_load = tracemalloc.take_snapshot()
current_load, peak_load = tracemalloc.get_traced_memory()
print(f"Memori puncak setelah model dimuat: {peak_load / (1024*1024):.2f} MB", file=sys.stderr)


# 6. Jalankan satu prediksi (untuk mensimulasikan pemanggilan API)
print("Menjalankan 1x prediksi...", file=sys.stderr)

# Gunakan data dummy yang sama dari log Anda
input_data = {
  "Age": 30, "DistanceFromHome": 10, "MonthlyIncome": 5000, "YearsAtCompany": 5,
  "JobLevel": 2, "OverTime": "No", "JobSatisfaction": 3, "WorkLifeBalance": 3,
  "Department": "Research & Development", "EducationField": "Life Sciences",
  "MaritalStatus": "Single", "EmployeeNumber": 1, "DailyRate": 800, "Education": 3,
  "EnvironmentSatisfaction": 3, "HourlyRate": 50, "JobInvolvement": 3,
  "MonthlyRate": 15000, "NumCompaniesWorked": 1, "PercentSalaryHike": 15,
  "PerformanceRating": 3, "RelationshipSatisfaction": 3, "StockOptionLevel": 0,
  "TotalWorkingYears": 10, "TrainingTimesLastYear": 2, "YearsInCurrentRole": 3,
  "YearsSinceLastPromotion": 1, "YearsWithCurrManager": 2, "BusinessTravel": "Travel_Rarely",
  "Gender": "Male", "JobRole": "Sales Executive", "EmployeeCount": 1, "StandardHours": 80
}

try:
    processed_data = preprocess_input_data(input_data)
    scaled_data = scaler.transform(processed_data)
    prediction = model.predict(scaled_data)
    prediction_proba = model.predict_proba(scaled_data)
except Exception as e:
    print(f"Error saat prediksi: {e}", file=sys.stderr)

predict_time = time.time()
print(f"Prediksi selesai. (Waktu: {predict_time - model_load_time:.2f}s)", file=sys.stderr)

# 7. Dapatkan hasil akhir dan hentikan pelacakan
current_final, peak_final = tracemalloc.get_traced_memory()
tracemalloc.stop()

total_time = time.time() - start_time

# 8. Cetak laporan akhir
print("\n--- 📊 Laporan Memori Puncak ---")
print(f"Total Waktu Eksekusi   : {total_time:.2f} detik")
print("---------------------------------------")
print(f"Puncak (Hanya Impor)     : {peak_imports / (1024*1024):.2f} MB")
print(f"Puncak (Impor + Model)   : {peak_load / (1024*1024):.2f} MB")
print(f"PUNCAK TOTAL (Total Run) : {peak_final / (1024*1024):.2f} MB")
print("---------------------------------------")
print(f"\n💡 Angka 'PUNCAK TOTAL' ({peak_final / (1024*1024):.2f} MB) adalah yang perlu Anda bandingkan")
print("dengan batas memori Vercel (1024 MB untuk Hobby).")