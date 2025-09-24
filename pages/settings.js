import Layout from '../components/Layout'
import ClientOnly from '../components/ClientOnly'
import { Cog, Save, RefreshCw, Database, Bell, Shield, Eye } from 'lucide-react'

export default function SettingsPage() {
  const handleSave = (e) => {
    e.preventDefault()
    // Handle save settings
    alert('Settings saved successfully!')
  }

  return (
    <Layout currentPage="settings">
      <div className="max-w-4xl">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Settings</h1>
          <p className="mt-1 text-sm text-gray-600">
            Configure your dashboard preferences and data sources
          </p>
        </div>

        <div className="space-y-8">
          {/* Dashboard Configuration */}
          <div className="bg-white shadow-lg rounded-lg">
            <div className="px-6 py-4 border-b border-gray-200">
              <div className="flex items-center">
                <Cog className="h-5 w-5 text-gray-400 mr-2" />
                <h2 className="text-xl font-semibold text-gray-900">Dashboard Configuration</h2>
              </div>
            </div>
            <div className="p-6">
              <form onSubmit={handleSave} className="space-y-6">
                <div>
                  <label htmlFor="dashboardTitle" className="block text-sm font-medium text-gray-700 mb-2">
                    Dashboard Title
                  </label>
                  <input
                    type="text"
                    id="dashboardTitle"
                    className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500"
                    defaultValue="Business Attrition Analytics"
                  />
                </div>
                
                <div>
                  <label htmlFor="companyName" className="block text-sm font-medium text-gray-700 mb-2">
                    Company Name
                  </label>
                  <input
                    type="text"
                    id="companyName"
                    className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500"
                    defaultValue="AttritionAI"
                  />
                </div>

                <div>
                  <label htmlFor="refreshInterval" className="block text-sm font-medium text-gray-700 mb-2">
                    Auto Refresh Interval (minutes)
                  </label>
                  <select
                    id="refreshInterval"
                    className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500"
                  >
                    <option value="5">5 minutes</option>
                    <option value="10">10 minutes</option>
                    <option value="15" selected>15 minutes</option>
                    <option value="30">30 minutes</option>
                    <option value="60">1 hour</option>
                  </select>
                </div>
              </form>
            </div>
          </div>

          {/* Data Source Settings */}
          <div className="bg-white shadow-lg rounded-lg">
            <div className="px-6 py-4 border-b border-gray-200">
              <div className="flex items-center">
                <Database className="h-5 w-5 text-gray-400 mr-2" />
                <h2 className="text-xl font-semibold text-gray-900">Data Source</h2>
              </div>
            </div>
            <div className="p-6">
              <div className="space-y-4">
                <div className="flex items-center justify-between p-4 bg-green-50 border border-green-200 rounded-lg">
                  <div className="flex items-center">
                    <div className="h-3 w-3 bg-green-400 rounded-full mr-3"></div>
                    <div>
                      <p className="font-medium text-green-900">Google Looker Studio</p>
                      <p className="text-sm text-green-700">Connected and syncing</p>
                    </div>
                  </div>
                  <button className="inline-flex items-center px-3 py-1 border border-green-300 text-sm font-medium rounded-md text-green-700 bg-green-100 hover:bg-green-200">
                    <RefreshCw className="h-4 w-4 mr-1" />
                    Refresh
                  </button>
                </div>
                
                <div className="p-4 bg-gray-50 border border-gray-200 rounded-lg">
                  <ClientOnly>
                    <p className="text-sm text-gray-600 mb-2">
                      <strong>Last Sync:</strong> {new Date().toLocaleString()}
                    </p>
                  </ClientOnly>
                  <p className="text-sm text-gray-600">
                    <strong>Data Range:</strong> Last 12 months
                  </p>
                </div>
              </div>
            </div>
          </div>

          {/* Notification Settings */}
          <div className="bg-white shadow-lg rounded-lg">
            <div className="px-6 py-4 border-b border-gray-200">
              <div className="flex items-center">
                <Bell className="h-5 w-5 text-gray-400 mr-2" />
                <h2 className="text-xl font-semibold text-gray-900">Notifications</h2>
              </div>
            </div>
            <div className="p-6 space-y-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="font-medium text-gray-900">High Attrition Alerts</p>
                  <p className="text-sm text-gray-600">Get notified when attrition rate exceeds threshold</p>
                </div>
                <input type="checkbox" className="h-5 w-5 text-primary-600" defaultChecked />
              </div>
              
              <div className="flex items-center justify-between">
                <div>
                  <p className="font-medium text-gray-900">Weekly Reports</p>
                  <p className="text-sm text-gray-600">Receive weekly attrition summary via email</p>
                </div>
                <input type="checkbox" className="h-5 w-5 text-primary-600" />
              </div>

              <div className="flex items-center justify-between">
                <div>
                  <p className="font-medium text-gray-900">Data Quality Issues</p>
                  <p className="text-sm text-gray-600">Alert when data sync encounters problems</p>
                </div>
                <input type="checkbox" className="h-5 w-5 text-primary-600" defaultChecked />
              </div>
            </div>
          </div>

          {/* Privacy & Security */}
          <div className="bg-white shadow-lg rounded-lg">
            <div className="px-6 py-4 border-b border-gray-200">
              <div className="flex items-center">
                <Shield className="h-5 w-5 text-gray-400 mr-2" />
                <h2 className="text-xl font-semibold text-gray-900">Privacy & Security</h2>
              </div>
            </div>
            <div className="p-6 space-y-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="font-medium text-gray-900">Data Anonymization</p>
                  <p className="text-sm text-gray-600">Anonymize personal identifiers in reports</p>
                </div>
                <input type="checkbox" className="h-5 w-5 text-primary-600" defaultChecked />
              </div>
              
              <div className="flex items-center justify-between">
                <div>
                  <p className="font-medium text-gray-900">Audit Logging</p>
                  <p className="text-sm text-gray-600">Log all dashboard access and actions</p>
                </div>
                <input type="checkbox" className="h-5 w-5 text-primary-600" defaultChecked />
              </div>
            </div>
          </div>

          {/* Save Button */}
          <div className="flex justify-end">
            <button
              onClick={handleSave}
              className="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
            >
              <Save className="h-5 w-5 mr-2" />
              Save Settings
            </button>
          </div>
        </div>
      </div>
    </Layout>
  )
}