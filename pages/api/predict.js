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
  console.log('Request headers:', req.headers);
  console.log('Request body type:', typeof req.body);
  console.log('Request body:', req.body);
  
  if (req.method !== 'POST') {
    console.log('Method not allowed - returning 405');
    return res.status(405).json({ 
      success: false, 
      error: 'Method not allowed. Use POST.',
      received_method: req.method,
      debug_info: {
        headers: req.headers,
        body: req.body
      }
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

    // --- TRY TO CALL PYTHON API FIRST ---
    
    try {
      // Try to call the Python API
      console.log('Attempting to call Python API...');
      
      const pythonApiUrl = `/api/python/predict`;
      console.log('Calling Python ML API at:', pythonApiUrl);

      const response = await fetch(`${req.headers.origin || 'https://dashboard-business-attrition-vercel-lilac.vercel.app'}${pythonApiUrl}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(inputData)
      });

      if (response.ok) {
        const result = await response.json();
        console.log('Python API response:', result);

        if (result.success) {
          // Success! Return result from Python ML API
          return res.status(200).json({
            ...result,
            note: 'Prediction from Python ML API'
          });
        } else {
          console.error('Python ML model returned error:', result.error);
          // Fall through to rule-based logic below
        }
      } else {
        const errorText = await response.text();
        console.error('Python API failed:', response.status, errorText);
        // Fall through to rule-based logic below
      }

    } catch (fetchError) {
      console.error('Error calling Python API:', fetchError);
      // Fall through to rule-based logic below
    }

    // --- FALLBACK TO RULE-BASED LOGIC ---
    
    console.log('Using integrated rule-based prediction logic');
    
    // Simple rule-based prediction (same logic as Python API)
    let riskScore = 0.0;
    
    const age = inputData.Age || 30;
    const income = inputData.MonthlyIncome || 5000;
    const overtime = inputData.OverTime || 'No';
    const distance = inputData.DistanceFromHome || 5;
    const jobSatisfaction = inputData.JobSatisfaction || 3;
    const workLifeBalance = inputData.WorkLifeBalance || 3;
    const yearsAtCompany = inputData.YearsAtCompany || 5;
    
    // Apply scoring rules
    if (age < 25 || age > 55) riskScore += 0.3;
    if (income < 3000) riskScore += 0.4;
    if (overtime === 'Yes') riskScore += 0.3;
    if (distance > 20) riskScore += 0.15;
    if (jobSatisfaction <= 2) riskScore += 0.3;
    if (workLifeBalance <= 2) riskScore += 0.25;
    if (yearsAtCompany < 1 || yearsAtCompany > 20) riskScore += 0.15;
    
    const probability = Math.min(riskScore, 0.9);
    const prediction = probability > 0.5 ? 1 : 0;
    
    const result = {
      success: true,
      prediction: prediction,
      prediction_label: prediction === 1 ? "Will Leave" : "Will Stay",
      probability: {
        will_stay: 1 - probability,
        will_leave: probability
      },
      risk_level: probability > 0.7 ? "High" : probability > 0.4 ? "Medium" : "Low",
      confidence: Math.max(probability, 1 - probability),
      model_type: "Integrated Rule-Based Model",
      feature_importance: {
        "Monthly Income": income < 3000 ? 0.4 : 0,
        "Age": (age < 25 || age > 55) ? 0.3 : 0,
        "Over Time": overtime === 'Yes' ? 0.3 : 0,
        "Job Satisfaction": jobSatisfaction <= 2 ? 0.3 : 0,
        "Work Life Balance": workLifeBalance <= 2 ? 0.25 : 0,
        "Distance From Home": distance > 20 ? 0.15 : 0,
        "Years At Company": (yearsAtCompany < 1 || yearsAtCompany > 20) ? 0.15 : 0
      }
    };
    
    console.log('Generated prediction result:', result);
    return res.status(200).json(result);

  } catch (error) {
    // Handle any errors with validation or processing
    console.error('API error in predict.js:', error);
    console.error('With input data:', inputData);
    
    // Fallback ke mock prediction jika terjadi error
    const mockResult = generateMockPrediction(req.body || {});
    return res.status(200).json({
      ...mockResult,
      note: 'Using fallback prediction due to internal server error',
      error_details: error.message
    });
  }
}