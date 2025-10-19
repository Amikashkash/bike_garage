/**
 * NotificationSettings Component
 *
 * Notification settings section with:
 * - Send notification checkbox
 * - Notification preview
 * - Customer contact info display
 */

const NotificationSettings = ({ sendNotification, onToggle, customer, bike }) => {
  return (
    <div className="bg-slate-800/50 backdrop-blur-sm border border-slate-700 rounded-xl p-6 mt-6">
      {/* Header */}
      <h3 className="text-lg font-bold text-white mb-4 flex items-center gap-2">
        <i className="fas fa-bell text-blue-400"></i>
        התראות ללקוח
      </h3>

      <div className="space-y-4">
        {/* Send Notification Checkbox */}
        <div className="flex items-start gap-3 p-3 bg-slate-700/30 rounded-lg">
          <div className="flex-shrink-0 mt-1">
            <input
              type="checkbox"
              id="send-notification"
              checked={sendNotification}
              onChange={e => onToggle(e.target.checked)}
              className="w-5 h-5 text-blue-500 bg-slate-600 border-slate-500 rounded focus:ring-blue-500 focus:ring-2"
            />
          </div>
          <label htmlFor="send-notification" className="flex-1 cursor-pointer">
            <div className="text-white font-medium mb-1">📱 שלח התראה ללקוח</div>
            <div className="text-slate-400 text-sm">
              הלקוח יקבל התראת דחיפה ואימייל עם בקשה לאישור הפעולות
            </div>
          </label>
        </div>

        {/* Notification Preview */}
        {sendNotification && (
          <div className="bg-blue-500/10 border border-blue-400/30 rounded-lg p-3">
            <div className="flex items-start gap-3">
              <i className="fas fa-mobile-alt text-blue-400 text-lg mt-1"></i>
              <div className="flex-1">
                <div className="text-blue-200 font-medium text-sm mb-1">
                  תצוגה מקדימה של ההתראה:
                </div>
                <div className="text-blue-100 text-sm">
                  "נדרש אישור - תיקון {bike.brand} {bike.model}"
                  <br />
                  <span className="text-blue-300">
                    האבחון לתיקון האופניים {bike.brand} {bike.model} מוכן. יש צורך באישור שלך
                    לפעולות התיקון.
                  </span>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Customer Contact Info */}
        <div className="flex flex-wrap items-center gap-3 text-sm">
          <div className="flex items-center gap-2 text-slate-400">
            <i className="fas fa-user"></i>
            <span>{customer.name}</span>
          </div>
          {customer.phone && (
            <div className="flex items-center gap-2 text-slate-400">
              <i className="fas fa-phone"></i>
              <span>{customer.phone}</span>
            </div>
          )}
          {customer.email ? (
            <div className="flex items-center gap-2 text-slate-400">
              <i className="fas fa-envelope"></i>
              <span>{customer.email}</span>
            </div>
          ) : (
            <div className="flex items-center gap-2 text-yellow-400">
              <i className="fas fa-exclamation-triangle"></i>
              <span className="text-sm">אין אימייל - רק התראת דחיפה</span>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default NotificationSettings;
