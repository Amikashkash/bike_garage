import React, { useState, useEffect } from 'react'
import { useWebSocket } from '../hooks/useWebSocket'

export default function CustomerHome() {
  const [stats, setStats] = useState({
    activeRepairs: 0,
    totalRepairs: 0,
    notifications: 0
  })
  
  const { isConnected, messages } = useWebSocket(null, 'customer')

  useEffect(() => {
    // Fetch initial stats
    fetch('/api/customer/stats/')
      .then(res => res.json())
      .then(data => setStats(data))
      .catch(err => console.error('Error fetching stats:', err))
  }, [])

  useEffect(() => {
    // Handle real-time messages
    messages.forEach(message => {
      if (message.type === 'repair_status_update') {
        // Refresh stats when repairs update
        fetch('/api/customer/stats/')
          .then(res => res.json())
          .then(data => setStats(data))
      }
    })
  }, [messages])

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
      {/* Header */}
      <div className="bg-slate-800/30 backdrop-blur-md border-b border-slate-700">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-blue-500/20 rounded-xl flex items-center justify-center">
                <i className="fas fa-bicycle text-blue-400"></i>
              </div>
              <h1 className="text-xl font-bold text-white">אופני יקיר</h1>
            </div>
            
            {/* Connection Status */}
            <div className="flex items-center gap-2">
              <div className={`w-2 h-2 rounded-full ${isConnected ? 'bg-green-400' : 'bg-red-400'}`}></div>
              <span className="text-sm text-slate-400">
                {isConnected ? 'מחובר' : 'מנותק'}
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="container mx-auto px-4 py-8">
        {/* Welcome Section */}
        <div className="mb-8 animate-fade-in">
          <h2 className="text-3xl font-bold text-white mb-2">שלום! 👋</h2>
          <p className="text-slate-400 text-lg">ברוכים הבאים למערכת ניהול התיקונים</p>
        </div>

        {/* Quick Stats */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <StatCard
            icon="fas fa-tools"
            title="תיקונים פעילים"
            value={stats.activeRepairs}
            color="blue"
            className="animate-slide-up"
            style={{ animationDelay: '0.1s' }}
          />
          <StatCard
            icon="fas fa-history" 
            title="סה״כ תיקונים"
            value={stats.totalRepairs}
            color="purple"
            className="animate-slide-up"
            style={{ animationDelay: '0.2s' }}
          />
          <StatCard
            icon="fas fa-bell"
            title="התראות חדשות"
            value={stats.notifications}
            color="green"
            className="animate-slide-up"
            style={{ animationDelay: '0.3s' }}
          />
        </div>

        {/* Action Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
          <ActionCard
            icon="fas fa-plus-circle"
            title="דיווח תיקון חדש"
            description="דווח על תקלה באופניים שלך"
            href="/customer/report/"
            color="bg-gradient-to-br from-blue-500 to-blue-600"
            className="animate-scale-in"
            style={{ animationDelay: '0.4s' }}
          />
          
          <ActionCard
            icon="fas fa-list-alt"
            title="הלוח האישי שלי"
            description="צפה בכל התיקונים וההתראות"
            href="/customer/dashboard/"
            color="bg-gradient-to-br from-purple-500 to-purple-600"
            className="animate-scale-in"
            style={{ animationDelay: '0.5s' }}
          />
        </div>

        {/* Recent Activity */}
        <div className="card-mercury animate-fade-in" style={{ animationDelay: '0.6s' }}>
          <h3 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
            <i className="fas fa-clock text-blue-400"></i>
            פעילות אחרונה
          </h3>
          <div className="text-slate-400">
            <p>עדכונים אחרונים יופיעו כאן בזמן אמת</p>
          </div>
        </div>
      </div>
    </div>
  )
}

function StatCard({ icon, title, value, color, className, style }) {
  const colorClasses = {
    blue: 'from-blue-500/20 to-blue-600/20 border-blue-500/30',
    purple: 'from-purple-500/20 to-purple-600/20 border-purple-500/30',
    green: 'from-green-500/20 to-green-600/20 border-green-500/30'
  }

  const iconColorClasses = {
    blue: 'text-blue-400',
    purple: 'text-purple-400', 
    green: 'text-green-400'
  }

  return (
    <div className={`bg-gradient-to-br ${colorClasses[color]} backdrop-blur-sm border rounded-xl p-6 ${className}`} style={style}>
      <div className="flex items-center justify-between">
        <div>
          <p className="text-slate-300 text-sm mb-1">{title}</p>
          <p className={`text-3xl font-bold ${iconColorClasses[color]}`}>{value}</p>
        </div>
        <div className={`w-12 h-12 bg-gradient-to-br ${colorClasses[color]} rounded-xl flex items-center justify-center`}>
          <i className={`${icon} ${iconColorClasses[color]} text-xl`}></i>
        </div>
      </div>
    </div>
  )
}

function ActionCard({ icon, title, description, href, color, className, style }) {
  return (
    <a 
      href={href}
      className={`block ${color} hover:scale-105 rounded-xl p-6 shadow-lg hover:shadow-xl transition-all duration-200 ${className}`}
      style={style}
    >
      <div className="flex items-start gap-4">
        <div className="w-12 h-12 bg-white/20 rounded-xl flex items-center justify-center flex-shrink-0">
          <i className={`${icon} text-white text-xl`}></i>
        </div>
        <div>
          <h4 className="text-xl font-bold text-white mb-2">{title}</h4>
          <p className="text-white/80">{description}</p>
        </div>
      </div>
    </a>
  )
}