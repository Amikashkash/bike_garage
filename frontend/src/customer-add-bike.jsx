import React from 'react'
import { createRoot } from 'react-dom/client'
import CustomerAddBike from './components/CustomerAddBike'

// Initialize the React app
const container = document.getElementById('customer-add-bike-root')
if (container) {
  const root = createRoot(container)
  root.render(<CustomerAddBike />)
} else {
  console.error('Customer Add Bike: Root element not found')
}