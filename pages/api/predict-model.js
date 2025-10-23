import { spawn } from 'child_process';
import path from 'path';

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ message: 'Method not allowed' });
  }

  try {
    const inputData = req.body;
    
    // Validate required fields
    const requiredFields = ['Age', 'DistanceFromHome', 'MonthlyIncome', 'YearsAtCompany'];
    for (const field of requiredFields) {
      if (!(field in inputData) || inputData[field] === '' || inputData[field] === null) {
        return res.status(400).json({
          success: false,
          message: `Missing required field: ${field}`
        });
      }
    }
    
    // Path to Python script
    const scriptPath = path.join(process.cwd(), 'scripts', 'predict_with_model.py');
    
    // Use the virtual environment Python executable
    const pythonExe = path.join(process.cwd(), '.venv', 'Scripts', 'python.exe');
    
    console.log('Script path:', scriptPath);
    console.log('Python executable:', pythonExe);
    console.log('Input data:', JSON.stringify(inputData, null, 2));
    
    // Run Python script
    const pythonProcess = spawn(pythonExe, [scriptPath, JSON.stringify(inputData)]);
    
    let result = '';
    let error = '';

    pythonProcess.stdout.on('data', (data) => {
      result += data.toString();
    });

    pythonProcess.stderr.on('data', (data) => {
      error += data.toString();
    });

    pythonProcess.on('close', (code) => {
      if (code !== 0) {
        console.error('Python script error:', error);
        return res.status(500).json({ 
          success: false, 
          message: 'Model prediction failed',
          error: error,
          fallback: 'Please check if Python and required packages are installed'
        });
      }

      try {
        const prediction = JSON.parse(result);
        res.status(200).json(prediction);
      } catch (parseError) {
        console.error('Parse error:', parseError);
        res.status(500).json({
          success: false,
          message: 'Failed to parse prediction result',
          rawResult: result
        });
      }
    });

  } catch (error) {
    console.error('API error:', error);
    res.status(500).json({
      success: false,
      message: 'Internal server error',
      error: error.message
    });
  }
}

export const config = {
  api: {
    bodyParser: {
      sizeLimit: '1mb',
    },
  },
}