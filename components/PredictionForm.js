import React, { useState } from 'react'
import { Calculator, TrendingUp, AlertTriangle, CheckCircle, Brain, Cog, User, Briefcase, DollarSign, Clock } from 'lucide-react'

const PredictionForm = () => {
  const [formData, setFormData] = useState({
    // Essential fields - Required
    Age: '30',
    DistanceFromHome: '10',
    MonthlyIncome: '5000',
    YearsAtCompany: '5',
    JobLevel: '2',
    OverTime: 'No',
    JobSatisfaction: '3',
    WorkLifeBalance: '3',
    Department: 'Research & Development',
    EducationField: 'Life Sciences',
    MaritalStatus: 'Single',
    
    // Additional fields for ML model with defaults
    DailyRate: '800',
    Education: '3',
    EmployeeNumber: '1',
    EnvironmentSatisfaction: '3',
    HourlyRate: '50',
    JobInvolvement: '3',
    MonthlyRate: '15000',
    NumCompaniesWorked: '1',
    PercentSalaryHike: '15',
    PerformanceRating: '3',
    RelationshipSatisfaction: '3',
    StockOptionLevel: '0',
    TotalWorkingYears: '10',
    TrainingTimesLastYear: '2',
    YearsInCurrentRole: '3',
    YearsSinceLastPromotion: '1',
    YearsWithCurrManager: '2',
    BusinessTravel: 'Travel_Rarely',
    Gender: 'Male',
    JobRole: 'Sales Executive'
  })
  
  const [prediction, setPrediction] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [showAdvanced, setShowAdvanced] = useState(false)

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
      // Prepare data for API
      const processedData = { ...formData }
      
      // Convert string inputs to numbers for numerical fields
      const numericalFields = [
        'Age', 'DailyRate', 'DistanceFromHome', 'Education', 'EmployeeNumber',
        'EnvironmentSatisfaction', 'HourlyRate', 'JobInvolvement', 'JobLevel',
        'JobSatisfaction', 'MonthlyIncome', 'MonthlyRate', 'NumCompaniesWorked',
        'PercentSalaryHike', 'PerformanceRating', 'RelationshipSatisfaction',
        'StockOptionLevel', 'TotalWorkingYears', 'TrainingTimesLastYear',
        'WorkLifeBalance', 'YearsAtCompany', 'YearsInCurrentRole',
        'YearsSinceLastPromotion', 'YearsWithCurrManager'
      ]

      numericalFields.forEach(field => {
        if (processedData[field] !== '' && processedData[field] !== null) {
          processedData[field] = parseFloat(processedData[field]) || 0
        }
      })

      // Set default values for required ML model fields
      processedData.EmployeeCount = 1;
      processedData.StandardHours = 80;

      // Set default EmployeeId if not provided
      if (!processedData.EmployeeId && !processedData.EmployeeNumber) {
        processedData.EmployeeNumber = Math.floor(Math.random() * 10000) + 1;
      }
      
      // Calculate derived fields if not provided
      if (!processedData.TotalWorkingYears || processedData.TotalWorkingYears === 0) {
        processedData.TotalWorkingYears = Math.max(processedData.YearsAtCompany || 0, (processedData.Age || 25) - 18)
      }
      if (!processedData.YearsInCurrentRole || processedData.YearsInCurrentRole === 0) {
        processedData.YearsInCurrentRole = Math.min(processedData.YearsAtCompany || 0, 5)
      }
      if (!processedData.YearsWithCurrManager || processedData.YearsWithCurrManager === 0) {
        processedData.YearsWithCurrManager = Math.min(processedData.YearsAtCompany || 0, 3)
      }

      const response = await fetch('/api/predict', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(processedData)
      })

      const result = await response.json()

      if (result.success !== false) {
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
      <div className="flex items-center justify-between mb-8">
        <div className="flex items-center">
          <Calculator className="w-7 h-7 text-blue-600 mr-3" />
          <h2 className="text-2xl font-bold text-gray-800">Employee Attrition Risk Prediction</h2>
        </div>
        
        <button
          type="button"
          onClick={() => setShowAdvanced(!showAdvanced)}
          className="flex items-center space-x-2 px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200 transition-colors"
        >
          <Cog className="w-4 h-4" />
          <span>{showAdvanced ? 'Simple View' : 'Advanced View'}</span>
        </button>
      </div>

      <form onSubmit={handleSubmit} className="space-y-8">
        {/* Essential Employee Information */}
        <div className="bg-gradient-to-r from-blue-50 to-indigo-50 p-6 rounded-lg border border-blue-200">
          <div className="flex items-center mb-4">
            <User className="w-5 h-5 text-blue-600 mr-2" />
            <h3 className="text-lg font-semibold text-gray-800">Personal Information</h3>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div>
              <label className={labelClassName}>
                Age: <span className="text-blue-600 font-bold">{formData.Age}</span>
              </label>
              <input
                type="range"
                name="Age"
                min="18"
                max="65"
                value={formData.Age}
                onChange={handleChange}
                className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-blue-600"
                required
              />
              <div className="flex justify-between text-xs text-gray-500 mt-1">
                <span>18</span>
                <span>65</span>
              </div>
            </div>

            <div>
              <label className={labelClassName}>
                Distance From Home: <span className="text-blue-600 font-bold">{formData.DistanceFromHome} km</span>
              </label>
              <input
                type="range"
                name="DistanceFromHome"
                min="1"
                max="50"
                value={formData.DistanceFromHome}
                onChange={handleChange}
                className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-blue-600"
                required
              />
              <div className="flex justify-between text-xs text-gray-500 mt-1">
                <span>1 km</span>
                <span>50 km</span>
              </div>
            </div>

            <div>
              <label className={labelClassName}>Gender</label>
              <select
                name="Gender"
                value={formData.Gender}
                onChange={handleChange}
                className={selectClassName}
              >
                <option value="Male">Male</option>
                <option value="Female">Female</option>
              </select>
            </div>
          </div>
        </div>

        {/* Work Information */}
        <div className="bg-gradient-to-r from-green-50 to-emerald-50 p-6 rounded-lg border border-green-200">
          <div className="flex items-center mb-4">
            <Briefcase className="w-5 h-5 text-green-600 mr-2" />
            <h3 className="text-lg font-semibold text-gray-800">Work Information</h3>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div>
              <label className={labelClassName}>
                Years at Company: <span className="text-blue-600 font-bold">{formData.YearsAtCompany} years</span>
              </label>
              <input
                type="range"
                name="YearsAtCompany"
                min="0"
                max="40"
                value={formData.YearsAtCompany}
                onChange={handleChange}
                className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-blue-600"
                required
              />
              <div className="flex justify-between text-xs text-gray-500 mt-1">
                <span>0</span>
                <span>40 years</span>
              </div>
            </div>

            <div>
              <label className={labelClassName}>Job Level</label>
              <select
                name="JobLevel"
                value={formData.JobLevel}
                onChange={handleChange}
                className={selectClassName}
                required
              >
                <option value="1">Level 1 - Entry</option>
                <option value="2">Level 2 - Junior</option>
                <option value="3">Level 3 - Senior</option>
                <option value="4">Level 4 - Lead</option>
                <option value="5">Level 5 - Manager</option>
              </select>
            </div>

            <div>
              <label className={labelClassName}>Department</label>
              <select
                name="Department"
                value={formData.Department}
                onChange={handleChange}
                className={selectClassName}
                required
              >
                <option value="Research & Development">Research & Development</option>
                <option value="Sales">Sales</option>
                <option value="Human Resources">Human Resources</option>
              </select>
            </div>

            <div>
              <label className={labelClassName}>Job Role</label>
              <select
                name="JobRole"
                value={formData.JobRole}
                onChange={handleChange}
                className={selectClassName}
              >
                <option value="Sales Executive">Sales Executive</option>
                <option value="Research Scientist">Research Scientist</option>
                <option value="Laboratory Technician">Laboratory Technician</option>
                <option value="Manufacturing Director">Manufacturing Director</option>
                <option value="Healthcare Representative">Healthcare Representative</option>
                <option value="Manager">Manager</option>
                <option value="Sales Representative">Sales Representative</option>
                <option value="Research Director">Research Director</option>
                <option value="Human Resources">Human Resources</option>
              </select>
            </div>

            <div>
              <label className={labelClassName}>Over Time</label>
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
              <label className={labelClassName}>Business Travel</label>
              <select
                name="BusinessTravel"
                value={formData.BusinessTravel}
                onChange={handleChange}
                className={selectClassName}
              >
                <option value="Travel_Rarely">Travel Rarely</option>
                <option value="Travel_Frequently">Travel Frequently</option>
                <option value="Non-Travel">Non-Travel</option>
              </select>
            </div>
          </div>
        </div>

        {/* Compensation */}
        <div className="bg-gradient-to-r from-yellow-50 to-amber-50 p-6 rounded-lg border border-yellow-200">
          <div className="flex items-center mb-4">
            <DollarSign className="w-5 h-5 text-yellow-600 mr-2" />
            <h3 className="text-lg font-semibold text-gray-800">Compensation</h3>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className={labelClassName}>
                Monthly Income: <span className="text-blue-600 font-bold">${formData.MonthlyIncome}</span>
              </label>
              <input
                type="range"
                name="MonthlyIncome"
                min="1000"
                max="20000"
                step="100"
                value={formData.MonthlyIncome}
                onChange={handleChange}
                className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-blue-600"
                required
              />
              <div className="flex justify-between text-xs text-gray-500 mt-1">
                <span>$1,000</span>
                <span>$20,000</span>
              </div>
            </div>
          </div>
        </div>

        {/* Job Satisfaction */}
        <div className="bg-gradient-to-r from-purple-50 to-pink-50 p-6 rounded-lg border border-purple-200">
          <div className="flex items-center mb-4">
            <Clock className="w-5 h-5 text-purple-600 mr-2" />
            <h3 className="text-lg font-semibold text-gray-800">Job Satisfaction & Work-Life Balance</h3>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <div>
              <label className={labelClassName}>Job Satisfaction (1-4)</label>
              <select
                name="JobSatisfaction"
                value={formData.JobSatisfaction}
                onChange={handleChange}
                className={selectClassName}
                required
              >
                <option value="1">1 - Low</option>
                <option value="2">2 - Medium</option>
                <option value="3">3 - High</option>
                <option value="4">4 - Very High</option>
              </select>
            </div>

            <div>
              <label className={labelClassName}>Work Life Balance (1-4)</label>
              <select
                name="WorkLifeBalance"
                value={formData.WorkLifeBalance}
                onChange={handleChange}
                className={selectClassName}
                required
              >
                <option value="1">1 - Bad</option>
                <option value="2">2 - Good</option>
                <option value="3">3 - Better</option>
                <option value="4">4 - Best</option>
              </select>
            </div>

            <div>
              <label className={labelClassName}>Environment Satisfaction</label>
              <select
                name="EnvironmentSatisfaction"
                value={formData.EnvironmentSatisfaction}
                onChange={handleChange}
                className={selectClassName}
              >
                <option value="1">1 - Low</option>
                <option value="2">2 - Medium</option>
                <option value="3">3 - High</option>
                <option value="4">4 - Very High</option>
              </select>
            </div>

            <div>
              <label className={labelClassName}>Job Involvement</label>
              <select
                name="JobInvolvement"
                value={formData.JobInvolvement}
                onChange={handleChange}
                className={selectClassName}
              >
                <option value="1">1 - Low</option>
                <option value="2">2 - Medium</option>
                <option value="3">3 - High</option>
                <option value="4">4 - Very High</option>
              </select>
            </div>
          </div>
        </div>

        {/* Personal Details */}
        <div className="bg-gradient-to-r from-gray-50 to-slate-50 p-6 rounded-lg border border-gray-200">
          <div className="flex items-center mb-4">
            <User className="w-5 h-5 text-gray-600 mr-2" />
            <h3 className="text-lg font-semibold text-gray-800">Personal Details</h3>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div>
              <label className={labelClassName}>Education Field</label>
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
              <label className={labelClassName}>Marital Status</label>
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

            <div>
              <label className={labelClassName}>Education Level</label>
              <select
                name="Education"
                value={formData.Education}
                onChange={handleChange}
                className={selectClassName}
              >
                <option value="1">1 - Below College</option>
                <option value="2">2 - College</option>
                <option value="3">3 - Bachelor</option>
                <option value="4">4 - Master</option>
                <option value="5">5 - Doctor</option>
              </select>
            </div>
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

      {prediction && prediction.success !== false && (
        <div className="mt-8 p-6 bg-gray-50 rounded-xl border border-gray-200">
          <h3 className="text-xl font-bold text-gray-800 mb-4">Prediction Result</h3>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="bg-white p-6 rounded-lg border border-gray-200 shadow-sm">
              <div className="flex items-center mb-3">
                {(() => {
                  const probability = prediction.probability?.will_leave || 0
                  const risk = getRiskLevel(probability)
                  const IconComponent = risk.icon
                  return (
                    <>
                      <IconComponent className={`w-6 h-6 ${risk.color} mr-3`} />
                      <span className={`font-bold text-lg ${risk.color}`}>
                        {prediction.risk_level || risk.level} Risk
                      </span>
                    </>
                  )
                })()}
              </div>
              <p className="text-3xl font-bold text-gray-800 mb-1">
                {((prediction.probability?.will_leave || 0) * 100).toFixed(1)}%
              </p>
              <p className="text-gray-600">Attrition Probability</p>
            </div>

            <div className="bg-white p-6 rounded-lg border border-gray-200 shadow-sm">
              <h4 className="font-bold text-gray-800 mb-3">Prediction Details</h4>
              <div className="space-y-2 text-sm">
                <p>
                  <span className="font-medium text-gray-700">Model:</span> 
                  <span className="text-gray-600 ml-2">
                    {prediction.model_type || 'ML Model'}
                  </span>
                </p>
                <p>
                  <span className="font-medium text-gray-700">Prediction:</span> 
                  <span className={`ml-2 font-medium ${
                    prediction.prediction === 1 ? 'text-red-600' : 'text-green-600'
                  }`}>
                    {prediction.prediction_label || (prediction.prediction === 1 ? 'Will Leave' : 'Will Stay')}
                  </span>
                </p>
                {prediction.confidence && (
                  <p>
                    <span className="font-medium text-gray-700">Confidence:</span> 
                    <span className="text-gray-600 ml-2">{(prediction.confidence * 100).toFixed(1)}%</span>
                  </p>
                )}
                {prediction.note && (
                  <p className="text-xs text-blue-600 mt-2">
                    <span className="font-medium">Note:</span> {prediction.note}
                  </p>
                )}
              </div>
            </div>
          </div>

          {/* Probability Breakdown */}
          {prediction.probability && (
            <div className="mt-6 bg-white p-6 rounded-lg border border-gray-200 shadow-sm">
              <h4 className="font-bold text-gray-800 mb-4">Probability Breakdown</h4>
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <span className="text-gray-700">Will Stay:</span>
                  <div className="flex items-center space-x-3">
                    <div className="w-40 bg-gray-200 rounded-full h-3">
                      <div 
                        className="bg-green-500 h-3 rounded-full transition-all duration-500" 
                        style={{width: `${prediction.probability.will_stay * 100}%`}}
                      ></div>
                    </div>
                    <span className="text-sm font-medium text-green-600">
                      {(prediction.probability.will_stay * 100).toFixed(1)}%
                    </span>
                  </div>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-gray-700">Will Leave:</span>
                  <div className="flex items-center space-x-3">
                    <div className="w-40 bg-gray-200 rounded-full h-3">
                      <div 
                        className="bg-red-500 h-3 rounded-full transition-all duration-500" 
                        style={{width: `${prediction.probability.will_leave * 100}%`}}
                      ></div>
                    </div>
                    <span className="text-sm font-medium text-red-600">
                      {(prediction.probability.will_leave * 100).toFixed(1)}%
                    </span>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Feature Importance */}
          {(prediction.top_feature_importance || prediction.feature_importance) && (
            <div className="mt-6 bg-white p-6 rounded-lg border border-gray-200 shadow-sm">
              <h4 className="font-bold text-gray-800 mb-4">Key Contributing Factors</h4>
              <div className="space-y-3">
                {(() => {
                  const features = prediction.top_feature_importance || prediction.feature_importance
                  const featureEntries = Object.entries(features)
                    .filter(([_, importance]) => importance > 0)
                    .sort(([,a], [,b]) => b - a)
                    .slice(0, 6)
                  
                  return featureEntries.map(([feature, importance]) => (
                    <div key={feature} className="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
                      <span className="font-medium text-gray-700 text-sm">
                        {feature.replace(/_/g, ' ').replace(/([A-Z])/g, ' $1').trim()}
                      </span>
                      <span className="font-bold px-3 py-1 rounded-full text-sm bg-blue-100 text-blue-700">
                        {(importance * 100).toFixed(1)}%
                      </span>
                    </div>
                  ))
                })()}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

export default PredictionForm