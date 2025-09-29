import fs from 'fs'
import path from 'path'

export default function handler(req, res) {
  try {
    // Read CSV file
    const filePath = path.join(process.cwd(), 'public', 'data', 'hasil_output_DSP (2).csv')
    const csvData = fs.readFileSync(filePath, 'utf8')
    
    // Parse CSV data
    const lines = csvData.trim().split('\n')
    const headers = lines[0].split(',')
    const data = lines.slice(1).map(line => {
      const values = line.split(',')
      const obj = {}
      headers.forEach((header, index) => {
        obj[header.trim()] = values[index] ? values[index].trim() : ''
      })
      return obj
    })

    // Calculate metrics
    const totalEmployees = data.length
    
    // Calculate attrition rate (using Final_Attrition column)
    const attritionCount = data.filter(emp => 
      emp.Final_Attrition === '1.0' || emp.Attrition === '1.0'
    ).length
    const attritionRate = ((attritionCount / totalEmployees) * 100).toFixed(1)
    
    // Calculate average age
    const validAges = data.filter(emp => emp.Age && emp.Age !== '').map(emp => parseFloat(emp.Age))
    const avgAge = validAges.length > 0 ? (validAges.reduce((sum, age) => sum + age, 0) / validAges.length).toFixed(1) : 0
    
    // Calculate average tenure (YearsAtCompany)
    const validTenure = data.filter(emp => emp.YearsAtCompany && emp.YearsAtCompany !== '')
      .map(emp => parseFloat(emp.YearsAtCompany))
    const avgTenure = validTenure.length > 0 ? (validTenure.reduce((sum, years) => sum + years, 0) / validTenure.length).toFixed(1) : 0
    
    // Calculate at-risk employees (high performers with low satisfaction)
    const atRiskEmployees = data.filter(emp => {
      const envSat = parseFloat(emp.EnvironmentSatisfaction || 0)
      const jobSat = parseFloat(emp.JobSatisfaction || 0)
      const workLifeBal = parseFloat(emp.WorkLifeBalance || 0)
      return (envSat <= 2 || jobSat <= 2 || workLifeBal <= 2) && emp.OverTime === 'Yes'
    }).length

    // Department with highest attrition
    const deptAttrition = {}
    data.forEach(emp => {
      const dept = emp.Department || 'Unknown'
      if (!deptAttrition[dept]) {
        deptAttrition[dept] = { total: 0, attrition: 0 }
      }
      deptAttrition[dept].total++
      if (emp.Final_Attrition === '1.0' || emp.Attrition === '1.0') {
        deptAttrition[dept].attrition++
      }
    })

    let highestAttritionDept = { name: 'Unknown', rate: 0 }
    Object.keys(deptAttrition).forEach(dept => {
      const rate = (deptAttrition[dept].attrition / deptAttrition[dept].total) * 100
      if (rate > highestAttritionDept.rate) {
        highestAttritionDept = { name: dept, rate: rate.toFixed(1) }
      }
    })

    // Key risk factors analysis
    const overTimeAttrition = data.filter(emp => emp.OverTime === 'Yes' && (emp.Final_Attrition === '1.0' || emp.Attrition === '1.0')).length
    const totalOverTime = data.filter(emp => emp.OverTime === 'Yes').length
    const overTimeAttritionRate = totalOverTime > 0 ? ((overTimeAttrition / totalOverTime) * 100).toFixed(1) : 0

    // Response data
    const analytics = {
      totalEmployees,
      attritionRate: parseFloat(attritionRate),
      atRiskEmployees,
      avgTenure: parseFloat(avgTenure),
      avgAge: parseFloat(avgAge),
      highestAttritionDept,
      keyInsights: {
        overTimeImpact: overTimeAttritionRate,
        totalAttrition: attritionCount,
        departmentBreakdown: deptAttrition
      }
    }

    res.status(200).json(analytics)
  } catch (error) {
    console.error('Error processing data:', error)
    res.status(500).json({ error: 'Failed to process data' })
  }
}