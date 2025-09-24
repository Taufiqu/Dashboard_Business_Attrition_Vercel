import Layout from '../components/Layout'
import { TrendingDown, Users, AlertTriangle, BarChart3, ArrowRight, Activity } from 'lucide-react'

export default function Home() {
  const stats = [
    {
      name: 'Total Employees',
      stat: '2,847',
      icon: Users,
      change: '+4.3%',
      changeType: 'positive'
    },
    {
      name: 'Attrition Rate',
      stat: '12.4%',
      icon: TrendingDown,
      change: '-2.1%',
      changeType: 'positive'
    },
    {
      name: 'At Risk Employees',
      stat: '342',
      icon: AlertTriangle,
      change: '+8.2%',
      changeType: 'negative'
    },
    {
      name: 'Avg Tenure',
      stat: '3.2 years',
      icon: Activity,
      change: '+0.4%',
      changeType: 'positive'
    }
  ]

  const insights = [
    {
      title: 'Highest Risk Department',
      value: 'Engineering',
      description: '18.7% attrition rate, 15% above average',
      trend: 'negative'
    },
    {
      title: 'Retention Improvement',
      value: 'Sales Team',
      description: 'Attrition reduced by 23% this quarter',
      trend: 'positive'
    },
    {
      title: 'Key Risk Factor',
      value: 'Work-Life Balance',
      description: 'Primary reason for 34% of departures',
      trend: 'negative'
    }
  ]

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
        <h2 className="text-2xl font-bold text-gray-900 mb-6">Key Metrics Overview</h2>
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
                    item.changeType === 'positive' ? 'text-green-600' : 'text-red-600'
                  }`}>
                    {item.change}
                  </p>
                  <div className="absolute bottom-0 inset-x-0 bg-gray-50 px-4 py-4 sm:px-6">
                    <div className="text-sm">
                      <span className="text-gray-600">vs last month</span>
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