import React from 'react'
import { createRoot } from 'react-dom/client'
import './main.css'

// Placeholder for customer dashboard - will be implemented later
function CustomerDashboard() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
      <div className="container mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold text-white mb-4">לוח הבקרה האישי</h1>
        <p className="text-slate-400">בקרוב...</p>
      </div>
    </div>
  )
}

// Initialize React app
const container = document.getElementById('customer-dashboard-root')
if (container) {
  const root = createRoot(container)
  root.render(<CustomerDashboard />)
}