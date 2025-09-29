import { useState, useEffect } from 'react'
import Layout from '../components/Layout'
import { TrendingDown, Users, AlertTriangle, BarChart3, ArrowRight, Activity } from 'lucide-react'

export default function Home() {
  const [analytics, setAnalytics] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchAnalytics()
  }, [])

  const fetchAnalytics = async () => {
    try {
      const response = await fetch('/api/analytics')
      const data = await response.json()
      setAnalytics(data)
      setLoading(false)
    } catch (error) {
      console.error('Error fetching analytics:', error)
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <Layout currentPage="home">
        <div className="flex items-center justify-center min-h-64">
          <div className="loading-spinner mx-auto mb-4"></div>
          <p className="text-gray-600 ml-4">Loading analytics data...</p>
        </div>
      </Layout>
    )
  }

  const stats = analytics ? [
    {
      name: 'Total Employees',
      stat: analytics.totalEmployees.toLocaleString(),
      icon: Users,
      change: 'Real data',
      changeType: 'neutral'
    },
    {
      name: 'Attrition Rate',
      stat: `${analytics.attritionRate}%`,
      icon: TrendingDown,
      change: `${analytics.keyInsights.totalAttrition} employees`,
      changeType: analytics.attritionRate > 15 ? 'negative' : 'positive'
    },
    {
      name: 'At Risk Employees',
      stat: analytics.atRiskEmployees.toLocaleString(),
      icon: AlertTriangle,
      change: 'Low satisfaction + Overtime',
      changeType: 'negative'
    },
    {
      name: 'Avg Tenure',
      stat: `${analytics.avgTenure} years`,
      icon: Activity,
      change: `Avg age: ${analytics.avgAge} years`,
      changeType: 'positive'
    }
  ] : []

  const insights = analytics ? [
    {
      title: 'Highest Risk Department',
      value: analytics.highestAttritionDept.name,
      description: `${analytics.highestAttritionDept.rate}% attrition rate`,
      trend: 'negative'
    },
    {
      title: 'Overtime Impact',
      value: `${analytics.keyInsights.overTimeImpact}%`,
      description: 'Attrition rate among overtime workers',
      trend: analytics.keyInsights.overTimeImpact > 20 ? 'negative' : 'positive'
    },
    {
      title: 'Total Data Points',
      value: `${analytics.totalEmployees} Records`,
      description: 'Comprehensive employee dataset analyzed',
      trend: 'positive'
    }
  ] : []

  return (
    <Layout currentPage="home">
      {/* Welcome Section */}
      <div className="mb-8">
        <div className="bg-gradient-to-r from-primary-600 to-primary-700 rounded-lg shadow-xl overflow-hidden">
          <div className="px-6 py-8 sm:p-10 sm:pb-6">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <BarChart3 className="h-8 w-8 text-white" />
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-primary-100 truncate">Welcome to</dt>
                  <dd className="text-3xl font-bold text-white">Business Attrition Analytics</dd>
                </dl>
              </div>
            </div>
            <div className="mt-4">
              <p className="text-primary-100">
                Comprehensive insights into employee retention, attrition patterns, and predictive analytics 
                to help you make data-driven HR decisions.
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Key Metrics */}
      <div className="mb-8">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-2xl font-bold text-gray-900">Key Metrics Overview</h2>
          <div className="flex items-center space-x-4">
            <div className="flex items-center text-sm text-green-600">
              <div className="h-2 w-2 bg-green-400 rounded-full mr-2"></div>
              Real Data from CSV ({analytics ? analytics.totalEmployees.toLocaleString() : '0'} records)
            </div>
            <button
              onClick={fetchAnalytics}
              disabled={loading}
              className="inline-flex items-center px-3 py-2 border border-gray-300 shadow-sm text-sm leading-4 font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50"
            >
              <ArrowRight className={`h-4 w-4 mr-2 ${loading ? 'animate-spin' : ''}`} />
              Refresh Data
            </button>
          </div>
        </div>
        <dl className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
          {stats.map((item) => {
            const Icon = item.icon
            return (
              <div key={item.name} className="relative bg-white pt-5 px-4 pb-12 sm:pt-6 sm:px-6 shadow-lg rounded-lg overflow-hidden">
                <dt>
                  <div className="absolute bg-primary-500 rounded-md p-3">
                    <Icon className="h-6 w-6 text-white" />
                  </div>
                  <p className="ml-16 text-sm font-medium text-gray-500 truncate">{item.name}</p>
                </dt>
                <dd className="ml-16 pb-6 flex items-baseline sm:pb-7">
                  <p className="text-2xl font-semibold text-gray-900">{item.stat}</p>
                  <p className={`ml-2 flex items-baseline text-sm font-semibold ${
                    item.changeType === 'positive' ? 'text-green-600' : 
                    item.changeType === 'negative' ? 'text-red-600' : 'text-gray-600'
                  }`}>
                    {item.change}
                  </p>
                  <div className="absolute bottom-0 inset-x-0 bg-gray-50 px-4 py-4 sm:px-6">
                    <div className="text-sm">
                      <span className="text-gray-600">Based on real dataset analysis</span>
                    </div>
                  </div>
                </dd>
              </div>
            )
          })}
        </dl>
      </div>

      {/* Quick Insights */}
      <div className="mb-8">
        <h2 className="text-2xl font-bold text-gray-900 mb-6">Quick Insights</h2>
        <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
          {insights.map((insight, index) => (
            <div key={index} className="bg-white overflow-hidden shadow-lg rounded-lg">
              <div className="p-6">
                <div className="flex items-center">
                  <div className="flex-shrink-0">
                    <div className={`h-3 w-3 rounded-full ${
                      insight.trend === 'positive' ? 'bg-green-400' : 'bg-red-400'
                    }`} />
                  </div>
                  <div className="ml-3 w-0 flex-1">
                    <p className="text-sm font-medium text-gray-500">{insight.title}</p>
                    <p className="text-lg font-semibold text-gray-900">{insight.value}</p>
                  </div>
                </div>
                <div className="mt-4">
                  <p className="text-sm text-gray-600">{insight.description}</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* CTA Section */}
      <div className="bg-white shadow-lg rounded-lg overflow-hidden">
        <div className="px-6 py-8">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-xl font-bold text-gray-900">Ready for Deep Analytics?</h3>
              <p className="text-gray-600 mt-1">
                Explore comprehensive dashboards with advanced filtering and predictive insights.
              </p>
            </div>
            <div>
              <a
                href="/dashboard"
                className="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 transition-colors"
              >
                View Analytics Dashboard
                <ArrowRight className="ml-2 h-5 w-5" />
              </a>
            </div>
          </div>
        </div>
      </div>
    </Layout>
  )
}