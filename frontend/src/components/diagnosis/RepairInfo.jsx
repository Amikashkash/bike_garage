/**
 * RepairInfo Component
 *
 * Displays repair information sidebar including:
 * - Bike and customer details
 * - Subcategories
 * - Problem description
 */

const RepairInfo = ({ repair, onCategoryClick }) => {
  return (
    <div className="bg-slate-800/50 backdrop-blur-sm border border-slate-700 rounded-xl overflow-hidden h-fit">
      {/* Header */}
      <div className="bg-blue-500/20 px-4 py-3 border-b border-blue-500/30">
        <h3 className="text-lg font-bold text-white flex items-center gap-2">
          <i className="fas fa-info-circle text-blue-400"></i>פרטי התיקון
        </h3>
      </div>

      <div className="p-4 space-y-3">
        {/* Bike & Customer Info */}
        <div className="flex items-center gap-3 p-3 bg-slate-700/50 border border-slate-600 rounded-lg">
          <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg flex items-center justify-center">
            <i className="fas fa-bicycle text-white"></i>
          </div>
          <div className="flex-1 min-w-0">
            <h4 className="font-bold text-white text-base truncate">
              {repair.bike.brand} {repair.bike.model}
            </h4>
            <p className="text-slate-300 text-sm truncate">{repair.customer.name}</p>
          </div>
        </div>

        {/* Contact Info */}
        <div className="space-y-2 text-sm">
          <div className="flex items-center justify-between">
            <span className="text-slate-300">טלפון:</span>
            <span className="text-white font-medium">{repair.customer.phone || 'לא צוין'}</span>
          </div>
          <div className="flex items-center justify-between">
            <span className="text-slate-300">תאריך:</span>
            <span className="text-white font-medium">{repair.created_at}</span>
          </div>
        </div>

        {/* Subcategories */}
        {repair.subcategories && repair.subcategories.length > 0 && (
          <div>
            <h6 className="text-white font-medium mb-2 flex items-center gap-2 text-sm">
              <i className="fas fa-tags text-yellow-400"></i>קטגוריות התקלה
            </h6>
            <div className="space-y-1">
              {repair.subcategories.map(subcategory => (
                <div
                  key={subcategory.id}
                  onClick={() => onCategoryClick(subcategory.name)}
                  className="bg-yellow-500/10 border border-yellow-400/30 rounded-lg p-2 cursor-pointer transition-all hover:bg-yellow-500/20"
                  title="לחץ להוספה לתיאור הפעולה"
                >
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2 min-w-0 flex-1">
                      <i className="fas fa-tag text-yellow-400 text-xs flex-shrink-0"></i>
                      <span className="text-yellow-100 font-medium text-sm truncate">
                        {subcategory.name}
                      </span>
                    </div>
                    <i className="fas fa-plus-circle text-yellow-400 text-xs flex-shrink-0"></i>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Problem Description */}
        {repair.problem_description && (
          <div>
            <h6 className="text-white font-medium mb-2 flex items-center gap-2 text-sm">
              <i className="fas fa-exclamation-triangle text-red-400"></i>תיאור התקלה
            </h6>
            <div className="bg-red-500/10 border border-red-400/30 rounded-lg p-3">
              <p className="text-red-100 text-sm">{repair.problem_description}</p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default RepairInfo;
