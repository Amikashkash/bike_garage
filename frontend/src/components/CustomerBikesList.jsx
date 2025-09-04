import React, { useState, useEffect } from 'react'

export default function CustomerBikesList() {
  const [bikesData, setBikesData] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  // Fetch repairs data and group by bikes
  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true)
        const response = await fetch('/api/customer/repairs/')
        if (!response.ok) {
          throw new Error('Failed to fetch data')
        }
        const responseData = await response.json()
        
        // Handle different response formats (DRF pagination vs direct array)
        const repairsData = responseData.results || responseData || []
        
        // Group repairs by bike
        const bikesMap = new Map()
        
        if (Array.isArray(repairsData)) {
          repairsData.forEach(repair => {
            const bike = repair.bike_info
            const bikeId = bike.id
            
            if (!bikesMap.has(bikeId)) {
              bikesMap.set(bikeId, {
                id: bike.id,
                brand: bike.brand,
                model: bike.model || '',
                color: bike.color || '',
                created_at: repair.created_at, // We'll use the first repair date as approximation
                repairs: []
              })
            }
            
            bikesMap.get(bikeId).repairs.push({
              id: repair.id,
              status: repair.status,
              status_display: repair.status_display,
              problem_description: repair.problem_description,
              created_at: repair.created_at
            })
          })
        } else {
          console.log('Unexpected response format:', responseData)
        }
        
        setBikesData(Array.from(bikesMap.values()))
        
      } catch (err) {
        console.error('Error fetching bikes data:', err)
        setError(err.message)
      } finally {
        setLoading(false)
      }
    }

    fetchData()
  }, [])

  // Statistics calculations
  const stats = {
    totalBikes: bikesData.length,
    totalRepairs: bikesData.reduce((total, bike) => total + bike.repairs.length, 0),
    inProgressRepairs: bikesData.reduce((total, bike) => 
      total + bike.repairs.filter(repair => repair.status === 'in_progress').length, 0
    ),
    completedRepairs: bikesData.reduce((total, bike) => 
      total + bike.repairs.filter(repair => repair.status === 'completed').length, 0
    )
  }

  // Get color style for bike color indicator
  const getColorStyle = (color) => {
    if (!color) return {}
    const colorLower = color.toLowerCase()
    
    const colorMap = {
      'שחור': '#000000',
      'לבן': '#ffffff',
      'אדום': '#ef4444',
      'כחול': '#3b82f6',
      'ירוק': '#22c55e',
      'כתום': '#f97316',
      'צהוב': '#eab308',
      'סגול': '#a855f7'
    }
    
    return { backgroundColor: colorMap[color] || colorLower }
  }

  // Get status badge styling
  const getStatusBadgeStyle = (status) => {
    const statusStyles = {
      'completed': 'bg-green-500/10 border-green-500/30 text-green-400',
      'in_progress': 'bg-blue-500/10 border-blue-500/30 text-blue-400', 
      'diagnosed': 'bg-amber-500/10 border-amber-500/30 text-amber-400',
      'pending_approval': 'bg-purple-500/10 border-purple-500/30 text-purple-400'
    }
    
    return statusStyles[status] || 'bg-slate-500/10 border-slate-500/30 text-slate-400'
  }

  // Get status icon
  const getStatusIcon = (status) => {
    const statusIcons = {
      'completed': 'fas fa-check-circle',
      'in_progress': 'fas fa-cog fa-spin', 
      'diagnosed': 'fas fa-stethoscope',
      'pending_approval': 'fas fa-clock'
    }
    
    return statusIcons[status] || 'fas fa-hourglass-half'
  }

  // Format date
  const formatDate = (dateString) => {
    const date = new Date(dateString)
    return date.toLocaleDateString('he-IL')
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin w-8 h-8 border-2 border-blue-500 border-t-transparent rounded-full mx-auto mb-4"></div>
          <p className="text-slate-400">טוען את האופניים שלך...</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900 flex items-center justify-center">
        <div className="text-center">
          <div className="w-16 h-16 bg-red-500/20 rounded-full flex items-center justify-center mx-auto mb-4">
            <i className="fas fa-exclamation-triangle text-red-400 text-2xl"></i>
          </div>
          <h3 className="text-white font-bold text-xl mb-2">שגיאה בטעינת הנתונים</h3>
          <p className="text-slate-400 mb-4">{error}</p>
          <button 
            onClick={() => window.location.reload()} 
            className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-lg transition-colors"
          >
            נסה שוב
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-6 sm:py-8">
        
        {/* Header Section */}
        <div className="text-center mb-6 sm:mb-8">
          <div className="mb-6">
            <h1 className="text-3xl sm:text-4xl lg:text-5xl font-bold bg-gradient-to-r from-blue-500 via-cyan-500 to-purple-500 bg-clip-text text-transparent mb-4">
              🚲 האופניים שלי
              <span className="text-2xl sm:text-3xl lg:text-4xl text-blue-300">⚙️</span>
            </h1>
            <p className="text-slate-300 text-base sm:text-lg max-w-2xl mx-auto leading-relaxed">
              ניהול ומעקב אחר האופניים שלך - כל המידע במקום אחד
            </p>
          </div>
        </div>
        
        {/* Action Bar */}
        <div className="flex flex-col sm:flex-row justify-between items-center gap-4 mb-6 sm:mb-8">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-blue-500/20 rounded-xl flex items-center justify-center">
              <i className="fas fa-bicycle text-blue-400"></i>
            </div>
            <h2 className="text-xl sm:text-2xl font-bold text-white">האופניים שלי</h2>
            {bikesData.length > 0 && (
              <span className="bg-blue-500/20 border border-blue-400/30 rounded-lg px-3 py-1 text-blue-300 text-sm font-medium">
                {bikesData.length} אופניים
              </span>
            )}
          </div>
          
          <div className="flex gap-3">
            <a href="/my-bikes/add/" 
               className="bg-gradient-to-r from-green-500 to-emerald-600 hover:from-green-600 hover:to-emerald-700 text-white font-semibold py-3 px-6 rounded-xl transition-all duration-300 shadow-lg hover:shadow-xl transform hover:scale-105 active:scale-95">
              <i className="fas fa-plus mr-2"></i>
              <span className="hidden sm:inline">הוסף אופניים</span>
              <span className="sm:hidden">הוסף</span>
            </a>
            <a href="/customer/report/" 
               className="bg-gradient-to-r from-orange-500 to-red-600 hover:from-orange-600 hover:to-red-700 text-white font-semibold py-3 px-6 rounded-xl transition-all duration-300 shadow-lg hover:shadow-xl transform hover:scale-105 active:scale-95">
              <i className="fas fa-exclamation-triangle mr-2"></i>
              <span className="hidden sm:inline">דווח תקלה</span>
              <span className="sm:hidden">דווח</span>
            </a>
          </div>
        </div>
        
        {bikesData.length > 0 ? (
          <>
            {/* Bikes Grid */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
              {bikesData.map((bike, index) => (
                <div key={bike.id} 
                     className="bike-card bg-slate-800/40 backdrop-blur-xl border border-blue-400/30 rounded-2xl shadow-2xl overflow-hidden hover:border-blue-400/50 hover:bg-slate-800/50 hover:-translate-y-1 lg:hover:-translate-y-1 transition-all duration-300 opacity-0 animate-fadeInUp"
                     style={{ animationDelay: `${index * 100}ms`, animationFillMode: 'forwards' }}>
                  
                  {/* Bike Header */}
                  <div className="border-b border-slate-600/30 p-4 sm:p-6">
                    <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
                      <div className="flex items-center gap-3">
                        <div className="flex-shrink-0 w-12 h-12 bg-gradient-to-br from-blue-500 to-cyan-500 rounded-xl flex items-center justify-center shadow-lg">
                          <i className="fas fa-bicycle text-white text-lg"></i>
                        </div>
                        <div>
                          <h3 className="text-lg font-bold text-white">
                            {bike.brand} {bike.model}
                          </h3>
                          <p className="text-slate-400 text-sm">נרשם ב-{formatDate(bike.created_at)}</p>
                        </div>
                      </div>
                      {bike.color && (
                        <div className="flex items-center gap-2">
                          <div className="w-4 h-4 rounded-full border-2 border-white/20" 
                               style={getColorStyle(bike.color)}></div>
                          <span className="bg-slate-700/50 border border-slate-600/50 rounded-lg px-3 py-1 text-slate-200 text-sm font-medium">
                            {bike.color}
                          </span>
                        </div>
                      )}
                    </div>
                  </div>
                  
                  {/* Bike Details */}
                  <div className="p-4 sm:p-6">
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-6">
                      <div className="bike-detail-item bg-slate-700/30 border border-slate-600/30 rounded-lg p-3">
                        <div className="flex items-center gap-2 text-sm">
                          <i className="fas fa-industry text-orange-400"></i>
                          <span className="text-slate-400">יצרן:</span>
                          <span className="text-white font-medium">{bike.brand}</span>
                        </div>
                      </div>
                      
                      {bike.model && (
                        <div className="bike-detail-item bg-slate-700/30 border border-slate-600/30 rounded-lg p-3">
                          <div className="flex items-center gap-2 text-sm">
                            <i className="fas fa-tag text-cyan-400"></i>
                            <span className="text-slate-400">מודל:</span>
                            <span className="text-white font-medium">{bike.model}</span>
                          </div>
                        </div>
                      )}
                    </div>
                    
                    {/* Repairs Section */}
                    {bike.repairs.length > 0 ? (
                      <div className="bike-repairs-section">
                        <div className="flex items-center justify-between mb-4">
                          <h4 className="text-white font-semibold flex items-center gap-2">
                            <i className="fas fa-tools text-orange-400"></i>
                            תיקונים
                          </h4>
                          <span className="bg-orange-500/20 border border-orange-400/30 rounded-lg px-2 py-1 text-orange-300 text-xs font-medium">
                            {bike.repairs.length} תיקונים
                          </span>
                        </div>
                        
                        <div className="space-y-3 max-h-60 overflow-y-auto">
                          {bike.repairs.map((repair) => (
                            <div key={repair.id} className="repair-item bg-slate-800/50 border border-slate-600/40 rounded-lg p-3 hover:border-slate-500/60 hover:bg-slate-700/70 hover:-translate-x-1 transition-all duration-300">
                              <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2 mb-2">
                                <div className="flex items-center gap-3">
                                  <span className={`repair-status-badge inline-flex items-center px-2 py-1 rounded-lg text-xs font-semibold border ${getStatusBadgeStyle(repair.status)}`}>
                                    <i className={`${getStatusIcon(repair.status)} mr-1`}></i>
                                    {repair.status_display}
                                  </span>
                                  <span className="text-slate-400 text-xs">{formatDate(repair.created_at)}</span>
                                </div>
                                <a href={`/repair-status/${repair.id}/`} 
                                   className="bg-blue-500/20 hover:bg-blue-500/30 border border-blue-400/40 hover:border-blue-400/60 text-blue-300 px-3 py-1 rounded-lg text-xs font-medium transition-all duration-300 flex items-center gap-1">
                                  <i className="fas fa-eye"></i>
                                  <span>צפה</span>
                                </a>
                              </div>
                              
                              {repair.problem_description && (
                                <div className="repair-description">
                                  <p className="text-slate-300 text-sm leading-relaxed">
                                    "{repair.problem_description.length > 60 
                                      ? repair.problem_description.substring(0, 60) + '...'
                                      : repair.problem_description}"
                                  </p>
                                </div>
                              )}
                            </div>
                          ))}
                        </div>
                      </div>
                    ) : (
                      <div className="no-repairs-section text-center py-6">
                        <div className="w-16 h-16 bg-slate-700/30 rounded-2xl flex items-center justify-center mx-auto mb-4">
                          <i className="fas fa-tools text-slate-500 text-2xl"></i>
                        </div>
                        <h5 className="text-white font-medium mb-2">אין תיקונים עדיין</h5>
                        <p className="text-slate-400 text-sm mb-4">האופניים שלך עדיין לא נדרשו לתיקון</p>
                        <a href="/customer/report/" 
                           className="bg-gradient-to-r from-orange-500 to-red-500 hover:from-orange-600 hover:to-red-600 text-white font-medium py-2 px-4 rounded-lg transition-all duration-300 text-sm inline-flex items-center gap-2">
                          <i className="fas fa-plus"></i>
                          דווח תקלה
                        </a>
                      </div>
                    )}
                  </div>
                </div>
              ))}
            </div>

            {/* Statistics Section */}
            <div className="bg-slate-800/40 backdrop-blur-xl border border-purple-400/30 rounded-2xl shadow-2xl p-4 sm:p-6 mb-8 hover:bg-slate-800/50 hover:-translate-y-1 transition-all duration-300">
              <div className="flex items-center gap-3 mb-4">
                <div className="w-10 h-10 bg-purple-500/20 rounded-xl flex items-center justify-center">
                  <i className="fas fa-chart-bar text-purple-400"></i>
                </div>
                <h3 className="text-lg font-bold text-white">סטטיסטיקות</h3>
              </div>
              
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
                <div className="stat-item text-center p-4 bg-slate-700/30 border border-slate-600/50 rounded-xl hover:bg-slate-700/50 hover:border-slate-600/70 hover:-translate-y-1 transition-all duration-300">
                  <div className="text-2xl font-bold text-blue-300">{stats.totalBikes}</div>
                  <div className="text-slate-400 text-sm">אופניים</div>
                </div>
                <div className="stat-item text-center p-4 bg-slate-700/30 border border-slate-600/50 rounded-xl hover:bg-slate-700/50 hover:border-slate-600/70 hover:-translate-y-1 transition-all duration-300">
                  <div className="text-2xl font-bold text-green-300">{stats.totalRepairs}</div>
                  <div className="text-slate-400 text-sm">תיקונים</div>
                </div>
                <div className="stat-item text-center p-4 bg-slate-700/30 border border-slate-600/50 rounded-xl hover:bg-slate-700/50 hover:border-slate-600/70 hover:-translate-y-1 transition-all duration-300">
                  <div className="text-2xl font-bold text-orange-300">{stats.inProgressRepairs}</div>
                  <div className="text-slate-400 text-sm">בתיקון</div>
                </div>
                <div className="stat-item text-center p-4 bg-slate-700/30 border border-slate-600/50 rounded-xl hover:bg-slate-700/50 hover:border-slate-600/70 hover:-translate-y-1 transition-all duration-300">
                  <div className="text-2xl font-bold text-purple-300">{stats.completedRepairs}</div>
                  <div className="text-slate-400 text-sm">הושלמו</div>
                </div>
              </div>
            </div>
          </>
        ) : (
          /* Empty State */
          <div className="text-center py-16">
            <div className="bg-slate-800/40 backdrop-blur-xl border border-slate-600/40 rounded-2xl p-8 sm:p-12 max-w-lg mx-auto hover:bg-slate-800/50 hover:-translate-y-1 transition-all duration-300">
              <div className="w-24 h-24 bg-gradient-to-br from-blue-500/20 to-cyan-500/20 rounded-2xl flex items-center justify-center mx-auto mb-6">
                <i className="fas fa-bicycle text-blue-400 text-4xl"></i>
              </div>
              <h3 className="text-2xl font-bold text-white mb-4">אין לך אופניים רשומים במערכת</h3>
              <p className="text-slate-400 mb-8 leading-relaxed">
                תוכל להוסיף אופניים חדשים על ידי לחיצה על הכפתור למטה.<br/>
                לאחר ההוספה תוכל לדווח על תקלות ולעקוב אחר תיקונים.
              </p>
              <div className="flex flex-col sm:flex-row gap-4 justify-center">
                <a href="/my-bikes/add/" 
                   className="bg-gradient-to-r from-green-500 to-emerald-600 hover:from-green-600 hover:to-emerald-700 text-white font-semibold py-3 px-6 rounded-xl transition-all duration-300 shadow-lg hover:shadow-xl transform hover:scale-105 active:scale-95">
                  <i className="fas fa-plus mr-2"></i>
                  הוסף אופניים ראשונים
                </a>
                <a href="/" 
                   className="bg-slate-600/50 hover:bg-slate-600/70 text-slate-200 font-semibold py-3 px-6 rounded-xl transition-all duration-300 border border-slate-500/30 hover:border-slate-400/50">
                  <i className="fas fa-home mr-2"></i>
                  חזרה לדף הבית
                </a>
              </div>
            </div>
          </div>
        )}
        
        {/* Back to Home */}
        <div className="text-center">
          <a href="/" 
             className="bg-slate-600/50 hover:bg-slate-600/70 text-slate-200 font-semibold py-3 px-6 rounded-xl transition-all duration-300 border border-slate-500/30 hover:border-slate-400/50">
            <i className="fas fa-home mr-2"></i>
            חזרה לדף הבית
          </a>
        </div>
      </div>
      
      <style jsx>{`
        @keyframes fadeInUp {
          from {
            opacity: 0;
            transform: translateY(20px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }
        
        .animate-fadeInUp {
          animation: fadeInUp 0.6s ease-out;
        }
        
        .space-y-3::-webkit-scrollbar {
          width: 4px;
        }
        .space-y-3::-webkit-scrollbar-track {
          background: rgba(51, 65, 85, 0.3);
          border-radius: 0.375rem;
        }
        .space-y-3::-webkit-scrollbar-thumb {
          background: rgba(71, 85, 105, 0.5);
          border-radius: 0.375rem;
        }
        .space-y-3::-webkit-scrollbar-thumb:hover {
          background: rgba(71, 85, 105, 0.7);
        }
      `}</style>
    </div>
  )
}