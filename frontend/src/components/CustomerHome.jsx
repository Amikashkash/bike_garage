import React, { useState, useEffect } from 'react'
import { useWebSocket } from '../hooks/useWebSocket'

export default function CustomerHome() {
  const [stats, setStats] = useState({
    activeRepairs: 0,
    totalRepairs: 0,
    notifications: 0,
    readyForPickup: 0
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
      <div className="container mx-auto px-4 py-6">
        {/* Welcome Section */}
        <div className="mb-6">
          <h2 className="text-2xl md:text-3xl font-bold text-white mb-1">שלום! 👋</h2>
          <p className="text-slate-400">מה תרצה לעשות היום?</p>
        </div>

        {/* Priority Alert - Ready for Pickup */}
        {stats.readyForPickup > 0 && (
          <div className="mb-6">
            <div className="bg-gradient-to-r from-green-500/20 to-emerald-500/20 border border-green-500/30 rounded-xl p-4 backdrop-blur-sm">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 bg-green-500/20 rounded-xl flex items-center justify-center">
                  <i className="fas fa-check-circle text-green-400"></i>
                </div>
                <div className="flex-1">
                  <h3 className="text-green-300 font-semibold">
                    {stats.readyForPickup} אופניים מוכנים לאיסוף! 🎉
                  </h3>
                  <p className="text-green-200/80 text-sm">ניתן לאסוף מהמוסך</p>
                </div>
                <a 
                  href="/customer/dashboard/"
                  className="bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded-lg text-sm transition-colors"
                >
                  צפה בפרטים
                </a>
              </div>
            </div>
          </div>
        )}

        {/* Quick Stats - Mobile First */}
        <div className="grid grid-cols-2 gap-4 mb-6">
          <StatCard
            icon="fas fa-tools"
            title="תיקונים פעילים"
            value={stats.activeRepairs}
            color="blue"
            compact={true}
          />
          <StatCard
            icon="fas fa-bell"
            title="התראות"
            value={stats.notifications}
            color="red"
            compact={true}
          />
          <StatCard
            icon="fas fa-check-circle"
            title="מוכן לאיסוף"
            value={stats.readyForPickup}
            color="green"
            compact={true}
          />
          <StatCard
            icon="fas fa-history" 
            title="סה״כ תיקונים"
            value={stats.totalRepairs}
            color="purple"
            compact={true}
          />
        </div>

        {/* Main Action Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
          <ActionCard
            icon="fas fa-plus-circle"
            title="דיווח תיקון חדש"
            description="דווח על תקלה באופניים שלך"
            href="/customer/report/"
            color="bg-gradient-to-br from-red-500 to-red-600"
          />
          
          <ActionCard
            icon="fas fa-tachometer-alt"
            title="הלוח האישי שלי"
            description="צפה בכל התיקונים וההתראות"
            href="/customer/dashboard/"
            color="bg-gradient-to-br from-blue-500 to-blue-600"
          />
        </div>

        {/* Secondary Actions */}
        <div className="grid grid-cols-2 gap-4">
          <SecondaryActionCard
            icon="fas fa-bicycle"
            title="האופניים שלי"
            href="/my-bikes/"
          />
          <SecondaryActionCard
            icon="fas fa-plus"
            title="הוסף אופניים"
            href="/my-bikes/add/"
          />
        </div>
      </div>
    </div>
  )
}

function StatCard({ icon, title, value, color, compact = false, className, style }) {
  const colorClasses = {
    blue: 'from-blue-500/20 to-blue-600/20 border-blue-500/30',
    purple: 'from-purple-500/20 to-purple-600/20 border-purple-500/30',
    green: 'from-green-500/20 to-green-600/20 border-green-500/30',
    red: 'from-red-500/20 to-red-600/20 border-red-500/30'
  }

  const iconColorClasses = {
    blue: 'text-blue-400',
    purple: 'text-purple-400', 
    green: 'text-green-400',
    red: 'text-red-400'
  }

  if (compact) {
    return (
      <div className={`bg-gradient-to-br ${colorClasses[color]} backdrop-blur-sm border rounded-xl p-4 ${className || ''}`} style={style}>
        <div className="text-center">
          <div className={`w-8 h-8 bg-gradient-to-br ${colorClasses[color]} rounded-lg flex items-center justify-center mx-auto mb-2`}>
            <i className={`${icon} ${iconColorClasses[color]} text-sm`}></i>
          </div>
          <p className={`text-2xl font-bold ${iconColorClasses[color]} mb-1`}>{value}</p>
          <p className="text-slate-300 text-xs">{title}</p>
        </div>
      </div>
    )
  }

  return (
    <div className={`bg-gradient-to-br ${colorClasses[color]} backdrop-blur-sm border rounded-xl p-6 ${className || ''}`} style={style}>
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
      className={`block ${color} hover:scale-105 rounded-xl p-6 shadow-lg hover:shadow-xl transition-all duration-200 ${className || ''}`}
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

function SecondaryActionCard({ icon, title, href }) {
  const handleClick = (e) => {
    console.log('SecondaryActionCard clicked:', { title, href })
    // Let the default link behavior happen
  }
  
  return (
    <a 
      href={href}
      onClick={handleClick}
      className="block bg-slate-800/50 hover:bg-slate-800/70 border border-slate-700 hover:border-slate-600 rounded-xl p-4 transition-all duration-200 hover:scale-105 cursor-pointer"
      style={{ display: 'block', textDecoration: 'none' }}
    >
      <div className="text-center">
        <div className="w-10 h-10 bg-slate-700/50 rounded-lg flex items-center justify-center mx-auto mb-3">
          <i className={`${icon} text-slate-300 text-lg`}></i>
        </div>
        <p className="text-white font-medium text-sm">{title}</p>
      </div>
    </a>
  )
}