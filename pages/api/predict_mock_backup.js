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

    // For now, return a mock prediction to test the UI
    const mockPrediction = {
      success: true,
      prediction: Math.random() > 0.5 ? 1 : 0,
      attrition_probability: Math.random() * 0.8 + 0.1, // Random between 0.1 and 0.9
      model_info: {
        name: 'Mock Random Forest',
        version: '1.0',
        type: 'RandomForestClassifier'
      },
      feature_importance: {
        Age: Math.random() * 0.2,
        DistanceFromHome: Math.random() * 0.15,
        MonthlyIncome: Math.random() * 0.25,
        YearsAtCompany: Math.random() * 0.2,
        JobLevel: Math.random() * 0.15,
        OverTime: Math.random() * 0.1,
        JobSatisfaction: Math.random() * 0.2,
        WorkLifeBalance: Math.random() * 0.15
      },
      input_data: inputData
    }

    console.log('Sending mock prediction:', mockPrediction)
    return res.status(200).json(mockPrediction)

  } catch (error) {
    console.error('API error:', error)
    return res.status(500).json({
      success: false,
      error: 'Internal server error',
      details: error instanceof Error ? error.message : 'Unknown error'
    })
  }
}