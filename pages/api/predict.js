import { spawn } from 'child_process'
import path from 'path'

export default async function handler(req, res) {
  console.log('API predict called with method:', req.method)
  
  if (req.method !== 'POST') {
    return res.status(405).json({ 
      success: false, 
      error: 'Method not allowed. Use POST.' 
    })
  }

  try {
    const inputData = req.body
    console.log('Input data received:', inputData)

    // Validate input data
    if (!inputData || typeof inputData !== 'object') {
      console.log('Invalid input data')
      return res.status(400).json({
        success: false,
        error: 'Invalid input data. Expected JSON object.'
      })
    }

    // Validate required fields
    const requiredFields = ['Age', 'DistanceFromHome', 'MonthlyIncome', 'YearsAtCompany']
    for (const field of requiredFields) {
      if (!(field in inputData) || inputData[field] === '' || inputData[field] === null) {
        return res.status(400).json({
          success: false,
          error: `Missing required field: ${field}`
        })
      }
    }

    // Path to Python script - use predict_with_model.py
    const scriptPath = path.join(process.cwd(), 'scripts', 'predict_with_model.py')
    console.log('Script path:', scriptPath)
    
    // Use the virtual environment Python executable
    const pythonExe = path.join(process.cwd(), '.venv', 'Scripts', 'python.exe')
    
    // Spawn Python process
    const python = spawn(pythonExe, [scriptPath, JSON.stringify(inputData)], {
      cwd: process.cwd(),
      stdio: ['pipe', 'pipe', 'pipe']
    })

    let stdout = ''
    let stderr = ''

    // Collect stdout
    python.stdout.on('data', (data) => {
      stdout += data.toString()
    })

    // Collect stderr
    python.stderr.on('data', (data) => {
      stderr += data.toString()
    })

    // Handle process completion
    python.on('close', (code) => {
      console.log('Python script finished with code:', code)
      console.log('Stdout:', stdout)
      if (stderr) console.log('Stderr:', stderr)
      
      if (code === 0) {
        try {
          // Clean up stdout - remove any extra characters
          const cleanOutput = stdout.trim()
          console.log('Clean output:', cleanOutput)
          
          const result = JSON.parse(cleanOutput)
          console.log('Parsed result:', result)
          
          return res.status(200).json(result)
        } catch (parseError) {
          console.error('Parse error:', parseError)
          console.log('Falling back to mock prediction due to parse error')
          
          // Fallback to mock prediction
          const mockResult = generateMockPrediction(inputData)
          return res.status(200).json({
            ...mockResult,
            note: 'Using fallback prediction due to ML model parse error'
          })
        }
      } else {
        console.log('Python script failed, falling back to mock prediction')
        
        // Fallback to mock prediction
        const mockResult = generateMockPrediction(inputData)
        return res.status(200).json({
          ...mockResult,
          note: 'Using fallback prediction due to ML model execution error',
          model_error: stderr || stdout
        })
      }
    })

    // Handle process error
    python.on('error', (error) => {
      console.error('Python process error:', error)
      console.log('Falling back to mock prediction due to process error')
      
      // Fallback to mock prediction
      const mockResult = generateMockPrediction(inputData)
      return res.status(200).json({
        ...mockResult,
        note: 'Using fallback prediction due to Python process error'
      })
    })

    // Set timeout (30 seconds)
    const timeoutId = setTimeout(() => {
      python.kill()
      console.log('Python process timeout, falling back to mock prediction')
      
      // Fallback to mock prediction
      const mockResult = generateMockPrediction(inputData)
      return res.status(200).json({
        ...mockResult,
        note: 'Using fallback prediction due to timeout'
      })
    }, 30000)

    // Clear timeout when process completes
    python.on('close', () => {
      clearTimeout(timeoutId)
    })

  } catch (error) {
    console.error('API error:', error)
    console.log('Falling back to mock prediction due to API error')
    
    // Fallback to mock prediction
    const mockResult = generateMockPrediction(req.body || {})
    return res.status(200).json({
      ...mockResult,
      note: 'Using fallback prediction due to internal server error'
    })
  }
}

// Mock prediction function as fallback
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