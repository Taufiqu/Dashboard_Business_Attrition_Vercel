import { useState, useEffect } from 'react'

export default function LookerEmbed({ embedCode, title = "Analytics Dashboard" }) {
  const [isLoading, setIsLoading] = useState(true)
  const [isMounted, setIsMounted] = useState(false)

  useEffect(() => {
    setIsMounted(true)
    if (embedCode) {
      setIsLoading(false)
    }
  }, [embedCode])

  // Prevent hydration mismatch by not rendering until mounted
  if (!isMounted) {
    return (
      <div className="w-full h-96 bg-gray-100 rounded-lg flex flex-col items-center justify-center">
        <div className="loading-spinner mx-auto mb-4"></div>
        <p className="text-gray-600">Loading dashboard...</p>
      </div>
    )
  }

  if (!embedCode) {
    return (
      <div className="w-full h-96 bg-gray-100 rounded-lg flex flex-col items-center justify-center">
        <div className="text-center">
          <div className="mx-auto h-12 w-12 text-gray-400 mb-4">
            <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
            </svg>
          </div>
          <h3 className="text-lg font-medium text-gray-900 mb-2">Dashboard Ready</h3>
          <p className="text-sm text-gray-500 mb-4">
            Masukkan embed code dari Google Looker untuk menampilkan dashboard analytics
          </p>
          <div className="bg-yellow-50 border border-yellow-200 rounded-md p-4">
            <p className="text-sm text-yellow-800">
              <strong>Cara mendapatkan embed code:</strong>
              <br />1. Buka dashboard di Google Looker Studio
              <br />2. Klik tombol "Share" atau "Bagikan"
              <br />3. Pilih "Embed report" atau "Sematkan laporan"
              <br />4. Salin kode embed yang diberikan
            </p>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="w-full">
      <div className="mb-4">
        <h2 className="text-2xl font-bold text-gray-900">{title}</h2>
        <p className="text-sm text-gray-600">Real-time business attrition analytics powered by Google Looker</p>
      </div>
      
      <div className="relative w-full bg-white rounded-lg shadow-lg overflow-hidden">
        {isLoading && (
          <div className="absolute inset-0 bg-gray-100 flex items-center justify-center z-10">
            <div className="text-center">
              <div className="loading-spinner mx-auto mb-4"></div>
              <p className="text-gray-600">Loading dashboard...</p>
            </div>
          </div>
        )}
        
        <div 
          className="w-full"
          style={{ minHeight: '600px', height: '600px' }}
        >
          <iframe 
            src="https://lookerstudio.google.com/embed/reporting/1f6d0e32-9c2a-46aa-b5a7-b8e4b29ed806/page/p_ftmd8ridwd"
            width="100%"
            height="600"
            frameBorder="0"
            style={{border: 0}}
            allowFullScreen
            sandbox="allow-storage-access-by-user-activation allow-scripts allow-same-origin allow-popups allow-popups-to-escape-sandbox"
            onLoad={() => setIsLoading(false)}
          />
        </div>
      </div>
      
      <div className="mt-4 text-xs text-gray-500 text-center">
        Data is updated in real-time from your business systems
      </div>
    </div>
  )
}