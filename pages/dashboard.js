import { useState } from 'react'
import Layout from '../components/Layout'
import LookerEmbed from '../components/LookerEmbed'
import ClientOnly from '../components/ClientOnly'
import { Settings, RefreshCw, Download, Filter, Calendar, AlertCircle } from 'lucide-react'

export default function Dashboard() {
  const [embedCode, setEmbedCode] = useState('')
  const [showEmbedInput, setShowEmbedInput] = useState(false)
  const [isRefreshing, setIsRefreshing] = useState(false)

  const handleRefresh = () => {
    setIsRefreshing(true)
    // Simulate refresh
    setTimeout(() => {
      setIsRefreshing(false)
    }, 2000)
  }

  const handleEmbedCodeSubmit = (e) => {
    e.preventDefault()
    const formData = new FormData(e.target)
    const code = formData.get('embedCode')
    if (code.trim()) {
      setEmbedCode(code)
      setShowEmbedInput(false)
    }
  }

  return (
    <Layout currentPage="dashboard">
      {/* Dashboard Controls */}
      <div className="mb-6 flex flex-col sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Analytics Dashboard</h1>
          <p className="mt-1 text-sm text-gray-600">
            Comprehensive business attrition insights and trends
          </p>
        </div>
        
        <div className="mt-4 sm:mt-0 flex items-center space-x-3">
          <button
            onClick={() => setShowEmbedInput(!showEmbedInput)}
            className="inline-flex items-center px-3 py-2 border border-gray-300 shadow-sm text-sm leading-4 font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
          >
            <Settings className="h-4 w-4 mr-2" />
            Setup Embed
          </button>
          
          <button
            onClick={handleRefresh}
            disabled={isRefreshing}
            className="inline-flex items-center px-3 py-2 border border-transparent shadow-sm text-sm leading-4 font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50"
          >
            <RefreshCw className={`h-4 w-4 mr-2 ${isRefreshing ? 'animate-spin' : ''}`} />
            {isRefreshing ? 'Refreshing...' : 'Refresh'}
          </button>
          
          <button className="inline-flex items-center px-3 py-2 border border-gray-300 shadow-sm text-sm leading-4 font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500">
            <Download className="h-4 w-4 mr-2" />
            Export
          </button>
        </div>
      </div>

      {/* Embed Code Input Modal */}
      {showEmbedInput && (
        <div className="mb-6 bg-white shadow-lg rounded-lg p-6 border border-gray-200">
          <div className="flex items-center mb-4">
            <AlertCircle className="h-5 w-5 text-primary-600 mr-2" />
            <h3 className="text-lg font-medium text-gray-900">Setup Google Looker Embed</h3>
          </div>
          
          <form onSubmit={handleEmbedCodeSubmit} className="space-y-4">
            <div>
              <label htmlFor="embedCode" className="block text-sm font-medium text-gray-700 mb-2">
                Paste your Google Looker Studio embed code here:
              </label>
              <textarea
                id="embedCode"
                name="embedCode"
                rows={6}
                className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500"
                placeholder='<iframe src="https://lookerstudio.google.com/embed/reporting/..." frameborder="0" style="border:0" allowfullscreen></iframe>'
              />
            </div>
            
            <div className="flex items-center space-x-3">
              <button
                type="submit"
                className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
              >
                Apply Embed Code
              </button>
              <button
                type="button"
                onClick={() => setShowEmbedInput(false)}
                className="inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
              >
                Cancel
              </button>
            </div>
          </form>
          
          <div className="mt-4 p-4 bg-blue-50 rounded-md">
            <h4 className="text-sm font-medium text-blue-900 mb-2">How to get embed code:</h4>
            <ol className="text-sm text-blue-800 space-y-1">
              <li>1. Open your dashboard in Google Looker Studio</li>
              <li>2. Click the "Share" button in the top right</li>
              <li>3. Select "Embed report"</li>
              <li>4. Copy the iframe code provided</li>
              <li>5. Paste it in the textbox above</li>
            </ol>
          </div>
        </div>
      )}

      {/* Dashboard Content */}
      <div className="bg-white shadow-lg rounded-lg p-6">
        <LookerEmbed 
          embedCode="true"
          title="Business Attrition Analytics"
        />
      </div>

      {/* Additional Dashboard Info */}
      <div className="mt-6 grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="bg-white shadow rounded-lg p-6">
          <div className="flex items-center">
            <Calendar className="h-5 w-5 text-gray-400" />
            <h3 className="ml-2 text-lg font-medium text-gray-900">Last Updated</h3>
          </div>
          <p className="mt-2 text-sm text-gray-600">
            Dashboard data is synchronized in real-time with your HR systems.
          </p>
          <ClientOnly>
            <p className="mt-1 text-xs text-gray-500">
              Last refresh: {new Date().toLocaleString()}
            </p>
          </ClientOnly>
        </div>

        <div className="bg-white shadow rounded-lg p-6">
          <div className="flex items-center">
            <Filter className="h-5 w-5 text-gray-400" />
            <h3 className="ml-2 text-lg font-medium text-gray-900">Data Filters</h3>
          </div>
          <p className="mt-2 text-sm text-gray-600">
            Use the filters within the embedded dashboard to drill down into specific departments, time periods, or employee segments.
          </p>
        </div>

        <div className="bg-white shadow rounded-lg p-6">
          <div className="flex items-center">
            <Download className="h-5 w-5 text-gray-400" />
            <h3 className="ml-2 text-lg font-medium text-gray-900">Export Options</h3>
          </div>
          <p className="mt-2 text-sm text-gray-600">
            Export your analytics data directly from the Looker dashboard using the built-in export functionality.
          </p>
        </div>
      </div>
    </Layout>
  )
}