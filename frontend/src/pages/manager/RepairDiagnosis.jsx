/**
 * RepairDiagnosis Component
 *
 * Main component for repair diagnosis page.
 * Allows manager to:
 * - View repair details
 * - Add diagnosis text
 * - Create repair items (tasks) with prices
 * - Send notification to customer for approval
 */

import { useState, useEffect } from 'react';
import RepairInfo from '../../components/diagnosis/RepairInfo';
import ExistingItems from '../../components/diagnosis/ExistingItems';
import RepairItemRow from '../../components/diagnosis/RepairItemRow';
import NotificationSettings from '../../components/diagnosis/NotificationSettings';

const RepairDiagnosis = ({ repairId }) => {
  // ============================================================================
  // STATE MANAGEMENT
  // ============================================================================

  const [loading, setLoading] = useState(true);
  const [repair, setRepair] = useState(null);
  const [error, setError] = useState('');

  // Form fields
  const [diagnosis, setDiagnosis] = useState('');
  const [repairItems, setRepairItems] = useState([{ description: '', price: '' }]);
  const [sendNotification, setSendNotification] = useState(true);

  // UI state
  const [submitting, setSubmitting] = useState(false);
  const [totalNewPrice, setTotalNewPrice] = useState(0);

  // ============================================================================
  // DATA FETCHING
  // ============================================================================

  useEffect(() => {
    fetchRepairData();
  }, [repairId]);

  const fetchRepairData = async () => {
    try {
      const response = await fetch(`/api/repair/${repairId}/diagnosis/`, {
        credentials: 'same-origin',
      });

      if (!response.ok) {
        throw new Error('Failed to load repair data');
      }

      const data = await response.json();
      setRepair(data);
      setDiagnosis(data.diagnosis || '');
      setLoading(false);
    } catch (err) {
      setError(err.message);
      setLoading(false);
    }
  };

  // ============================================================================
  // REPAIR ITEMS MANAGEMENT
  // ============================================================================

  /**
   * Update a specific repair item field
   */
  const updateRepairItem = (index, field, value) => {
    const updated = [...repairItems];
    updated[index][field] = value;
    setRepairItems(updated);
  };

  /**
   * Add a new empty repair item
   */
  const addRepairItem = () => {
    setRepairItems([...repairItems, { description: '', price: '' }]);
  };

  /**
   * Remove a repair item by index
   */
  const removeRepairItem = index => {
    const updated = repairItems.filter((_, i) => i !== index);
    setRepairItems(updated);
  };

  /**
   * Handle category click - auto-fill description
   */
  const handleCategoryClick = categoryText => {
    // Find first empty description input
    const emptyIndex = repairItems.findIndex(item => !item.description.trim());

    if (emptyIndex >= 0) {
      // Fill existing empty input
      updateRepairItem(emptyIndex, 'description', categoryText);
    } else {
      // Add new item with category text
      setRepairItems([...repairItems, { description: categoryText, price: '' }]);
    }
  };

  // ============================================================================
  // PRICE CALCULATION
  // ============================================================================

  useEffect(() => {
    const total = repairItems.reduce((sum, item) => {
      const price = parseFloat(item.price) || 0;
      return sum + price;
    }, 0);
    setTotalNewPrice(total);
  }, [repairItems]);

  // ============================================================================
  // FORM SUBMISSION
  // ============================================================================

  const handleSubmit = async e => {
    e.preventDefault();

    // Validation
    const validItems = repairItems.filter(
      item => item.description.trim() && item.price && parseFloat(item.price) > 0
    );

    if (validItems.length === 0) {
      setError('נא להוסיף לפחות פעולת תיקון אחת עם מחיר');
      return;
    }

    setSubmitting(true);
    setError('');

    try {
      const response = await fetch(`/api/repair/${repairId}/diagnosis/submit/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
        },
        credentials: 'same-origin',
        body: JSON.stringify({
          diagnosis,
          repair_items: validItems.map(item => ({
            description: item.description.trim(),
            price: parseFloat(item.price),
          })),
          send_notification: sendNotification,
        }),
      });

      const data = await response.json();

      if (data.success) {
        // Redirect to manager dashboard on success
        window.location.href = '/manager/dashboard/';
      } else {
        setError(data.error || 'שגיאה בשמירת האבחון');
        setSubmitting(false);
      }
    } catch (err) {
      setError('שגיאה בשמירת האבחון');
      setSubmitting(false);
    }
  };

  // ============================================================================
  // LOADING & ERROR STATES
  // ============================================================================

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900 flex items-center justify-center">
        <div className="text-center">
          <div className="w-16 h-16 border-4 border-blue-400 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-slate-300 text-lg">טוען נתונים...</p>
        </div>
      </div>
    );
  }

  if (error && !repair) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900 flex items-center justify-center">
        <div className="bg-red-900/20 border border-red-500/30 rounded-2xl p-8 max-w-md mx-auto">
          <div className="text-center">
            <i className="fas fa-exclamation-triangle text-red-400 text-4xl mb-4"></i>
            <h2 className="text-xl font-bold text-white mb-2">שגיאה</h2>
            <p className="text-red-200 mb-4">{error}</p>
            <a
              href="/manager/dashboard/"
              className="bg-red-500/20 hover:bg-red-500/30 text-red-300 px-4 py-2 rounded-lg border border-red-400/40 transition-all duration-200 inline-block"
            >
              חזור לדשבורד
            </a>
          </div>
        </div>
      </div>
    );
  }

  // ============================================================================
  // MAIN RENDER
  // ============================================================================

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* ===== HEADER ===== */}
        <div className="text-center mb-8">
          <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between">
            <div className="mb-4 lg:mb-0">
              <h1 className="text-3xl lg:text-4xl font-bold mb-2 bg-gradient-to-r from-blue-400 via-purple-400 to-cyan-400 bg-clip-text text-transparent">
                🔍 אבחון תיקון #{repair.id}
              </h1>
              <p className="text-slate-300 text-base">
                {repair.is_editing ? 'עריכת אבחון והצעת מחיר מפורטת' : 'אבחון מקצועי והצעת מחיר מדויקת'}
              </p>
            </div>

            {/* Breadcrumb */}
            <div className="hidden sm:flex justify-center lg:justify-end">
              <div className="bg-blue-500/20 border border-blue-400/40 rounded-xl px-4 py-2">
                <nav className="flex items-center gap-2 text-sm">
                  <a
                    href="/manager/dashboard/"
                    className="text-blue-300 hover:text-blue-200 transition-colors"
                  >
                    <i className="fas fa-tachometer-alt mr-1"></i>דשבורד מנהל
                  </a>
                  <i className="fas fa-chevron-left text-slate-400"></i>
                  <span className="text-white font-medium">
                    <i className="fas fa-stethoscope mr-1"></i>
                    {repair.is_editing ? 'עריכת אבחון' : 'אבחון'}
                  </span>
                </nav>
              </div>
            </div>
          </div>
        </div>

        {/* ===== INSTRUCTIONS (if no existing items) ===== */}
        {(!repair.existing_items || repair.existing_items.length === 0) && (
          <div className="mb-6">
            <div className="bg-blue-900/30 border border-blue-500/40 rounded-xl overflow-hidden backdrop-blur-sm">
              <div className="px-4 py-3 bg-blue-500/20 border-b border-blue-500/30">
                <div className="flex items-center gap-3">
                  <div className="w-8 h-8 bg-blue-500/30 rounded-lg flex items-center justify-center">
                    <i className="fas fa-lightbulb text-blue-400"></i>
                  </div>
                  <div>
                    <h3 className="text-lg font-bold text-white">💡 הוראות לאבחון מדויק</h3>
                    <p className="text-blue-200 text-sm">
                      הוסף את כל הפעולות הנדרשות עם מחירים מדויקים, וכך הלקוח יוכל לאשר בדיוק איזה
                      פעולות הוא רוצה לבצע.
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* ===== ERROR MESSAGE ===== */}
        {error && (
          <div className="mb-6 p-4 bg-red-500/10 border border-red-400/30 rounded-xl">
            <div className="flex items-center gap-2 text-red-300">
              <i className="fas fa-exclamation-triangle"></i>
              <span>{error}</span>
            </div>
          </div>
        )}

        {/* ===== MAIN CONTENT ===== */}
        <div className="flex flex-col xl:flex-row gap-6 w-full">
          {/* Left Sidebar - Repair Info */}
          <div className="w-full xl:w-96 xl:shrink-0 order-2 xl:order-1">
            <RepairInfo repair={repair} onCategoryClick={handleCategoryClick} />
          </div>

          {/* Main Form Area */}
          <div className="flex-1 min-w-0 order-1 xl:order-2">
            <form onSubmit={handleSubmit}>
              <div className="grid grid-cols-1 xl:grid-cols-2 gap-6">
                {/* ===== DIAGNOSIS CARD ===== */}
                <div className="bg-slate-800/50 backdrop-blur-sm border border-slate-700 rounded-xl overflow-hidden h-fit">
                  <div className="bg-green-500/20 px-4 py-3 border-b border-green-500/30">
                    <h3 className="text-lg font-bold text-white flex items-center gap-2">
                      <i className="fas fa-stethoscope text-green-400"></i>אבחון והצעת מחיר
                    </h3>
                  </div>
                  <div className="p-4">
                    <label className="block text-slate-300 text-sm font-medium mb-2">
                      <i className="fas fa-clipboard-list text-blue-400 mr-2"></i>
                      אבחון (אופציונלי)
                    </label>
                    <textarea
                      value={diagnosis}
                      onChange={e => setDiagnosis(e.target.value)}
                      className="w-full px-3 py-2 bg-slate-700/50 border border-slate-600 rounded-lg text-white placeholder-slate-400 text-sm focus:ring-2 focus:ring-green-500 focus:border-transparent resize-vertical min-h-[100px]"
                      placeholder="פרט את האבחון..."
                    />
                  </div>
                </div>

                {/* ===== REPAIR ITEMS CARD ===== */}
                <div className="bg-slate-800/50 backdrop-blur-sm border border-slate-700 rounded-xl overflow-hidden">
                  <div className="bg-orange-500/20 px-4 py-3 border-b border-orange-500/30">
                    <h3 className="text-lg font-bold text-white flex items-center gap-2">
                      <i className="fas fa-tools text-orange-400"></i>פעולות תיקון ומחירים
                    </h3>
                    <p className="text-orange-200 text-sm mt-1">
                      הוסף את כל הפעולות הנדרשות עם מחירים מדויקים
                    </p>
                  </div>
                  <div className="p-4">
                    {/* Existing Items */}
                    <ExistingItems
                      items={repair.existing_items}
                      totalPrice={repair.total_existing_price}
                    />

                    {/* New Items */}
                    <div className="space-y-3">
                      {repairItems.map((item, index) => (
                        <RepairItemRow
                          key={index}
                          index={index}
                          item={item}
                          onUpdate={updateRepairItem}
                          onRemove={removeRepairItem}
                          showRemove={repairItems.length > 1}
                        />
                      ))}
                    </div>

                    {/* Add Item Button & Total */}
                    <div className="flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-3 mt-4">
                      <button
                        type="button"
                        onClick={addRepairItem}
                        className="bg-green-500/20 hover:bg-green-500/30 text-green-300 px-4 py-2 rounded-lg border border-green-400/40 hover:border-green-400/60 transition-all duration-200 flex items-center justify-center gap-2"
                      >
                        <i className="fas fa-plus"></i>
                        <span className="text-sm font-medium">הוסף פעולה נוספת</span>
                      </button>

                      <div className="bg-green-500/10 border border-green-400/30 rounded-lg px-4 py-2 text-center sm:text-right">
                        <span className="text-green-300 font-medium text-sm">סה"כ פעולות חדשות: </span>
                        <span className="text-green-200 font-bold text-base">₪{totalNewPrice.toFixed(2)}</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              {/* ===== NOTIFICATION SETTINGS ===== */}
              <NotificationSettings
                sendNotification={sendNotification}
                onToggle={setSendNotification}
                customer={repair.customer}
                bike={repair.bike}
              />

              {/* ===== FORM ACTIONS ===== */}
              <div className="flex flex-col gap-4 mt-6">
                <button
                  type="submit"
                  disabled={submitting}
                  className="bg-gradient-to-r from-green-500 to-emerald-600 hover:from-green-600 hover:to-emerald-700 text-white font-semibold py-4 px-8 rounded-xl transition-all shadow-lg hover:shadow-xl transform hover:scale-105 active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none"
                >
                  {submitting ? (
                    <>
                      <i className="fas fa-spinner fa-spin mr-2"></i>
                      שומר...
                    </>
                  ) : repair.is_editing ? (
                    <>
                      <i className="fas fa-save mr-2"></i>
                      עדכן אבחון ושלח ללקוח
                    </>
                  ) : (
                    <>
                      <i className="fas fa-check mr-2"></i>
                      שמור אבחון ושלח ללקוח
                    </>
                  )}
                </button>

                <a
                  href="/manager/dashboard/"
                  className="bg-slate-600/50 hover:bg-slate-600/70 text-slate-200 font-semibold py-4 px-8 rounded-xl transition-all text-center border border-slate-500/30 hover:border-slate-400/50"
                >
                  <i className="fas fa-times mr-2"></i>
                  ביטול
                </a>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
};

// ============================================================================
// INITIALIZE REACT APP
// ============================================================================

import { createRoot } from 'react-dom/client';
const rootElement = document.getElementById('root');
if (rootElement) {
  const root = createRoot(rootElement);
  const repairId = rootElement.dataset.repairId ? parseInt(rootElement.dataset.repairId) : null;
  root.render(<RepairDiagnosis repairId={repairId} />);
}

export default RepairDiagnosis;
