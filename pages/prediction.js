import Layout from '../components/Layout'
import PredictionForm from '../components/PredictionForm'
import { Brain, Target, TrendingUp } from 'lucide-react'

export default function Prediction() {
  return (
    <Layout currentPage="prediction">
      <div className="min-h-screen bg-gray-50 py-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          {/* Header */}
          <div className="text-center mb-8">
            <div className="flex justify-center mb-4">
              <Brain className="w-12 h-12 text-blue-600" />
            </div>
            <h1 className="text-3xl font-bold text-gray-900 mb-2">
              Employee Attrition Prediction
            </h1>
            <p className="text-lg text-gray-600 max-w-2xl mx-auto">
              Use our machine learning model to predict the likelihood of an employee leaving the company
            </p>
          </div>

          {/* Info Cards */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
            <div className="bg-white p-6 rounded-lg shadow">
              <div className="flex items-center mb-3">
                <Target className="w-8 h-8 text-blue-600 mr-3" />
                <h3 className="text-lg font-semibold text-gray-800">Accurate Predictions</h3>
              </div>
              <p className="text-gray-600">
                Our ML model analyzes multiple factors to provide reliable attrition risk assessments
              </p>
            </div>

            <div className="bg-white p-6 rounded-lg shadow">
              <div className="flex items-center mb-3">
                <TrendingUp className="w-8 h-8 text-green-600 mr-3" />
                <h3 className="text-lg font-semibold text-gray-800">Real-time Analysis</h3>
              </div>
              <p className="text-gray-600">
                Get instant predictions based on current employee data and company metrics
              </p>
            </div>

            <div className="bg-white p-6 rounded-lg shadow">
              <div className="flex items-center mb-3">
                <Brain className="w-8 h-8 text-purple-600 mr-3" />
                <h3 className="text-lg font-semibold text-gray-800">Data-Driven Insights</h3>
              </div>
              <p className="text-gray-600">
                Understand key factors influencing employee retention and attrition patterns
              </p>
            </div>
          </div>

          {/* Prediction Form */}
          <PredictionForm />

          {/* Usage Instructions */}
          <div className="mt-8 bg-blue-50 border border-blue-200 rounded-lg p-6">
            <h3 className="text-lg font-semibold text-blue-900 mb-3">How to Use</h3>
            <ul className="space-y-2 text-blue-800">
              <li className="flex items-start">
                <span className="bg-blue-200 text-blue-800 rounded-full w-6 h-6 flex items-center justify-center text-sm font-semibold mr-3 mt-0.5">1</span>
                Fill in the employee information in the form above
              </li>
              <li className="flex items-start">
                <span className="bg-blue-200 text-blue-800 rounded-full w-6 h-6 flex items-center justify-center text-sm font-semibold mr-3 mt-0.5">2</span>
                Click "Predict Attrition Risk" to analyze the data
              </li>
              <li className="flex items-start">
                <span className="bg-blue-200 text-blue-800 rounded-full w-6 h-6 flex items-center justify-center text-sm font-semibold mr-3 mt-0.5">3</span>
                Review the risk assessment and key contributing factors
              </li>
              <li className="flex items-start">
                <span className="bg-blue-200 text-blue-800 rounded-full w-6 h-6 flex items-center justify-center text-sm font-semibold mr-3 mt-0.5">4</span>
                Use insights to develop targeted retention strategies
              </li>
            </ul>
          </div>
        </div>
      </div>
    </Layout>
  )
}