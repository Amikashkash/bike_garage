/**
 * ExistingItems Component
 *
 * Displays existing repair items (if any) with:
 * - Item description and price
 * - Approval status
 * - Total price calculation
 */

const ExistingItems = ({ items, totalPrice }) => {
  if (!items || items.length === 0) {
    return null;
  }

  return (
    <div className="mb-4">
      {/* Header */}
      <h6 className="text-white font-medium mb-3 flex items-center gap-2 text-sm">
        <i className="fas fa-list text-blue-400"></i>פעולות תיקון קיימות
      </h6>

      {/* Items List */}
      <div className="grid grid-cols-1 gap-3 mb-4">
        {items.map(item => (
          <div key={item.id} className="bg-slate-700/50 border border-slate-600 rounded-lg p-3">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
              {/* Item Description */}
              <div className="flex items-center gap-2 flex-1 min-w-0">
                <div className="w-6 h-6 bg-blue-500/20 rounded flex items-center justify-center flex-shrink-0">
                  <i className="fas fa-wrench text-blue-400 text-xs"></i>
                </div>
                <span className="text-white font-medium text-sm break-words">
                  {item.description}
                </span>
              </div>

              {/* Price and Status */}
              <div className="flex items-center justify-between sm:justify-end gap-2">
                <span className="text-white font-bold text-sm">₪{item.price}</span>
                {item.is_approved ? (
                  <span className="bg-green-500/20 text-green-300 px-2 py-1 rounded text-xs font-medium whitespace-nowrap">
                    <i className="fas fa-check mr-1"></i>אושר
                  </span>
                ) : (
                  <span className="bg-orange-500/20 text-orange-300 px-2 py-1 rounded text-xs font-medium whitespace-nowrap">
                    <i className="fas fa-clock mr-1"></i>ממתין
                  </span>
                )}
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Total Price */}
      <div className="bg-slate-700/30 border border-slate-600 rounded-lg p-3 mb-4">
        <div className="flex items-center justify-between">
          <span className="text-slate-300 font-medium text-sm">סה"כ קיים:</span>
          <span className="text-white font-bold text-lg">₪{totalPrice.toFixed(2)}</span>
        </div>
      </div>

      {/* Divider */}
      <div className="border-t border-slate-600 pt-4">
        <h6 className="text-white font-medium flex items-center gap-2 text-sm">
          <i className="fas fa-plus text-green-400"></i>הוסף פעולות נוספות
        </h6>
      </div>
    </div>
  );
};

export default ExistingItems;
