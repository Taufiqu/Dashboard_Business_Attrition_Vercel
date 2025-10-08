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

    // Write input to temporary file to avoid JSON parsing issues in Windows
    const fs = require('fs')
    const tempFile = path.join(process.cwd(), 'temp_input.json')
    fs.writeFileSync(tempFile, JSON.stringify(inputData))
    
    // Path to Python script
    const scriptPath = path.join(process.cwd(), 'scripts', 'predict_real.py')
    console.log('Script path:', scriptPath)
    
    // Spawn Python process with temp file
    const python = spawn('python', [scriptPath, '--file', tempFile], {
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
      console.log('Stderr:', stderr)
      
      // Clean up temp file
      try {
        const fs = require('fs')
        fs.unlinkSync(tempFile)
      } catch (e) {
        console.log('Temp file cleanup failed:', e.message)
      }
      
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
          return res.status(500).json({
            success: false,
            error: 'Failed to parse prediction result',
            details: stdout,
            stderr: stderr
          })
        }
      } else {
        return res.status(500).json({
          success: false,
          error: 'Python script execution failed',
          details: stderr || stdout,
          exit_code: code
        })
      }
    })

    // Handle process error
    python.on('error', (error) => {
      console.error('Python process error:', error)
      return res.status(500).json({
        success: false,
        error: 'Failed to start Python process',
        details: error.message
      })
    })

    // Set timeout (30 seconds)
    const timeoutId = setTimeout(() => {
      python.kill()
      return res.status(500).json({
        success: false,
        error: 'Prediction timeout (30 seconds)'
      })
    }, 30000)

    // Clear timeout when process completes
    python.on('close', () => {
      clearTimeout(timeoutId)
    })

  } catch (error) {
    console.error('API error:', error)
    return res.status(500).json({
      success: false,
      error: 'Internal server error',
      details: error instanceof Error ? error.message : 'Unknown error'
    })
  }
}