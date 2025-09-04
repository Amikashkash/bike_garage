import React from 'react'
import { createRoot } from 'react-dom/client'
import CustomerBikesList from './components/CustomerBikesList'

// Initialize the React app
const container = document.getElementById('customer-bikes-list-root')
if (container) {
  const root = createRoot(container)
  root.render(<CustomerBikesList />)
} else {
  console.error('Customer Bikes List: Root element not found')
}