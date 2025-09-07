import React, { useState, useEffect } from 'react'
import { useWebSocket } from '../hooks/useWebSocket'

export default function CustomerDashboard() {
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [customer, setCustomer] = useState(null)
  const [stats, setStats] = useState({
    active_repairs: 0,
    total_repairs: 0,
    notifications: 0,
    ready_for_pickup: 0
  })
  const [repairs, setRepairs] = useState([])
  const [notifications, setNotifications] = useState([])
  const [showNotifications, setShowNotifications] = useState(false)

  const { isConnected, messages } = useWebSocket(null, 'customer')

  useEffect(() => {
    // Fetch initial data
    Promise.all([
      fetch('/api/customer/stats/', { credentials: 'include' }).then(res => res.json()),
      fetch('/api/customer/repairs/', { credentials: 'include' }).then(res => res.json()),
      fetch('/api/customer/notifications/', { credentials: 'include' }).then(res => res.json())
    ])
    .then(([statsData, repairsData, notificationsData]) => {
      setStats(statsData)
      setRepairs(repairsData.results || repairsData)
      setNotifications(notificationsData.results || notificationsData)
      setLoading(false)
    })
    .catch(err => {
      console.error('Error fetching data:', err)
      setError('שגיאה בטעינת הנתונים')
      setLoading(false)
    })
  }, [])

  useEffect(() => {
    // Handle real-time updates
    messages.forEach(message => {
      if (message.type === 'repair_status_update' || message.type === 'notification') {
        // Refresh data when updates come in
        Promise.all([
          fetch('/api/customer/stats/', { credentials: 'include' }).then(res => res.json()),
          fetch('/api/customer/repairs/', { credentials: 'include' }).then(res => res.json()),
          fetch('/api/customer/notifications/', { credentials: 'include' }).then(res => res.json())
        ])
        .then(([statsData, repairsData, notificationsData]) => {
          setStats(statsData)
          setRepairs(repairsData.results || repairsData)
          setNotifications(notificationsData.results || notificationsData)
        })
        .catch(err => console.error('Error refreshing data:', err))
      }
    })
  }, [messages])

  const markNotificationAsRead = async (notificationId) => {
    try {
      await fetch(`/api/customer/notifications/${notificationId}/read/`, {
        method: 'POST',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]')?.value || ''
        }
      })
      
      // Update local state
      setNotifications(prev => prev.map(notif => 
        notif.id === notificationId ? { ...notif, is_read: true } : notif
      ))
      setStats(prev => ({ ...prev, notifications: prev.notifications - 1 }))
    } catch (error) {
      console.error('Error marking notification as read:', error)
    }
  }

  const getStatusColor = (status) => {
    const colors = {
      'completed': 'bg-green-500/20 text-green-300 border-green-500/30',
      'delivered': 'bg-green-600/20 text-green-200 border-green-600/30',
      'quality_approved': 'bg-emerald-500/20 text-emerald-300 border-emerald-500/30',
      'in_progress': 'bg-blue-500/20 text-blue-300 border-blue-500/30',
      'approved': 'bg-cyan-500/20 text-cyan-300 border-cyan-500/30',
      'diagnosed': 'bg-yellow-500/20 text-yellow-300 border-yellow-500/30',
      'partially_approved': 'bg-amber-500/20 text-amber-300 border-amber-500/30',
      'reported': 'bg-orange-500/20 text-orange-300 border-orange-500/30',
      'awaiting_quality_check': 'bg-purple-500/20 text-purple-300 border-purple-500/30'
    }
    return colors[status] || 'bg-gray-500/20 text-gray-300 border-gray-500/30'
  }

  const getActionButton = (repair) => {
    if (repair.status === 'diagnosed' || repair.status === 'partially_approved') {
      return (
        <a 
          href={`/repair/${repair.id}/approve/`}
          className="block mt-2 bg-green-500 hover:bg-green-600 text-white px-3 py-1 rounded text-xs transition-colors duration-200 text-center"
        >
          <i className="fas fa-check ml-1"></i>
          אשר
        </a>
      )
    }
    
    return (
      <a 
        href={`/repair/${repair.id}/status/`}
        className="block mt-2 bg-blue-500 hover:bg-blue-600 text-white px-3 py-1 rounded text-xs transition-colors duration-200 text-center"
      >
        <i className="fas fa-eye ml-1"></i>
        צפה
      </a>
    )
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin w-8 h-8 border-2 border-blue-500 border-t-transparent rounded-full mx-auto mb-4"></div>
          <p className="text-slate-400">טוען...</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 flex items-center justify-center">
        <div className="text-center">
          <i className="fas fa-exclamation-triangle text-red-400 text-4xl mb-4"></i>
          <p className="text-red-300">{error}</p>
          <button 
            onClick={() => window.location.reload()} 
            className="mt-4 bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-lg transition-colors"
          >
            נסה שוב
          </button>
        </div>
      </div>
    )
  }

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
              <h1 className="text-xl font-bold text-white">לוח הבקרה האישי</h1>
            </div>
            
            {/* Connection Status & Notifications */}
            <div className="flex items-center gap-4">
              <button 
                onClick={() => setShowNotifications(!showNotifications)}
                className="relative p-2 bg-slate-700/50 rounded-lg hover:bg-slate-700 transition-colors"
              >
                <i className="fas fa-bell text-slate-300"></i>
                {stats.notifications > 0 && (
                  <span className="absolute -top-1 -right-1 w-5 h-5 bg-red-500 text-white text-xs rounded-full flex items-center justify-center">
                    {stats.notifications}
                  </span>
                )}
              </button>
              
              <div className="flex items-center gap-2">
                <div className={`w-2 h-2 rounded-full ${isConnected ? 'bg-green-400' : 'bg-red-400'}`}></div>
                <span className="text-sm text-slate-400">
                  {isConnected ? 'מחובר' : 'מנותק'}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="container mx-auto px-4 py-8">
        {/* Welcome Section */}
        <div className="text-center mb-8">
          <h2 className="text-3xl font-bold text-white mb-2">שלום! 👋</h2>
          <p className="text-blue-200 text-lg">ברוך הבא לדשבורד האישי שלך</p>
        </div>

        {/* Quick Stats */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <StatCard
            icon="fas fa-tools"
            title="תיקונים פעילים"
            value={stats.active_repairs}
            color="blue"
          />
          <StatCard
            icon="fas fa-history"
            title="סה״כ תיקונים"
            value={stats.total_repairs}
            color="purple"
          />
          <StatCard
            icon="fas fa-bell"
            title="התראות חדשות"
            value={stats.notifications}
            color="red"
          />
          <StatCard
            icon="fas fa-check-circle"
            title="מוכן לאיסוף"
            value={stats.ready_for_pickup}
            color="green"
          />
        </div>

        {/* Notifications Panel (collapsible) */}
        {showNotifications && (
          <div className="bg-slate-800/50 backdrop-blur-sm border border-slate-700 rounded-xl p-6 mb-8">
            <h3 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
              <i className="fas fa-bell text-blue-400"></i>
              התראות אחרונות
            </h3>
            {notifications.length > 0 ? (
              <div className="space-y-3 max-h-64 overflow-y-auto">
                {notifications.slice(0, 10).map(notification => (
                  <div 
                    key={notification.id}
                    className={`p-3 rounded-lg border ${notification.is_read ? 'bg-slate-700/30 border-slate-600' : 'bg-blue-500/10 border-blue-500/30'}`}
                  >
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <h4 className="text-white font-medium">{notification.title}</h4>
                        <p className="text-slate-300 text-sm mt-1">{notification.message}</p>
                        <div className="flex items-center text-xs text-slate-400 mt-2">
                          <i className="fas fa-clock ml-1"></i>
                          {new Date(notification.created_at).toLocaleDateString('he-IL')}
                        </div>
                      </div>
                      {!notification.is_read && (
                        <button
                          onClick={() => markNotificationAsRead(notification.id)}
                          className="text-blue-400 hover:text-blue-300 text-sm"
                        >
                          סמן כנקרא
                        </button>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-slate-400">אין התראות חדשות</p>
            )}
          </div>
        )}

        {/* Quick Actions */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <ActionCard
            icon="fas fa-plus-circle"
            title="דיווח תיקון חדש"
            description="דווח על תקלה באופניים שלך"
            href="/customer/report/"
            color="bg-gradient-to-br from-red-500 to-red-600"
          />
          <ActionCard
            icon="fas fa-bicycle"
            title="רשימת אופניים"
            description="צפה וערוך את רשימת האופניים שלך"
            href="/my-bikes/"
            color="bg-gradient-to-br from-blue-500 to-blue-600"
          />
          <ActionCard
            icon="fas fa-plus"
            title="הוסף אופניים"
            description="הוסף אופניים חדשים למערכת"
            href="/my-bikes/add/"
            color="bg-gradient-to-br from-green-500 to-green-600"
          />
        </div>

        {/* Active Repairs */}
        {repairs.filter(r => !['completed', 'delivered'].includes(r.status)).length > 0 && (
          <div className="bg-slate-800/50 backdrop-blur-sm border border-slate-700 rounded-xl p-6 mb-8">
            <h3 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
              <i className="fas fa-tools text-blue-400"></i>
              תיקונים פעילים
            </h3>
            <div className="space-y-4">
              {repairs
                .filter(repair => !['completed', 'delivered'].includes(repair.status))
                .map(repair => (
                <RepairCard key={repair.id} repair={repair} getStatusColor={getStatusColor} getActionButton={getActionButton} />
              ))}
            </div>
          </div>
        )}

        {/* Repair History */}
        <div className="bg-slate-800/50 backdrop-blur-sm border border-slate-700 rounded-xl p-6">
          <h3 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
            <i className="fas fa-history text-purple-400"></i>
            היסטוריית תיקונים
          </h3>
          {repairs.length > 0 ? (
            <div className="space-y-4">
              {repairs.slice(0, 10).map(repair => (
                <RepairCard key={repair.id} repair={repair} getStatusColor={getStatusColor} getActionButton={getActionButton} />
              ))}
            </div>
          ) : (
            <div className="text-center py-12">
              <i className="fas fa-history text-6xl text-slate-600 mb-4"></i>
              <p className="text-slate-400 text-lg">אין היסטוריית תיקונים</p>
              <p className="text-slate-500 text-sm mb-6">התיקונים שלך יופיעו כאן</p>
              <a 
                href="/customer/report/"
                className="bg-red-500 hover:bg-red-600 text-white px-6 py-3 rounded-lg transition-colors duration-200 inline-flex items-center"
              >
                <i className="fas fa-wrench ml-2"></i>
                דווח על תקלה ראשונה
              </a>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

function StatCard({ icon, title, value, color }) {
  const colorClasses = {
    blue: 'from-blue-500/20 to-blue-600/20 border-blue-500/30 text-blue-400',
    purple: 'from-purple-500/20 to-purple-600/20 border-purple-500/30 text-purple-400',
    green: 'from-green-500/20 to-green-600/20 border-green-500/30 text-green-400',
    red: 'from-red-500/20 to-red-600/20 border-red-500/30 text-red-400'
  }

  return (
    <div className={`bg-gradient-to-br ${colorClasses[color]} backdrop-blur-sm border rounded-xl p-6`}>
      <div className="flex items-center justify-between">
        <div>
          <p className="text-slate-300 text-sm mb-1">{title}</p>
          <p className={`text-3xl font-bold ${colorClasses[color].split(' ')[2]}`}>{value}</p>
        </div>
        <div className={`w-12 h-12 bg-gradient-to-br ${colorClasses[color]} rounded-xl flex items-center justify-center`}>
          <i className={`${icon} ${colorClasses[color].split(' ')[2]} text-xl`}></i>
        </div>
      </div>
    </div>
  )
}

function ActionCard({ icon, title, description, href, color }) {
  return (
    <a 
      href={href}
      className={`block ${color} hover:scale-105 rounded-xl p-6 shadow-lg hover:shadow-xl transition-all duration-200`}
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

function RepairCard({ repair, getStatusColor, getActionButton }) {
  return (
    <div className="bg-slate-700/30 border border-slate-600 rounded-lg p-4 hover:bg-slate-700/50 transition-colors duration-200">
      <div className="flex justify-between items-start">
        <div className="flex-1">
          <div className="flex items-center mb-2">
            <span className="text-blue-300 font-medium">#{repair.id}</span>
            <span className="mx-2 text-slate-500">•</span>
            <span className="text-white font-medium">{repair.bike_info?.brand} {repair.bike_info?.model}</span>
          </div>
          
          {repair.problem_description && (
            <p className="text-slate-400 text-sm mb-2">
              {repair.problem_description.length > 80 ? 
                repair.problem_description.substring(0, 80) + '...' : 
                repair.problem_description
              }
            </p>
          )}
          
          <div className="flex items-center text-sm text-slate-500 mb-2">
            <i className="fas fa-calendar ml-1"></i>
            {new Date(repair.created_at).toLocaleDateString('he-IL')}
          </div>
          
          {repair.progress_percentage > 0 && (
            <div className="flex items-center text-sm text-slate-400">
              <i className="fas fa-tasks ml-1"></i>
              התקדמות: {Math.round(repair.progress_percentage)}%
              <div className="w-16 h-2 bg-slate-600 rounded-full ml-2">
                <div 
                  className="h-full bg-blue-500 rounded-full transition-all duration-300"
                  style={{ width: `${repair.progress_percentage}%` }}
                ></div>
              </div>
            </div>
          )}
        </div>
        
        <div className="text-left">
          <span className={`px-3 py-1 rounded-full text-xs font-medium border ${getStatusColor(repair.status)}`}>
            {repair.status_display}
          </span>
          {getActionButton(repair)}
        </div>
      </div>
    </div>
  )
}