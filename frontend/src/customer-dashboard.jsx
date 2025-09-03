import React from 'react'
import { createRoot } from 'react-dom/client'
import CustomerDashboard from './components/CustomerDashboard'
import './main.css'

// Initialize React app
const container = document.getElementById('customer-dashboard-root')
if (container) {
  const root = createRoot(container)
  root.render(<CustomerDashboard />)
}