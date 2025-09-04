import React, { useState, useEffect } from 'react'

export default function CustomerApproval({ repairId }) {
  const [repairData, setRepairData] = useState(null)
  const [selectedItems, setSelectedItems] = useState(new Set())
  const [confirmed, setConfirmed] = useState(false)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [submitting, setSubmitting] = useState(false)

  useEffect(() => {
    fetchRepairData()
  }, [repairId])

  const fetchRepairData = async () => {
    try {
      setLoading(true)
      const response = await fetch(`/api/customer/repairs/${repairId}/`)
      if (!response.ok) throw new Error('Failed to fetch repair data')
      
      const data = await response.json()
      setRepairData(data)
      
      // Pre-select already approved items
      const preSelected = new Set()
      data.repair_items?.forEach(item => {
        if (item.is_approved_by_customer) {
          preSelected.add(item.id)
        }
      })
      setSelectedItems(preSelected)
      
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const handleItemToggle = (itemId) => {
    const newSelected = new Set(selectedItems)
    if (newSelected.has(itemId)) {
      newSelected.delete(itemId)
    } else {
      newSelected.add(itemId)
    }
    setSelectedItems(newSelected)
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (selectedItems.size === 0 || !confirmed) return
    
    setSubmitting(true)
    try {
      const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value
      
      const response = await fetch(window.location.pathname, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
          'X-CSRFToken': csrfToken
        },
        body: new URLSearchParams({
          approved_items: Array.from(selectedItems),
          csrfmiddlewaretoken: csrfToken
        })
      })
      
      if (response.ok) {
        // Show success and redirect
        showSuccessMessage('הפעולות אושרו בהצלחה!')
        setTimeout(() => {
          window.location.href = '/'
        }, 2000)
      } else {
        throw new Error('Failed to submit approval')
      }
    } catch (err) {
      setError('שגיאה בשליחת האישור')
    } finally {
      setSubmitting(false)
    }
  }

  const showSuccessMessage = (message) => {
    const div = document.createElement('div')
    div.className = 'fixed top-4 right-4 bg-green-500 text-white px-6 py-3 rounded-lg shadow-lg z-50'
    div.innerHTML = `<i class="fas fa-check mr-2"></i>${message}`
    document.body.appendChild(div)
    
    setTimeout(() => {
      if (document.body.contains(div)) {
        document.body.removeChild(div)
      }
    }, 3000)
  }

  const calculateTotal = () => {
    if (!repairData?.repair_items) return { count: 0, total: 0 }
    
    let total = 0
    let count = 0
    
    repairData.repair_items.forEach(item => {
      if (selectedItems.has(item.id)) {
        total += parseFloat(item.price || 0)
        count++
      }
    })
    
    return { count, total }
  }

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('he-IL', {
      day: '2-digit',
      month: '2-digit',
      hour: '2-digit',
      minute: '2-digit'
    })
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin w-8 h-8 border-2 border-blue-500 border-t-transparent rounded-full mx-auto mb-4"></div>
          <p className="text-slate-400">טוען פרטי התיקון...</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 flex items-center justify-center">
        <div className="text-center max-w-md mx-auto p-6">
          <div className="w-16 h-16 bg-red-500/20 rounded-full flex items-center justify-center mx-auto mb-4">
            <i className="fas fa-exclamation-triangle text-red-400 text-2xl"></i>
          </div>
          <h3 className="text-white font-bold text-xl mb-2">שגיאה בטעינת הנתונים</h3>
          <p className="text-slate-400 mb-6">{error}</p>
          <button 
            onClick={fetchRepairData}
            className="bg-blue-500 hover:bg-blue-600 text-white px-6 py-2 rounded-lg transition-colors"
          >
            נסה שוב
          </button>
        </div>
      </div>
    )
  }

  if (!repairData) return null

  const { count, total } = calculateTotal()
  const canSubmit = count > 0 && confirmed && !submitting

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        
        {/* Clean Header */}
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-white mb-2">
            אישור תיקון #{repairData.id}
          </h1>
          <p className="text-slate-400">
            בחר את הפעולות שברצונך לאשר לביצוע
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          
          {/* Left Column - Repair Info */}
          <div className="lg:col-span-1">
            <div className="bg-slate-800/40 backdrop-blur-sm border border-slate-700 rounded-xl p-6">
              <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
                <i className="fas fa-info-circle text-blue-400"></i>
                פרטי התיקון
              </h3>
              
              <div className="space-y-4">
                <div className="flex items-center gap-3 p-3 bg-slate-700/50 rounded-lg">
                  <div className="w-10 h-10 bg-blue-500/20 rounded-lg flex items-center justify-center">
                    <i className="fas fa-bicycle text-blue-400"></i>
                  </div>
                  <div>
                    <div className="text-white font-medium">{repairData.bike_info?.brand} {repairData.bike_info?.model}</div>
                    <div className="text-slate-400 text-sm">לקוח: {repairData.bike_info?.customer_name}</div>
                  </div>
                </div>

                <div className="space-y-2 text-sm">
                  <div className="flex justify-between">
                    <span className="text-slate-400">תאריך דיווח:</span>
                    <span className="text-white">{formatDate(repairData.created_at)}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-slate-400">סטטוס:</span>
                    <span className="text-green-400">{repairData.status_display}</span>
                  </div>
                </div>

                {repairData.problem_description && (
                  <div>
                    <h4 className="text-white font-medium mb-2">תיאור התקלה:</h4>
                    <div className="bg-slate-700/50 rounded-lg p-3">
                      <p className="text-slate-300 text-sm">{repairData.problem_description}</p>
                    </div>
                  </div>
                )}

                {repairData.diagnosis && (
                  <div>
                    <h4 className="text-white font-medium mb-2">אבחון המוסך:</h4>
                    <div className="bg-blue-500/10 border border-blue-500/30 rounded-lg p-3">
                      <p className="text-blue-100 text-sm">{repairData.diagnosis}</p>
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>

          {/* Right Column - Main Content */}
          <div className="lg:col-span-2">
            <form onSubmit={handleSubmit}>
              
              {/* Repair Items */}
              {repairData.repair_items && repairData.repair_items.length > 0 ? (
                <div className="bg-slate-800/40 backdrop-blur-sm border border-slate-700 rounded-xl p-6 mb-6">
                  <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
                    <i className="fas fa-tools text-blue-400"></i>
                    פעולות תיקון מוצעות
                  </h3>
                  
                  <div className="space-y-3">
                    {repairData.repair_items.map((item) => (
                      <div key={item.id} 
                           className={`border rounded-lg p-4 transition-all duration-200 cursor-pointer hover:shadow-md ${
                             selectedItems.has(item.id)
                               ? 'border-blue-500 bg-blue-500/10'
                               : 'border-slate-600 bg-slate-700/30 hover:border-slate-500'
                           }`}
                           onClick={() => handleItemToggle(item.id)}>
                        
                        <div className="flex items-start gap-3">
                          <div className="flex-shrink-0 mt-1">
                            <div className={`w-5 h-5 rounded border-2 flex items-center justify-center ${
                              selectedItems.has(item.id)
                                ? 'border-blue-500 bg-blue-500'
                                : 'border-slate-500'
                            }`}>
                              {selectedItems.has(item.id) && (
                                <i className="fas fa-check text-white text-xs"></i>
                              )}
                            </div>
                          </div>
                          
                          <div className="flex-1">
                            <div className="flex items-start justify-between gap-4">
                              <div className="flex-1">
                                <h4 className="text-white font-medium mb-1">{item.description}</h4>
                                {item.notes && (
                                  <p className="text-slate-400 text-sm">{item.notes}</p>
                                )}
                              </div>
                              <div className="text-right">
                                <div className="text-xl font-bold text-white">₪{item.price}</div>
                              </div>
                            </div>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              ) : (
                <div className="bg-slate-800/40 backdrop-blur-sm border border-slate-700 rounded-xl p-8 mb-6 text-center">
                  <div className="w-16 h-16 bg-yellow-500/20 rounded-full flex items-center justify-center mx-auto mb-4">
                    <i className="fas fa-clock text-yellow-400 text-2xl"></i>
                  </div>
                  <h3 className="text-white font-bold text-lg mb-2">המתן לאבחון המוסך</h3>
                  <p className="text-slate-400">המוסך עדיין לא הוסיף פעולות לתיקון זה</p>
                </div>
              )}

              {/* Summary & Confirmation */}
              {repairData.repair_items && repairData.repair_items.length > 0 && (
                <>
                  {/* Summary */}
                  <div className="bg-slate-800/40 backdrop-blur-sm border border-slate-700 rounded-xl p-6 mb-6">
                    <h3 className="text-lg font-semibold text-white mb-4">סיכום</h3>
                    <div className="grid grid-cols-2 gap-4">
                      <div className="text-center p-4 bg-slate-700/50 rounded-lg">
                        <div className="text-2xl font-bold text-blue-400">{count}</div>
                        <div className="text-slate-400 text-sm">פעולות נבחרו</div>
                      </div>
                      <div className="text-center p-4 bg-slate-700/50 rounded-lg">
                        <div className="text-2xl font-bold text-green-400">₪{total.toFixed(2)}</div>
                        <div className="text-slate-400 text-sm">סה״כ מחיר</div>
                      </div>
                    </div>
                  </div>

                  {/* Confirmation */}
                  <div className="bg-slate-800/40 backdrop-blur-sm border border-slate-700 rounded-xl p-6 mb-6">
                    <div className="flex items-start gap-3">
                      <div className="flex-shrink-0 mt-1">
                        <div 
                          className={`w-5 h-5 rounded border-2 flex items-center justify-center cursor-pointer ${
                            confirmed ? 'border-green-500 bg-green-500' : 'border-slate-500'
                          }`}
                          onClick={() => setConfirmed(!confirmed)}>
                          {confirmed && <i className="fas fa-check text-white text-xs"></i>}
                        </div>
                      </div>
                      <div className="flex-1">
                        <h4 className="text-white font-medium mb-2">אישור ביצוע</h4>
                        <div className="text-slate-300 text-sm space-y-1">
                          <p>• אני מאשר/ת את ביצוע הפעולות שנבחרו</p>
                          <p>• אני מסכים/ה לתשלום הסכום המוצג</p>
                          <p>• אני מבין/ה שלא ניתן לבטל לאחר האישור</p>
                        </div>
                      </div>
                    </div>
                  </div>

                  {/* Submit Button */}
                  <div className="flex flex-col sm:flex-row gap-4">
                    <button
                      type="submit"
                      disabled={!canSubmit}
                      className={`flex-1 py-4 px-6 rounded-lg font-semibold transition-all ${
                        canSubmit
                          ? 'bg-green-500 hover:bg-green-600 text-white shadow-lg hover:shadow-xl'
                          : 'bg-slate-600 text-slate-400 cursor-not-allowed'
                      }`}>
                      {submitting ? (
                        <>
                          <i className="fas fa-spinner fa-spin mr-2"></i>
                          שולח אישור...
                        </>
                      ) : (
                        <>
                          <i className="fas fa-check mr-2"></i>
                          אשר פעולות ({count})
                        </>
                      )}
                    </button>
                    
                    <a href="/" 
                       className="flex-1 py-4 px-6 bg-slate-600 hover:bg-slate-500 text-white text-center rounded-lg font-semibold transition-colors">
                      <i className="fas fa-home mr-2"></i>
                      חזרה לדף הבית
                    </a>
                  </div>
                </>
              )}
            </form>
          </div>
        </div>
      </div>

      {/* Hidden CSRF token */}
      <form method="post" style={{display: 'none'}}>
        <input type="hidden" name="csrfmiddlewaretoken" value={document.querySelector('[name=csrfmiddlewaretoken]')?.value} />
      </form>
    </div>
  )
}