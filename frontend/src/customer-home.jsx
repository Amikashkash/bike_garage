import React from 'react'
import { createRoot } from 'react-dom/client'
import CustomerHome from './components/CustomerHome'
import './main.css'

// Initialize React app
const container = document.getElementById('customer-home-root')
if (container) {
  const root = createRoot(container)
  root.render(<CustomerHome />)
}