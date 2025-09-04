import React, { useState, useEffect, useRef } from 'react'

export default function CustomerAddBike() {
  const [formData, setFormData] = useState({
    brand: '',
    model: '',
    color: ''
  })
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [errors, setErrors] = useState({})
  const brandInputRef = useRef(null)

  // Popular colors for quick selection
  const popularColors = [
    { name: 'שחור', bg: 'bg-black', textColor: 'text-white' },
    { name: 'לבן', bg: 'bg-white', textColor: 'text-black' },
    { name: 'אדום', bg: 'bg-red-500', textColor: 'text-white' },
    { name: 'כחול', bg: 'bg-blue-500', textColor: 'text-white' },
    { name: 'ירוק', bg: 'bg-green-500', textColor: 'text-white' },
    { name: 'כתום', bg: 'bg-orange-500', textColor: 'text-white' },
    { name: 'צהוב', bg: 'bg-yellow-400', textColor: 'text-black' },
    { name: 'סגול', bg: 'bg-purple-500', textColor: 'text-white' }
  ]

  const [selectedColorIndex, setSelectedColorIndex] = useState(-1)

  // Auto-focus first field
  useEffect(() => {
    const timer = setTimeout(() => {
      if (brandInputRef.current) {
        brandInputRef.current.focus()
      }
    }, 500)
    return () => clearTimeout(timer)
  }, [])

  // Load draft from localStorage
  useEffect(() => {
    const savedDraft = {
      brand: localStorage.getItem('bike_draft_brand') || '',
      model: localStorage.getItem('bike_draft_model') || '',
      color: localStorage.getItem('bike_draft_color') || ''
    }
    
    if (savedDraft.brand || savedDraft.model || savedDraft.color) {
      setFormData(savedDraft)
    }
  }, [])

  // Auto-save draft
  const saveToDraft = (field, value) => {
    localStorage.setItem(`bike_draft_${field}`, value)
  }

  const handleInputChange = (field, value) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }))
    saveToDraft(field, value)
    
    // Clear error when user starts typing
    if (errors[field]) {
      setErrors(prev => ({
        ...prev,
        [field]: null
      }))
    }
  }

  const handleColorSelect = (colorName, index) => {
    handleInputChange('color', colorName)
    setSelectedColorIndex(index)
    
    // Visual feedback animation
    const colorInput = document.getElementById('color-input')
    if (colorInput) {
      colorInput.classList.add('scale-105')
      setTimeout(() => {
        colorInput.classList.remove('scale-105')
      }, 200)
    }
  }

  const validateForm = () => {
    const newErrors = {}
    
    if (!formData.brand.trim()) {
      newErrors.brand = 'חובה למלא שם יצרן'
    }
    
    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    
    if (!validateForm()) {
      // Focus on first error field
      if (errors.brand && brandInputRef.current) {
        brandInputRef.current.focus()
        brandInputRef.current.style.borderColor = '#ef4444'
        brandInputRef.current.style.boxShadow = '0 0 0 3px rgba(239, 68, 68, 0.1)'
        
        setTimeout(() => {
          brandInputRef.current.style.borderColor = ''
          brandInputRef.current.style.boxShadow = ''
        }, 2000)
      }
      return
    }
    
    setIsSubmitting(true)
    
    try {
      // Get CSRF token
      const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value
      
      const response = await fetch(window.location.pathname, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
          'X-CSRFToken': csrfToken
        },
        body: new URLSearchParams({
          brand: formData.brand,
          model: formData.model,
          color: formData.color,
          csrfmiddlewaretoken: csrfToken
        })
      })
      
      if (response.ok) {
        // Clear draft
        localStorage.removeItem('bike_draft_brand')
        localStorage.removeItem('bike_draft_model')
        localStorage.removeItem('bike_draft_color')
        
        // Show success message
        showSuccessMessage('אופניים נוספו בהצלחה!')
        
        // Redirect after short delay
        setTimeout(() => {
          window.location.href = '/my-bikes/'
        }, 1500)
      } else {
        // Handle form errors from server
        const text = await response.text()
        const parser = new DOMParser()
        const doc = parser.parseFromString(text, 'text/html')
        
        // Extract errors from Django form
        const formErrors = {}
        const errorElements = doc.querySelectorAll('.form-error')
        errorElements.forEach(el => {
          const fieldName = el.getAttribute('data-field') || 'brand'
          formErrors[fieldName] = el.textContent.trim()
        })
        
        if (Object.keys(formErrors).length > 0) {
          setErrors(formErrors)
        } else {
          throw new Error('Failed to add bike')
        }
      }
    } catch (error) {
      console.error('Error adding bike:', error)
      showErrorMessage('אירעה שגיאה בהוספת האופניים')
    } finally {
      setIsSubmitting(false)
    }
  }

  const showSuccessMessage = (message) => {
    const successDiv = document.createElement('div')
    successDiv.className = 'fixed top-4 right-4 bg-green-500 text-white px-6 py-3 rounded-lg shadow-lg z-50 transition-all duration-300'
    successDiv.innerHTML = `<i class="fas fa-check mr-2"></i>${message}`
    document.body.appendChild(successDiv)
    
    setTimeout(() => {
      if (document.body.contains(successDiv)) {
        document.body.removeChild(successDiv)
      }
    }, 3000)
  }

  const showErrorMessage = (message) => {
    const errorDiv = document.createElement('div')
    errorDiv.className = 'fixed top-4 right-4 bg-red-500 text-white px-6 py-3 rounded-lg shadow-lg z-50 transition-all duration-300'
    errorDiv.innerHTML = `<i class="fas fa-exclamation-triangle mr-2"></i>${message}`
    document.body.appendChild(errorDiv)
    
    setTimeout(() => {
      if (document.body.contains(errorDiv)) {
        document.body.removeChild(errorDiv)
      }
    }, 3000)
  }

  // Keyboard shortcuts
  useEffect(() => {
    const handleKeyDown = (e) => {
      // Ctrl/Cmd + Enter to submit
      if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        e.preventDefault()
        handleSubmit(e)
      }
      
      // Escape to cancel
      if (e.key === 'Escape') {
        window.location.href = '/my-bikes/'
      }
    }
    
    document.addEventListener('keydown', handleKeyDown)
    return () => document.removeEventListener('keydown', handleKeyDown)
  }, [formData])

  const getInputIndicatorClass = (field) => {
    if (!formData[field]) return 'opacity-0'
    if (errors[field]) return 'opacity-100 bg-red-400'
    return 'opacity-100 bg-emerald-400'
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-emerald-900 to-slate-900">
      <div className="max-w-2xl mx-auto px-4 sm:px-6 lg:px-8 py-6 sm:py-8">
        
        {/* Header Section */}
        <div className="text-center mb-6 sm:mb-8">
          <div className="mb-6">
            <h1 className="text-3xl sm:text-4xl lg:text-5xl font-bold bg-gradient-to-r from-emerald-500 via-cyan-500 to-purple-500 bg-clip-text text-transparent mb-4">
              🚲 הוסף אופניים חדשים
              <span className="text-2xl sm:text-3xl lg:text-4xl text-emerald-300">✨</span>
            </h1>
            <p className="text-slate-300 text-base sm:text-lg max-w-2xl mx-auto leading-relaxed">
              הוסף אופניים חדשים למערכת ותתחיל לעקוב אחר התיקונים שלהם
            </p>
          </div>
        </div>
        
        {/* Main Form Card */}
        <div className="glass-card border border-emerald-400/30 rounded-2xl backdrop-blur-xl bg-slate-800/40 shadow-2xl overflow-hidden hover:bg-slate-800/50 hover:-translate-y-1 transition-all duration-300">
          
          {/* Card Header */}
          <div className="border-b border-slate-600/30 p-4 sm:p-6">
            <div className="flex items-center gap-3">
              <div className="w-12 h-12 bg-gradient-to-br from-emerald-500 to-green-600 rounded-xl flex items-center justify-center shadow-lg">
                <i className="fas fa-plus-circle text-white text-lg"></i>
              </div>
              <div>
                <h2 className="text-xl sm:text-2xl font-bold text-white">פרטי האופניים החדשים</h2>
                <p className="text-slate-400 text-sm">מלא את הפרטים הבסיסיים של האופניים</p>
              </div>
            </div>
          </div>
          
          {/* Form Content */}
          <div className="p-4 sm:p-6">
            <form onSubmit={handleSubmit} className="space-y-6">
              
              {/* Brand Field */}
              <div className="form-group opacity-0 translate-y-5 animate-fadeInUp" style={{ animationDelay: '0.1s' }}>
                <label className="form-label text-white font-semibold mb-3 flex items-center gap-2" htmlFor="brand-input">
                  <i className="fas fa-industry text-orange-400"></i>
                  יצרן
                  <span className="text-red-400">*</span>
                </label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <i className="fas fa-industry text-slate-400"></i>
                  </div>
                  <input 
                    type="text"
                    id="brand-input"
                    ref={brandInputRef}
                    value={formData.brand}
                    onChange={(e) => handleInputChange('brand', e.target.value)}
                    className="mercury-input w-full pl-10 pr-4 py-3 bg-slate-700/50 border border-slate-600/50 rounded-xl text-white placeholder-slate-400 focus:border-emerald-400 focus:ring-2 focus:ring-emerald-400/30 transition-all duration-300"
                    placeholder="דוגמה: Trek, Giant, Specialized"
                    required
                    style={{ fontSize: window.innerWidth <= 640 ? '16px' : '' }}
                  />
                  <div className="absolute inset-y-0 right-0 pr-3 flex items-center">
                    <div className={`w-2 h-2 rounded-full transition-opacity duration-300 ${getInputIndicatorClass('brand')}`}></div>
                  </div>
                </div>
                {errors.brand && (
                  <div className="form-error mt-2 text-red-400 text-sm flex items-center gap-1">
                    <i className="fas fa-exclamation-triangle"></i>
                    {errors.brand}
                  </div>
                )}
                <div className="mt-2">
                  <small className="text-slate-400">שם החברה היצרנית של האופניים</small>
                </div>
              </div>
              
              {/* Model Field */}
              <div className="form-group opacity-0 translate-y-5 animate-fadeInUp" style={{ animationDelay: '0.2s' }}>
                <label className="form-label text-white font-semibold mb-3 flex items-center gap-2" htmlFor="model-input">
                  <i className="fas fa-tag text-cyan-400"></i>
                  מודל
                </label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <i className="fas fa-tag text-slate-400"></i>
                  </div>
                  <input 
                    type="text"
                    id="model-input"
                    value={formData.model}
                    onChange={(e) => handleInputChange('model', e.target.value)}
                    className="mercury-input w-full pl-10 pr-4 py-3 bg-slate-700/50 border border-slate-600/50 rounded-xl text-white placeholder-slate-400 focus:border-cyan-400 focus:ring-2 focus:ring-cyan-400/30 transition-all duration-300"
                    placeholder="דוגמה: Domane, Defy, Tarmac"
                    style={{ fontSize: window.innerWidth <= 640 ? '16px' : '' }}
                  />
                  <div className="absolute inset-y-0 right-0 pr-3 flex items-center">
                    <div className={`w-2 h-2 rounded-full transition-opacity duration-300 ${getInputIndicatorClass('model')}`}></div>
                  </div>
                </div>
                {errors.model && (
                  <div className="form-error mt-2 text-red-400 text-sm flex items-center gap-1">
                    <i className="fas fa-exclamation-triangle"></i>
                    {errors.model}
                  </div>
                )}
                <div className="mt-2">
                  <small className="text-slate-400">מודל או סדרה של האופניים (אופציונלי)</small>
                </div>
              </div>
              
              {/* Color Field */}
              <div className="form-group opacity-0 translate-y-5 animate-fadeInUp" style={{ animationDelay: '0.3s' }}>
                <label className="form-label text-white font-semibold mb-3 flex items-center gap-2" htmlFor="color-input">
                  <i className="fas fa-palette text-purple-400"></i>
                  צבע
                </label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <i className="fas fa-palette text-slate-400"></i>
                  </div>
                  <input 
                    type="text"
                    id="color-input"
                    value={formData.color}
                    onChange={(e) => handleInputChange('color', e.target.value)}
                    className="mercury-input w-full pl-10 pr-4 py-3 bg-slate-700/50 border border-slate-600/50 rounded-xl text-white placeholder-slate-400 focus:border-purple-400 focus:ring-2 focus:ring-purple-400/30 transition-all duration-300"
                    placeholder="דוגמה: שחור, לבן, אדום, כחול"
                    style={{ fontSize: window.innerWidth <= 640 ? '16px' : '' }}
                  />
                  <div className="absolute inset-y-0 right-0 pr-3 flex items-center">
                    <div className={`w-2 h-2 rounded-full transition-opacity duration-300 ${getInputIndicatorClass('color')}`}></div>
                  </div>
                </div>
                {errors.color && (
                  <div className="form-error mt-2 text-red-400 text-sm flex items-center gap-1">
                    <i className="fas fa-exclamation-triangle"></i>
                    {errors.color}
                  </div>
                )}
                <div className="mt-2">
                  <small className="text-slate-400">הצבע העיקרי של האופניים (אופציונלי)</small>
                </div>
              </div>
              
              {/* Popular Colors Quick Select */}
              <div className="color-suggestions opacity-0 translate-y-5 animate-fadeInUp" style={{ animationDelay: '0.4s' }}>
                <label className="text-white font-medium mb-3 block">צבעים פופולריים:</label>
                <div className="grid grid-cols-4 sm:grid-cols-6 gap-3">
                  {popularColors.map((color, index) => (
                    <button 
                      key={index}
                      type="button" 
                      className={`color-option w-10 h-10 rounded-full border-2 hover:scale-110 transition-all duration-300 relative overflow-hidden ${color.bg} ${
                        selectedColorIndex === index ? 'border-emerald-500 shadow-lg shadow-emerald-500/30' : 'border-slate-500 hover:border-emerald-400'
                      }`}
                      onClick={() => handleColorSelect(color.name, index)}
                    >
                      <span className="sr-only">{color.name}</span>
                      <i className={`fas fa-check absolute inset-0 flex items-center justify-center ${color.textColor} font-bold transition-opacity duration-300 ${
                        selectedColorIndex === index ? 'opacity-100' : 'opacity-0'
                      }`} style={{ textShadow: '0 0 4px rgba(0, 0, 0, 0.8)' }}></i>
                    </button>
                  ))}
                </div>
              </div>
              
              {/* Form Actions */}
              <div className="form-actions pt-6 border-t border-slate-600/30 opacity-0 translate-y-5 animate-fadeInUp" style={{ animationDelay: '0.5s' }}>
                <div className="flex flex-col sm:flex-row gap-4 sm:justify-center">
                  <button 
                    type="submit" 
                    disabled={isSubmitting}
                    className="bg-green-500 w-full sm:w-auto inline-flex items-center justify-center px-6 py-3 hover:from-emerald-500 hover:to-green-500 text-white font-bold rounded-xl transition-all duration-300 shadow-lg hover:shadow-xl hover:shadow-emerald-500/40 hover:scale-105 active:scale-95 border border-emerald-500/50 backdrop-blur-sm disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    {isSubmitting ? (
                      <>
                        <i className="fas fa-spinner fa-spin mr-2"></i>
                        <span className="font-bold">מוסיף אופניים...</span>
                      </>
                    ) : (
                      <>
                        <i className="fas fa-plus mr-2"></i>
                        <span className="font-bold">הוסף אופניים</span>
                      </>
                    )}
                  </button>
                  <a 
                    href="/my-bikes/" 
                    className="w-full sm:w-auto inline-flex items-center justify-center px-6 py-3 bg-gradient-to-r from-slate-600 to-slate-700 hover:from-slate-500 hover:to-slate-600 text-white font-bold rounded-xl transition-all duration-300 shadow-lg hover:shadow-xl hover:shadow-slate-500/40 hover:scale-105 active:scale-95 border border-slate-500/50 backdrop-blur-sm"
                  >
                    <i className="fas fa-times mr-2"></i>
                    <span className="font-bold">ביטול</span>
                  </a>
                </div>
              </div>
            </form>
          </div>
        </div>
        
        {/* Info Section */}
        <div className="mt-6 text-center">
          <div className="glass-card border border-blue-400/20 rounded-xl p-4 inline-block bg-slate-800/40 backdrop-blur-xl hover:bg-slate-800/50 hover:-translate-y-1 transition-all duration-300">
            <div className="flex items-center gap-2 text-slate-300">
              <i className="fas fa-info-circle text-blue-400"></i>
              <small>לאחר הוספת האופניים תוכל לדווח על תקלות ולעקוב אחר התיקונים</small>
            </div>
          </div>
        </div>
        
        {/* Quick Actions */}
        <div className="mt-6 grid grid-cols-1 sm:grid-cols-2 gap-4">
          <a 
            href="/customer/report/" 
            className="glass-card border border-orange-400/30 rounded-xl p-4 hover:border-orange-400/50 transition-all duration-300 group bg-slate-800/40 backdrop-blur-xl hover:bg-slate-800/50 hover:-translate-y-1"
          >
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-orange-500/20 rounded-lg flex items-center justify-center group-hover:bg-orange-500/30 transition-colors duration-300">
                <i className="fas fa-exclamation-triangle text-orange-400"></i>
              </div>
              <div>
                <h3 className="text-white font-medium">דווח תקלה</h3>
                <p className="text-slate-400 text-sm">דווח על בעיה עם אופניים קיימות</p>
              </div>
            </div>
          </a>
          
          <a 
            href="/my-bikes/" 
            className="glass-card border border-blue-400/30 rounded-xl p-4 hover:border-blue-400/50 transition-all duration-300 group bg-slate-800/40 backdrop-blur-xl hover:bg-slate-800/50 hover:-translate-y-1"
          >
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-blue-500/20 rounded-lg flex items-center justify-center group-hover:bg-blue-500/30 transition-colors duration-300">
                <i className="fas fa-list text-blue-400"></i>
              </div>
              <div>
                <h3 className="text-white font-medium">האופניים שלי</h3>
                <p className="text-slate-400 text-sm">צפה ונהל את כל האופניים שלך</p>
              </div>
            </div>
          </a>
        </div>
      </div>
      
      <style jsx>{`
        @keyframes fadeInUp {
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }
        
        .animate-fadeInUp {
          animation: fadeInUp 0.6s ease-out forwards;
        }
      `}</style>
    </div>
  )
}