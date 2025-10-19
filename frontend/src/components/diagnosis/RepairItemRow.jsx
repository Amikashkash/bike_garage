/**
 * RepairItemRow Component
 *
 * Single row for adding a repair item with:
 * - Description input
 * - Price input
 * - Remove button
 */

const RepairItemRow = ({ index, item, onUpdate, onRemove, showRemove }) => {
  return (
    <div className="repair-item-row">
      <div className="flex flex-col sm:flex-row gap-3 items-stretch sm:items-center">
        {/* Description Input */}
        <div className="flex-1 min-w-0">
          <input
            type="text"
            value={item.description}
            onChange={e => onUpdate(index, 'description', e.target.value)}
            className="w-full px-3 py-2 bg-slate-700/50 border border-slate-600 rounded-lg text-white placeholder-slate-400 text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            placeholder="תיאור הפעולה (לדוגמה: החלפת בלמים קדמיים)"
            required
          />
        </div>

        {/* Price Input and Remove Button */}
        <div className="flex gap-3 items-center">
          <div className="w-32 flex-shrink-0">
            <input
              type="number"
              value={item.price}
              onChange={e => onUpdate(index, 'price', e.target.value)}
              className="w-full px-3 py-2 bg-slate-700/50 border border-slate-600 rounded-lg text-white placeholder-slate-400 text-sm focus:ring-2 focus:ring-green-500 focus:border-transparent"
              placeholder="מחיר (₪)"
              step="10"
              min="0"
              required
            />
          </div>

          {/* Remove Button */}
          <div className="w-10 flex-shrink-0 flex justify-center">
            {showRemove && (
              <button
                type="button"
                onClick={() => onRemove(index)}
                className="w-8 h-8 bg-red-500/20 hover:bg-red-500/30 text-red-400 rounded-lg border border-red-400/40 hover:border-red-400/60 transition-all duration-200 flex items-center justify-center"
                title="הסר פעולה"
              >
                <i className="fas fa-trash text-xs"></i>
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default RepairItemRow;
