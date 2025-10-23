// Hapus 'spawn' dan 'path' karena tidak lagi digunakan
// import { spawn } from 'child_process'
// import path from 'path'

// Fungsi fallback Anda (generateMockPrediction) tetap sama, tidak perlu diubah
function generateMockPrediction(inputData) {
  console.log('Generating mock prediction for:', inputData)
  
  let riskScore = 0;
  
  // Age factor
  if (inputData.Age && (inputData.Age < 25 || inputData.Age > 55)) riskScore += 0.2;
  
  // Distance factor
  if (inputData.DistanceFromHome && inputData.DistanceFromHome > 20) riskScore += 0.15;
  
  // Income factor
  if (inputData.MonthlyIncome && inputData.MonthlyIncome < 3000) riskScore += 0.25;
  
  // Overtime factor
  if (inputData.OverTime === 'Yes') riskScore += 0.2;
  
  // Job satisfaction factor
  if (inputData.JobSatisfaction && inputData.JobSatisfaction <= 2) riskScore += 0.3;
  
  // Work-life balance factor
  if (inputData.WorkLifeBalance && inputData.WorkLifeBalance <= 2) riskScore += 0.25;
  
  // Years at company factor (too short or too long)
  if (inputData.YearsAtCompany && (inputData.YearsAtCompany < 1 || inputData.YearsAtCompany > 20)) riskScore += 0.15;
  
  const probability = Math.min(riskScore, 0.95);
  const prediction = probability > 0.5 ? 1 : 0;
  
  const riskLevel = probability > 0.7 ? "High" : probability > 0.4 ? "Medium" : "Low";
  
  return {
    success: true,
    prediction: prediction,
    prediction_label: prediction === 1 ? "Will Leave" : "Will Stay",
    probability: {
      will_stay: 1 - probability,
      will_leave: probability
    },
    risk_level: riskLevel,
    confidence: Math.max(probability, 1 - probability),
    model_type: "Rule-Based Fallback Model",
    feature_importance: {
      "Job Satisfaction": inputData.JobSatisfaction <= 2 ? 0.3 : 0,
      "Work Life Balance": inputData.WorkLifeBalance <= 2 ? 0.25 : 0,
      "Monthly Income": inputData.MonthlyIncome < 3000 ? 0.25 : 0,
      "Over Time": inputData.OverTime === 'Yes' ? 0.2 : 0,
      "Age": (inputData.Age < 25 || inputData.Age > 55) ? 0.2 : 0,
      "Distance From Home": inputData.DistanceFromHome > 20 ? 0.15 : 0
    }
  };
}


// --- INI ADALAH HANDLER API YANG BARU ---
export default async function handler(req, res) {
  console.log('API predict (Node.js) called with method:', req.method);
  
  if (req.method !== 'POST') {
    return res.status(405).json({ 
      success: false, 
      error: 'Method not allowed. Use POST.' 
    });
  }

  try {
    const inputData = req.body;
    console.log('Input data received:', inputData);

    // Validasi inputData Anda tetap di sini
    const requiredFields = ['Age', 'DistanceFromHome', 'MonthlyIncome', 'YearsAtCompany'];
    for (const field of requiredFields) {
      if (!(field in inputData) || inputData[field] === '' || inputData[field] === null) {
        return res.status(400).json({
          success: false,
          error: `Missing required field: ${field}`
        });
      }
    }

    // --- PERUBAHAN UTAMA: HAPUS SPAWN, GUNAKAN FETCH ---

    // Tentukan URL untuk memanggil API Python
    // Prioritaskan environment variables Vercel
    const host = process.env.VERCEL_URL 
      ? `https://${process.env.VERCEL_URL}`
      : process.env.NEXT_PUBLIC_VERCEL_URL
        ? `https://${process.env.NEXT_PUBLIC_VERCEL_URL}`
        : 'http://localhost:3000'; // Untuk local development
    
    // Ini akan memanggil function di api/python/predict.py
    const pythonApiUrl = `${host}/api/python/predict`;
    console.log('Calling Python ML API at:', pythonApiUrl);

    const response = await fetch(pythonApiUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(inputData),
      timeout: 30000, // Tambahkan timeout 30 detik
    });

    if (!response.ok) {
      // Jika API Python gagal, catat error dan gunakan fallback
      const errorText = await response.text();
      console.error('Python API failed:', response.status, errorText);
      throw new Error(`Python API responded with ${response.status}: ${errorText}`);
    }

    // Dapatkan hasil JSON dari API Python
    const result = await response.json();
    console.log('Parsed result from Python API:', result);

    if (result.success) {
      // Sukses! Kembalikan hasil dari model ML
      return res.status(200).json(result);
    } else {
      // Model ML mengembalikan error, gunakan fallback
      console.error('Python ML model returned error:', result.error);
      const mockResult = generateMockPrediction(inputData);
      return res.status(200).json({
        ...mockResult,
        note: 'Using fallback prediction due to ML model execution error',
        model_error: result.error || 'Unknown error from Python'
      });
    }

  } catch (error) {
    // Ini menangkap error 'fetch' (mis. timeout, 500) atau error validasi
    console.error('API error in predict.js:', error);
    
    // Fallback ke mock prediction jika terjadi error
    const mockResult = generateMockPrediction(req.body || {});
    return res.status(200).json({
      ...mockResult,
      note: 'Using fallback prediction due to internal server error',
      error_details: error.message
    });
  }
}