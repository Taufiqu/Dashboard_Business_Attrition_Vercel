import React, { useState } from 'react'
import { Calculator, TrendingUp, AlertTriangle, CheckCircle } from 'lucide-react'

const PredictionForm = () => {
  const [formData, setFormData] = useState({
    Age: '',
    DistanceFromHome: '',
    MonthlyIncome: '',
    YearsAtCompany: '',
    JobLevel: '',
    OverTime: 'No',
    JobSatisfaction: '',
    WorkLifeBalance: '',
    Department: 'Research & Development',
    EducationField: 'Life Sciences',
    MaritalStatus: 'Single'
  })
  
  const [prediction, setPrediction] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  // Consistent input styling
  const inputClassName = "w-full p-3 border border-gray-300 rounded-lg bg-white text-gray-900 placeholder-gray-500 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 focus:outline-none transition-colors"
  const selectClassName = "w-full p-3 border border-gray-300 rounded-lg bg-white text-gray-900 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 focus:outline-none transition-colors"
  const labelClassName = "block text-sm font-semibold text-gray-700 mb-2"

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: value
    }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError(null)
    setPrediction(null)

    try {
      const response = await fetch('/api/predict', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData)
      })

      const result = await response.json()

      if (result.success) {
        setPrediction(result)
      } else {
        setError(result.error || 'Prediction failed')
      }
    } catch (err) {
      setError('Network error: ' + err.message)
    } finally {
      setLoading(false)
    }
  }

  const getRiskLevel = (probability) => {
    if (probability > 0.7) return { level: 'High', color: 'text-red-600', icon: AlertTriangle }
    if (probability > 0.4) return { level: 'Medium', color: 'text-yellow-600', icon: TrendingUp }
    return { level: 'Low', color: 'text-green-600', icon: CheckCircle }
  }

  return (
    <div className="bg-white p-8 rounded-xl shadow-lg border border-gray-100">
      <div className="flex items-center mb-8">
        <Calculator className="w-7 h-7 text-blue-600 mr-3" />
        <h2 className="text-2xl font-bold text-gray-800">Attrition Risk Prediction</h2>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label className={labelClassName}>
              Age
            </label>
            <input
              type="number"
              name="Age"
              value={formData.Age}
              onChange={handleChange}
              className={inputClassName}
              placeholder="Enter age (e.g., 30)"
              required
            />
          </div>

          <div>
            <label className={labelClassName}>
              Distance From Home (km)
            </label>
            <input
              type="number"
              name="DistanceFromHome"
              value={formData.DistanceFromHome}
              onChange={handleChange}
              className={inputClassName}
              placeholder="Enter distance (e.g., 15)"
              required
            />
          </div>

          <div>
            <label className={labelClassName}>
              Monthly Income
            </label>
            <input
              type="number"
              name="MonthlyIncome"
              value={formData.MonthlyIncome}
              onChange={handleChange}
              className={inputClassName}
              placeholder="Enter monthly income (e.g., 5000)"
              required
            />
          </div>

          <div>
            <label className={labelClassName}>
              Years at Company
            </label>
            <input
              type="number"
              name="YearsAtCompany"
              value={formData.YearsAtCompany}
              onChange={handleChange}
              className={inputClassName}
              placeholder="Enter years (e.g., 3)"
              required
            />
          </div>

          <div>
            <label className={labelClassName}>
              Job Level
            </label>
            <select
              name="JobLevel"
              value={formData.JobLevel}
              onChange={handleChange}
              className={selectClassName}
              required
            >
              <option value="">Select Job Level</option>
              <option value="1">Level 1 - Entry</option>
              <option value="2">Level 2 - Junior</option>
              <option value="3">Level 3 - Senior</option>
              <option value="4">Level 4 - Lead</option>
              <option value="5">Level 5 - Manager</option>
            </select>
          </div>

          <div>
            <label className={labelClassName}>
              Over Time
            </label>
            <select
              name="OverTime"
              value={formData.OverTime}
              onChange={handleChange}
              className={selectClassName}
            >
              <option value="No">No</option>
              <option value="Yes">Yes</option>
            </select>
          </div>

          <div>
            <label className={labelClassName}>
              Job Satisfaction (1-4)
            </label>
            <select
              name="JobSatisfaction"
              value={formData.JobSatisfaction}
              onChange={handleChange}
              className={selectClassName}
              required
            >
              <option value="">Select Satisfaction Level</option>
              <option value="1">1 - Low</option>
              <option value="2">2 - Medium</option>
              <option value="3">3 - High</option>
              <option value="4">4 - Very High</option>
            </select>
          </div>

          <div>
            <label className={labelClassName}>
              Work Life Balance (1-4)
            </label>
            <select
              name="WorkLifeBalance"
              value={formData.WorkLifeBalance}
              onChange={handleChange}
              className={selectClassName}
              required
            >
              <option value="">Select Balance Level</option>
              <option value="1">1 - Bad</option>
              <option value="2">2 - Good</option>
              <option value="3">3 - Better</option>
              <option value="4">4 - Best</option>
            </select>
          </div>

          <div>
            <label className={labelClassName}>
              Department
            </label>
            <select
              name="Department"
              value={formData.Department}
              onChange={handleChange}
              className={selectClassName}
            >
              <option value="Research & Development">Research & Development</option>
              <option value="Sales">Sales</option>
              <option value="Human Resources">Human Resources</option>
            </select>
          </div>

          <div>
            <label className={labelClassName}>
              Education Field
            </label>
            <select
              name="EducationField"
              value={formData.EducationField}
              onChange={handleChange}
              className={selectClassName}
            >
              <option value="Life Sciences">Life Sciences</option>
              <option value="Medical">Medical</option>
              <option value="Marketing">Marketing</option>
              <option value="Technical Degree">Technical Degree</option>
              <option value="Other">Other</option>
              <option value="Human Resources">Human Resources</option>
            </select>
          </div>

          <div>
            <label className={labelClassName}>
              Marital Status
            </label>
            <select
              name="MaritalStatus"
              value={formData.MaritalStatus}
              onChange={handleChange}
              className={selectClassName}
            >
              <option value="Single">Single</option>
              <option value="Married">Married</option>
              <option value="Divorced">Divorced</option>
            </select>
          </div>
        </div>

        <div className="pt-4">
          <button
            type="submit"
            disabled={loading}
            className="w-full bg-gradient-to-r from-blue-600 to-blue-700 text-white py-4 px-6 rounded-lg hover:from-blue-700 hover:to-blue-800 focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 font-semibold text-lg shadow-lg"
          >
            {loading ? (
              <div className="flex items-center justify-center">
                <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-white mr-3"></div>
                Predicting...
              </div>
            ) : (
              'Predict Attrition Risk'
            )}
          </button>
        </div>
      </form>

      {error && (
        <div className="mt-6 p-4 bg-red-50 border border-red-200 text-red-700 rounded-lg">
          <div className="flex items-center">
            <AlertTriangle className="w-5 h-5 mr-2" />
            <strong>Error:</strong>
          </div>
          <p className="mt-1">{error}</p>
        </div>
      )}

      {prediction && prediction.success && (
        <div className="mt-8 p-6 bg-gray-50 rounded-xl border border-gray-200">
          <h3 className="text-xl font-bold text-gray-800 mb-4">Prediction Result</h3>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="bg-white p-6 rounded-lg border border-gray-200 shadow-sm">
              <div className="flex items-center mb-3">
                {(() => {
                  const risk = getRiskLevel(prediction.attrition_probability)
                  const IconComponent = risk.icon
                  return (
                    <>
                      <IconComponent className={`w-6 h-6 ${risk.color} mr-3`} />
                      <span className={`font-bold text-lg ${risk.color}`}>
                        {risk.level} Risk
                      </span>
                    </>
                  )
                })()}
              </div>
              <p className="text-3xl font-bold text-gray-800 mb-1">
                {(prediction.attrition_probability * 100).toFixed(1)}%
              </p>
              <p className="text-gray-600">Attrition Probability</p>
            </div>

            <div className="bg-white p-6 rounded-lg border border-gray-200 shadow-sm">
              <h4 className="font-bold text-gray-800 mb-3">Prediction Details</h4>
              <div className="space-y-2 text-sm">
                <p>
                  <span className="font-medium text-gray-700">Model:</span> 
                  <span className="text-gray-600 ml-2">{prediction.model_info?.name || 'Unknown'}</span>
                </p>
                <p>
                  <span className="font-medium text-gray-700">Version:</span> 
                  <span className="text-gray-600 ml-2">{prediction.model_info?.version || 'Unknown'}</span>
                </p>
                <p>
                  <span className="font-medium text-gray-700">Prediction:</span> 
                  <span className={`ml-2 font-medium ${prediction.prediction === 1 ? 'text-red-600' : 'text-green-600'}`}>
                    {prediction.prediction === 1 ? 'Will Leave' : 'Will Stay'}
                  </span>
                </p>
              </div>
            </div>
          </div>

          {prediction.feature_importance && (
            <div className="mt-6 bg-white p-6 rounded-lg border border-gray-200 shadow-sm">
              <h4 className="font-bold text-gray-800 mb-4">Key Contributing Factors</h4>
              <div className="space-y-3">
                {Object.entries(prediction.feature_importance)
                  .sort(([,a], [,b]) => Math.abs(b) - Math.abs(a))
                  .slice(0, 5)
                  .map(([feature, importance]) => (
                    <div key={feature} className="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
                      <span className="font-medium text-gray-700">{feature}</span>
                      <span className={`font-bold px-3 py-1 rounded-full text-sm ${
                        importance > 0 ? 'bg-red-100 text-red-700' : 'bg-green-100 text-green-700'
                      }`}>
                        {importance > 0 ? '+' : ''}{(importance * 100).toFixed(1)}%
                      </span>
                    </div>
                  ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

export default PredictionForm