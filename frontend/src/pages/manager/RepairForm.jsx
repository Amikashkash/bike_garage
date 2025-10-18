import { useState, useEffect, useRef } from 'react';

const RepairForm = ({ selectedCustomerId = null }) => {
  // State management
  const [customerSearch, setCustomerSearch] = useState('');
  const [customerResults, setCustomerResults] = useState([]);
  const [searchLoading, setSearchLoading] = useState(false);
  const [selectedCustomer, setSelectedCustomer] = useState(null);

  const [bikes, setBikes] = useState([]);
  const [bikesLoading, setBikesLoading] = useState(false);
  const [selectedBike, setSelectedBike] = useState(null);

  const [categories, setCategories] = useState([]);
  const [expandedCategories, setExpandedCategories] = useState(new Set());
  const [selectedSubcategories, setSelectedSubcategories] = useState([]);

  const [problemDescription, setProblemDescription] = useState('');
  const [diagnosis, setDiagnosis] = useState('');

  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState('');

  const searchTimeoutRef = useRef(null);

  // Load categories on mount
  useEffect(() => {
    fetchCategories();
  }, []);

  // Auto-load customer if provided
  useEffect(() => {
    if (selectedCustomerId) {
      // If customer ID provided via URL, load that customer directly
      loadCustomerById(selectedCustomerId);
    }
  }, [selectedCustomerId]);

  // Auto-save to localStorage
  useEffect(() => {
    const formData = {
      selectedCustomer,
      selectedBike,
      selectedSubcategories,
      problemDescription,
      diagnosis,
    };
    localStorage.setItem('repair_form_backup', JSON.stringify(formData));
  }, [selectedCustomer, selectedBike, selectedSubcategories, problemDescription, diagnosis]);

  // Fetch categories
  const fetchCategories = async () => {
    try {
      const response = await fetch('/api/categories/', {
        credentials: 'same-origin',
      });
      const data = await response.json();
      setCategories(data);
    } catch (error) {
      console.error('Error fetching categories:', error);
      setError('שגיאה בטעינת קטגוריות');
    }
  };

  // Customer search with debouncing
  const handleCustomerSearch = e => {
    const query = e.target.value;
    setCustomerSearch(query);

    if (searchTimeoutRef.current) {
      clearTimeout(searchTimeoutRef.current);
    }

    if (query.trim().length < 2) {
      setCustomerResults([]);
      return;
    }

    setSearchLoading(true);
    searchTimeoutRef.current = setTimeout(() => {
      searchCustomers(query);
    }, 300);
  };

  const searchCustomers = async query => {
    try {
      const response = await fetch(`/api/search-customers/?q=${encodeURIComponent(query)}`, {
        credentials: 'same-origin',
      });
      const data = await response.json();
      setCustomerResults(data.customers || []);
      setSearchLoading(false);
    } catch (error) {
      console.error('Error searching customers:', error);
      setError('שגיאה בחיפוש לקוחות');
      setSearchLoading(false);
    }
  };

  const loadCustomerById = async customerId => {
    try {
      const response = await fetch(`/api/search-customers/?id=${customerId}`, {
        credentials: 'same-origin',
      });
      const data = await response.json();
      if (data.customers && data.customers.length > 0) {
        selectCustomer(data.customers[0]);
      }
    } catch (error) {
      console.error('Error loading customer:', error);
    }
  };

  const selectCustomer = customer => {
    setSelectedCustomer(customer);
    setCustomerResults([]);
    setCustomerSearch('');

    // Load customer bikes
    if (customer.bikes_count > 0) {
      loadCustomerBikes(customer.id);
    } else {
      setBikes([]);
    }
  };

  const clearCustomer = () => {
    setSelectedCustomer(null);
    setBikes([]);
    setSelectedBike(null);
    setCustomerSearch('');
  };

  const loadCustomerBikes = async customerId => {
    setBikesLoading(true);
    try {
      const response = await fetch(`/api/customer-bikes/${customerId}/`, {
        credentials: 'same-origin',
      });
      const data = await response.json();
      setBikes(data.bikes || []);

      // Auto-select if only one bike
      if (data.bikes && data.bikes.length === 1) {
        setSelectedBike(data.bikes[0]);
      }

      setBikesLoading(false);
    } catch (error) {
      console.error('Error loading bikes:', error);
      setError('שגיאה בטעינת אופניים');
      setBikesLoading(false);
    }
  };

  const toggleCategory = categoryId => {
    const newExpanded = new Set(expandedCategories);
    if (newExpanded.has(categoryId)) {
      newExpanded.delete(categoryId);
      // Remove all subcategories from this category
      const category = categories.find(c => c.id === categoryId);
      if (category) {
        const subcatIds = category.subcategories.map(sub => sub.id);
        setSelectedSubcategories(prev => prev.filter(id => !subcatIds.includes(id)));
      }
    } else {
      newExpanded.add(categoryId);
    }
    setExpandedCategories(newExpanded);
  };

  const toggleSubcategory = subcategoryId => {
    setSelectedSubcategories(prev =>
      prev.includes(subcategoryId)
        ? prev.filter(id => id !== subcategoryId)
        : [...prev, subcategoryId]
    );
  };

  const handleSubmit = async e => {
    e.preventDefault();

    // Validation
    if (!selectedBike) {
      setError('נא לבחור אופניים');
      return;
    }

    if (selectedSubcategories.length === 0 && !problemDescription.trim()) {
      setError('נא לבחור לפחות קטגוריה אחת או לכתוב תיאור בעיה');
      return;
    }

    setSubmitting(true);
    setError('');

    try {
      const response = await fetch('/api/repair/submit/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
        },
        credentials: 'same-origin',
        body: JSON.stringify({
          bike_id: selectedBike.id,
          subcategory_ids: selectedSubcategories,
          problem_description: problemDescription,
          diagnosis: diagnosis,
        }),
      });

      const data = await response.json();

      if (data.success) {
        // Clear localStorage backup
        localStorage.removeItem('repair_form_backup');

        // Redirect based on response
        if (data.redirect_to_diagnosis) {
          window.location.href = `/manager/repair/${data.repair_id}/diagnosis/`;
        } else {
          window.location.href = '/manager/dashboard/';
        }
      } else {
        setError(data.error || 'שגיאה בשמירת התיקון');
        setSubmitting(false);
      }
    } catch (error) {
      console.error('Error submitting repair:', error);
      setError('שגיאה בשמירת התיקון');
      setSubmitting(false);
    }
  };

  const isFormValid = () => {
    return selectedBike && (selectedSubcategories.length > 0 || problemDescription.trim());
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900">
      <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-6 sm:py-8">
        {/* Header */}
        <div className="text-center mb-6 sm:mb-8">
          <h1 className="text-3xl sm:text-4xl lg:text-5xl font-bold mb-4 bg-gradient-to-r from-blue-400 via-purple-400 to-cyan-400 bg-clip-text text-transparent">
            🔧 הוסף תיקון אופניים ⚙️
          </h1>
          <p className="text-slate-300 text-base sm:text-lg max-w-2xl mx-auto">
            צור תיקון חדש עם פרטי התקלה והאבחון המפורט
          </p>

          {/* Progress Indicator */}
          <div className="flex justify-center mt-6">
            <div className="bg-slate-800/40 border border-blue-400/30 rounded-2xl px-4 py-2 backdrop-blur-xl">
              <div className="flex items-center gap-3 text-sm">
                <div className="flex items-center gap-2">
                  <div className="w-3 h-3 bg-blue-400 rounded-full"></div>
                  <span className="text-blue-300 font-medium">טופס חדש</span>
                </div>
                <i className="fas fa-chevron-left text-slate-400"></i>
                <div className="flex items-center gap-2">
                  <div className="w-3 h-3 bg-slate-600 rounded-full"></div>
                  <span className="text-slate-400">אבחון</span>
                </div>
                <i className="fas fa-chevron-left text-slate-400"></i>
                <div className="flex items-center gap-2">
                  <div className="w-3 h-3 bg-slate-600 rounded-full"></div>
                  <span className="text-slate-400">ביצוע</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Error Message */}
        {error && (
          <div className="mb-6 p-4 bg-red-500/10 border border-red-400/30 rounded-xl">
            <div className="flex items-center gap-2 text-red-300">
              <i className="fas fa-exclamation-triangle"></i>
              <span>{error}</span>
            </div>
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Customer Search */}
          <div className="glass-card">
            <div className="border-b border-slate-600/30 p-4 sm:p-6">
              <div className="flex items-center gap-3">
                <div className="flex-shrink-0 w-10 h-10 sm:w-12 sm:h-12 bg-green-500/20 rounded-xl flex items-center justify-center">
                  <i className="fas fa-search text-green-400 text-lg sm:text-xl"></i>
                </div>
                <h2 className="text-lg sm:text-xl font-bold text-white">חיפוש לקוח</h2>
              </div>
            </div>
            <div className="p-4 sm:p-6">
              {!selectedCustomer ? (
                <>
                  <label className="block text-white font-semibold mb-3 flex items-center gap-2">
                    <i className="fas fa-user text-green-400"></i>
                    חפש לקוח לפי שם, טלפון או מספר לקוח
                  </label>
                  <input
                    type="text"
                    value={customerSearch}
                    onChange={handleCustomerSearch}
                    className="w-full bg-slate-700/50 border border-slate-600 text-white placeholder-slate-400 rounded-xl px-4 py-3 focus:border-green-400 focus:ring-2 focus:ring-green-400/20 transition-all"
                    placeholder="הקלד שם לקוח, מספר טלפון או מספר לקוח..."
                    autoComplete="off"
                  />

                  {/* Customer Results */}
                  {searchLoading && (
                    <div className="mt-4 bg-slate-700/50 border border-slate-600 rounded-xl p-4 text-center">
                      <i className="fas fa-spinner fa-spin text-slate-400 mr-2"></i>
                      <span className="text-slate-300">מחפש לקוחות...</span>
                    </div>
                  )}

                  {!searchLoading && customerResults.length > 0 && (
                    <div className="mt-4 space-y-2">
                      {customerResults.map(customer => (
                        <div
                          key={customer.id}
                          onClick={() => selectCustomer(customer)}
                          className="bg-slate-700/50 border border-slate-600 hover:border-green-400/50 rounded-xl p-4 cursor-pointer transition-all hover:bg-slate-600/50"
                        >
                          <div className="flex items-center justify-between">
                            <div className="flex items-center gap-3">
                              <div className="w-10 h-10 bg-green-500/20 rounded-full flex items-center justify-center">
                                <i className="fas fa-user text-green-400"></i>
                              </div>
                              <div>
                                <div className="text-white font-semibold">{customer.name}</div>
                                <div className="text-slate-300 text-sm">
                                  {customer.phone && (
                                    <>
                                      <i className="fas fa-phone mr-1"></i>
                                      {customer.phone}
                                    </>
                                  )}
                                  {customer.customer_number && (
                                    <>
                                      <span className="mx-2">•</span>
                                      <i className="fas fa-hashtag mr-1"></i>
                                      {customer.customer_number}
                                    </>
                                  )}
                                </div>
                              </div>
                            </div>
                            <div className="text-blue-300 text-sm">
                              <i className="fas fa-bicycle mr-1"></i>
                              {customer.bikes_count} אופניים
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>
                  )}
                </>
              ) : (
                <div className="bg-green-500/10 border border-green-400/30 rounded-xl p-4">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-3">
                      <div className="w-10 h-10 bg-green-500/20 rounded-full flex items-center justify-center">
                        <i className="fas fa-user text-green-400"></i>
                      </div>
                      <div>
                        <div className="text-white font-semibold">{selectedCustomer.name}</div>
                        <div className="text-green-300 text-sm">{selectedCustomer.phone || 'אין טלפון'}</div>
                      </div>
                    </div>
                    <button
                      type="button"
                      onClick={clearCustomer}
                      className="text-slate-400 hover:text-white transition-colors"
                    >
                      <i className="fas fa-times"></i>
                    </button>
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* Bike Selection */}
          <div className="glass-card">
            <div className="border-b border-slate-600/30 p-4 sm:p-6">
              <div className="flex items-center gap-3">
                <div className="flex-shrink-0 w-10 h-10 sm:w-12 sm:h-12 bg-blue-500/20 rounded-xl flex items-center justify-center">
                  <i className="fas fa-bicycle text-blue-400 text-lg sm:text-xl"></i>
                </div>
                <h2 className="text-lg sm:text-xl font-bold text-white">בחירת אופניים</h2>
              </div>
            </div>
            <div className="p-4 sm:p-6">
              {!selectedCustomer ? (
                <div className="text-center py-8 text-slate-400">
                  <i className="fas fa-info-circle text-4xl mb-4"></i>
                  <p>בחר לקוח תחילה כדי לראות את האופניים שלו</p>
                </div>
              ) : bikesLoading ? (
                <div className="text-center py-8">
                  <i className="fas fa-spinner fa-spin text-slate-400 text-2xl mb-2"></i>
                  <p className="text-slate-300">טוען אופניים...</p>
                </div>
              ) : bikes.length === 0 ? (
                <div className="bg-amber-500/10 border border-amber-400/30 rounded-xl p-4 text-center">
                  <i className="fas fa-bicycle text-amber-400 text-2xl mb-2"></i>
                  <div className="text-amber-300 font-semibold">ללקוח אין אופניים רשומים</div>
                  <div className="text-amber-200 text-sm mt-1">יש להוסיף אופניים תחילה</div>
                </div>
              ) : (
                <>
                  <label className="block text-white font-semibold mb-3 flex items-center gap-2">
                    <i className="fas fa-bicycle text-blue-400"></i>
                    בחר אופניים לתיקון
                  </label>
                  <div className="space-y-3">
                    {bikes.map(bike => (
                      <div
                        key={bike.id}
                        onClick={() => setSelectedBike(bike)}
                        className={`bg-slate-700/50 border rounded-xl p-4 cursor-pointer transition-all ${
                          selectedBike?.id === bike.id
                            ? 'border-blue-400 bg-blue-500/10'
                            : 'border-slate-600 hover:border-blue-400/50'
                        }`}
                      >
                        <div className="flex items-center justify-between">
                          <div className="flex items-center gap-3">
                            <div className="w-10 h-10 bg-blue-500/20 rounded-full flex items-center justify-center">
                              <i className="fas fa-bicycle text-blue-400"></i>
                            </div>
                            <div>
                              <div className="text-white font-semibold">
                                {bike.brand} {bike.model}
                              </div>
                              <div className="text-slate-300 text-sm">
                                <i className="fas fa-palette mr-1"></i>
                                {bike.color}
                                {bike.serial_number && (
                                  <>
                                    <span className="mx-2">•</span>
                                    <i className="fas fa-barcode mr-1"></i>
                                    {bike.serial_number}
                                  </>
                                )}
                              </div>
                            </div>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </>
              )}
            </div>
          </div>

          {/* Categories */}
          <div className="glass-card">
            <div className="border-b border-slate-600/30 p-4 sm:p-6">
              <div className="flex items-center gap-3">
                <div className="flex-shrink-0 w-10 h-10 sm:w-12 sm:h-12 bg-amber-500/20 rounded-xl flex items-center justify-center">
                  <i className="fas fa-tools text-amber-400 text-lg sm:text-xl"></i>
                </div>
                <h2 className="text-lg sm:text-xl font-bold text-white">קטגוריות התקלה</h2>
              </div>
            </div>
            <div className="p-4 sm:p-6">
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
                {categories.map(category => (
                  <div key={category.id} className="category-item">
                    <div
                      className={`bg-slate-700/30 border rounded-xl overflow-hidden transition-all ${
                        expandedCategories.has(category.id)
                          ? 'border-amber-400/50 bg-amber-500/5'
                          : 'border-slate-600/40'
                      }`}
                    >
                      {/* Category Header */}
                      <div
                        className="p-4 border-b border-slate-600/30 cursor-pointer"
                        onClick={() => toggleCategory(category.id)}
                      >
                        <div className="flex items-center justify-between">
                          <div className="flex items-center gap-2">
                            <i className="fas fa-folder text-amber-400"></i>
                            <span className="text-white font-medium">{category.name}</span>
                          </div>
                          <i
                            className={`fas fa-chevron-down text-slate-400 transition-transform ${
                              expandedCategories.has(category.id) ? 'rotate-180' : ''
                            }`}
                          ></i>
                        </div>
                      </div>

                      {/* Subcategories */}
                      {expandedCategories.has(category.id) && (
                        <div className="p-4 space-y-3">
                          {category.subcategories.map(sub => (
                            <label
                              key={sub.id}
                              className={`flex items-center gap-3 p-3 rounded-lg cursor-pointer transition-all ${
                                selectedSubcategories.includes(sub.id)
                                  ? 'bg-green-500/10 border border-green-400/50'
                                  : 'bg-slate-800/50 border border-slate-600/30 hover:border-green-400/50'
                              }`}
                            >
                              <input
                                type="checkbox"
                                checked={selectedSubcategories.includes(sub.id)}
                                onChange={() => toggleSubcategory(sub.id)}
                                className="sr-only"
                              />
                              <div
                                className={`w-4 h-4 rounded border-2 flex items-center justify-center transition-all ${
                                  selectedSubcategories.includes(sub.id)
                                    ? 'bg-green-500 border-green-500'
                                    : 'bg-slate-600 border-slate-500'
                                }`}
                              >
                                {selectedSubcategories.includes(sub.id) && (
                                  <i className="fas fa-check text-white text-xs"></i>
                                )}
                              </div>
                              <div className="flex items-center gap-2 flex-1">
                                <i className="fas fa-wrench text-green-400 text-sm"></i>
                                <span className="text-slate-200 text-sm">{sub.name}</span>
                              </div>
                            </label>
                          ))}
                        </div>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Problem Description */}
          <div className="glass-card">
            <div className="border-b border-slate-600/30 p-4 sm:p-6">
              <div className="flex items-center gap-3">
                <div className="flex-shrink-0 w-10 h-10 sm:w-12 sm:h-12 bg-purple-500/20 rounded-xl flex items-center justify-center">
                  <i className="fas fa-edit text-purple-400 text-lg sm:text-xl"></i>
                </div>
                <h2 className="text-lg sm:text-xl font-bold text-white">תיאור התקלה</h2>
              </div>
            </div>
            <div className="p-4 sm:p-6">
              <label className="block text-white font-semibold mb-3 flex items-center gap-2">
                <i className="fas fa-comment-alt text-purple-400"></i>
                תיאור התקלה (חופשי)
              </label>
              <div className="relative">
                <textarea
                  value={problemDescription}
                  onChange={e => setProblemDescription(e.target.value)}
                  className="w-full bg-slate-700/50 border border-slate-600 text-white placeholder-slate-400 rounded-xl px-4 py-3 pb-8 focus:border-purple-400 focus:ring-2 focus:ring-purple-400/20 transition-all resize-vertical min-h-[100px]"
                  placeholder="תאר את הבעיה..."
                  maxLength={500}
                />
                <div className="absolute bottom-3 left-3 text-xs text-slate-400">
                  {problemDescription.length} / 500 תווים
                </div>
              </div>
            </div>
          </div>

          {/* Diagnosis */}
          <div className="glass-card">
            <div className="border-b border-slate-600/30 p-4 sm:p-6">
              <div className="flex items-center gap-3">
                <div className="flex-shrink-0 w-10 h-10 sm:w-12 sm:h-12 bg-emerald-500/20 rounded-xl flex items-center justify-center">
                  <i className="fas fa-stethoscope text-emerald-400 text-lg sm:text-xl"></i>
                </div>
                <h2 className="text-lg sm:text-xl font-bold text-white">אבחון ופתרון</h2>
              </div>
            </div>
            <div className="p-4 sm:p-6">
              <label className="block text-white font-semibold mb-3 flex items-center gap-2">
                <i className="fas fa-microscope text-emerald-400"></i>
                אבחון (אופציונלי)
              </label>
              <textarea
                value={diagnosis}
                onChange={e => setDiagnosis(e.target.value)}
                className="w-full bg-slate-700/50 border border-slate-600 text-white placeholder-slate-400 rounded-xl px-4 py-3 focus:border-emerald-400 focus:ring-2 focus:ring-emerald-400/20 transition-all resize-vertical min-h-[100px]"
                placeholder="פרט אבחון..."
              />
              <div className="mt-4 p-4 bg-blue-500/10 border border-blue-400/30 rounded-lg">
                <div className="flex items-start gap-3">
                  <i className="fas fa-info-circle text-blue-400 mt-0.5"></i>
                  <div className="text-blue-200 text-sm leading-relaxed">
                    אם תמלא אבחון כאן, תועבר ישירות לדף האבחון המפורט כדי להוסיף פעולות תיקון ספציפיות עם מחירים
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Action Buttons */}
          <div className="flex flex-col sm:flex-row gap-4 justify-center pt-6">
            <button
              type="submit"
              disabled={!isFormValid() || submitting}
              className="bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700 text-white font-semibold py-4 px-8 rounded-xl transition-all shadow-lg hover:shadow-xl transform hover:scale-105 active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none order-2 sm:order-1"
            >
              {submitting ? (
                <>
                  <i className="fas fa-spinner fa-spin mr-2"></i>
                  שומר...
                </>
              ) : (
                <>
                  <i className="fas fa-save mr-2"></i>
                  שמור תיקון
                </>
              )}
            </button>
            <a
              href="/manager/dashboard/"
              className="bg-slate-600/50 hover:bg-slate-600/70 text-slate-200 font-semibold py-4 px-8 rounded-xl transition-all text-center border border-slate-500/30 hover:border-slate-400/50 order-1 sm:order-2"
            >
              <i className="fas fa-times mr-2"></i>
              ביטול
            </a>
          </div>
        </form>
      </div>

      <style>{`
        .glass-card {
          background: rgba(15, 23, 42, 0.4);
          backdrop-filter: blur(16px);
          border: 1px solid rgba(71, 85, 105, 0.3);
          border-radius: 1rem;
          box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
          animation: fadeInUp 0.6s ease-out forwards;
          overflow: hidden;
        }

        .glass-card:hover {
          background: rgba(15, 23, 42, 0.5);
          transform: translateY(-2px);
          transition: all 0.3s ease;
        }

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

        .sr-only {
          position: absolute;
          width: 1px;
          height: 1px;
          padding: 0;
          margin: -1px;
          overflow: hidden;
          clip: rect(0, 0, 0, 0);
          white-space: nowrap;
          border-width: 0;
        }
      `}</style>
    </div>
  );
};

// Initialize React app
import { createRoot } from 'react-dom/client';
const rootElement = document.getElementById('root');
if (rootElement) {
  const root = createRoot(rootElement);
  // Check if customer ID provided via data attribute
  const selectedCustomerId = rootElement.dataset.customerId
    ? parseInt(rootElement.dataset.customerId)
    : null;
  root.render(<RepairForm selectedCustomerId={selectedCustomerId} />);
}

export default RepairForm;
