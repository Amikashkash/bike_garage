// Standalone React component for customer approval
(function() {
  'use strict';
  
  const { useState, useEffect, createElement: e } = React;
  
  function CustomerApproval({ repairData, csrfToken, submitUrl }) {
    const [selectedItems, setSelectedItems] = useState(new Set());
    const [confirmed, setConfirmed] = useState(false);
    const [submitting, setSubmitting] = useState(false);
    const [error, setError] = useState(null);

    useEffect(() => {
      // Pre-select already approved items
      const preSelected = new Set();
      repairData.repair_items?.forEach(item => {
        if (item.is_approved_by_customer) {
          preSelected.add(item.id);
        }
      });
      setSelectedItems(preSelected);
    }, [repairData]);

    const handleItemToggle = (itemId) => {
      const newSelected = new Set(selectedItems);
      if (newSelected.has(itemId)) {
        newSelected.delete(itemId);
      } else {
        newSelected.add(itemId);
      }
      setSelectedItems(newSelected);
    };

    const handleSubmit = async (e) => {
      e.preventDefault();
      if (selectedItems.size === 0 || !confirmed) return;

      setSubmitting(true);
      setError(null);
      
      try {
        const formData = new FormData();
        formData.append('csrfmiddlewaretoken', csrfToken);
        selectedItems.forEach(itemId => {
          formData.append('approved_items', itemId);
        });

        const response = await fetch(submitUrl, {
          method: 'POST',
          body: formData
        });

        if (response.ok) {
          showSuccessMessage('הפעולות אושרו בהצלחה!');
          setTimeout(() => {
            window.location.href = '/';
          }, 2000);
        } else {
          throw new Error('Failed to submit approval');
        }
      } catch (err) {
        setError('שגיאה בשליחת האישור. נסה שוב.');
      } finally {
        setSubmitting(false);
      }
    };

    const showSuccessMessage = (message) => {
      const div = document.createElement('div');
      div.className = 'success-message';
      div.innerHTML = `<i class="fas fa-check-circle" style="margin-left: 0.5rem;"></i>${message}`;
      document.body.appendChild(div);
      
      setTimeout(() => {
        if (document.body.contains(div)) {
          document.body.removeChild(div);
        }
      }, 3000);
    };

    const calculateTotal = () => {
      let total = 0;
      let count = 0;
      
      repairData.repair_items?.forEach(item => {
        if (selectedItems.has(item.id)) {
          total += parseFloat(item.price || 0);
          count++;
        }
      });
      
      return { count, total };
    };

    const formatDate = (dateString) => {
      return new Date(dateString).toLocaleDateString('he-IL', {
        day: '2-digit',
        month: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
      });
    };

    const { count, total } = calculateTotal();
    const canSubmit = count > 0 && confirmed && !submitting;

    return e('div', { className: 'approval-container' },
      // Header
      e('div', { className: 'text-center mb-8' },
        e('div', { className: 'mobile-hidden' },
          e('h1', { className: 'text-4xl font-bold text-white mb-2' },
            '📋 אישור תיקון #', repairData.repair_id
          )
        ),
        e('div', { className: 'md:hidden' },
          e('h1', { className: 'text-2xl font-bold text-white mb-2' },
            'אישור תיקון #', repairData.repair_id
          )
        ),
        e('p', { className: 'text-slate-400 text-lg' },
          'בחר את הפעולות שברצונך לאשר'
        )
      ),

      // Error message
      error && e('div', { className: 'card bg-danger mb-6 p-4' },
        e('div', { className: 'flex items-center gap-3' },
          e('i', { className: 'fas fa-exclamation-triangle color-danger text-xl' }),
          e('p', { className: 'color-danger font-medium' }, error)
        )
      ),

      // Main layout
      e('div', { className: 'grid grid-cols-1 lg:grid-cols-3 gap-6' },
        // Left column - Repair Details
        e('div', { className: 'lg:col-span-1' },
          e('div', { className: 'card p-6 space-y-6' },
            e('div', { className: 'border-b border-slate-700 pb-4' },
              e('h3', { className: 'text-xl font-bold text-white flex items-center gap-2 mb-4' },
                e('i', { className: 'fas fa-bicycle color-info' }),
                'פרטי התיקון'
              )
            ),
            
            // Bike info
            e('div', { className: 'bg-primary p-4 rounded-lg' },
              e('div', { className: 'flex items-center gap-3' },
                e('div', { className: 'w-12 h-12 bg-blue-500/30 rounded-lg flex items-center justify-center' },
                  e('i', { className: 'fas fa-bicycle text-blue-400 text-xl' })
                ),
                e('div', null,
                  e('div', { className: 'text-white font-bold text-lg' },
                    repairData.bike_info.brand + ' ' + repairData.bike_info.model
                  ),
                  e('div', { className: 'color-primary text-sm' },
                    'לקוח: ' + repairData.bike_info.customer_name
                  )
                )
              )
            ),

            // Status info
            e('div', { className: 'space-y-3' },
              e('div', { className: 'flex justify-between items-center py-2 border-b border-slate-700/50' },
                e('span', { className: 'text-slate-400' }, 'תאריך דיווח:'),
                e('span', { className: 'text-white font-medium' }, formatDate(repairData.created_at))
              ),
              e('div', { className: 'flex justify-between items-center py-2' },
                e('span', { className: 'text-slate-400' }, 'סטטוס:'),
                e('span', { className: 'status-badge bg-success color-success' },
                  e('i', { className: 'fas fa-check-circle' }),
                  repairData.status_display
                )
              )
            ),

            // Problem description
            repairData.problem_description && e('div', null,
              e('h4', { className: 'text-white font-bold mb-2 flex items-center gap-2' },
                e('i', { className: 'fas fa-exclamation-circle color-danger' }),
                'התקלה שדיווחת:'
              ),
              e('div', { className: 'bg-danger p-3 rounded-lg' },
                e('p', { className: 'text-red-100 text-sm leading-relaxed' },
                  repairData.problem_description
                )
              )
            ),

            // Diagnosis
            repairData.diagnosis && e('div', null,
              e('h4', { className: 'text-white font-bold mb-2 flex items-center gap-2' },
                e('i', { className: 'fas fa-stethoscope color-success' }),
                'אבחון המוסך:'
              ),
              e('div', { className: 'bg-success p-3 rounded-lg' },
                e('p', { className: 'text-green-100 text-sm leading-relaxed' },
                  repairData.diagnosis
                )
              )
            )
          )
        ),

        // Right column - Main content
        e('div', { className: 'lg:col-span-2 space-y-6' },
          // Repair items
          repairData.repair_items && repairData.repair_items.length > 0 ? 
            e('div', { className: 'card p-6' },
              e('h3', { className: 'text-xl font-bold text-white mb-6 flex items-center gap-2' },
                e('i', { className: 'fas fa-tools color-warning' }),
                'פעולות תיקון מוצעות'
              ),
              
              e('div', { className: 'space-y-4' },
                ...repairData.repair_items.map(item =>
                  e('div', {
                    key: item.id,
                    className: `repair-item ${selectedItems.has(item.id) ? 'selected' : ''}`,
                    onClick: () => handleItemToggle(item.id)
                  },
                    e('div', { className: 'flex items-start gap-4' },
                      e('div', { className: 'flex-shrink-0 mt-1' },
                        e('input', {
                          type: 'checkbox',
                          className: 'custom-checkbox',
                          checked: selectedItems.has(item.id),
                          onChange: () => {}
                        })
                      ),
                      
                      e('div', { className: 'flex-1 min-w-0' },
                        e('div', { className: 'mobile-grid-fix flex justify-between items-start gap-4' },
                          e('div', { className: 'flex-1' },
                            e('h4', { className: 'text-white font-bold text-lg mb-2 flex items-center gap-2' },
                              e('i', { className: 'fas fa-wrench color-info' }),
                              item.description
                            ),
                            item.notes && e('p', { className: 'text-slate-400 text-sm bg-slate-700/50 p-2 rounded' },
                              e('i', { className: 'fas fa-sticky-note color-warning ml-1' }),
                              item.notes
                            )
                          ),
                          e('div', { className: 'flex-shrink-0 mobile-text-center mobile-full-width' },
                            e('div', { className: 'price-tag' },
                              '₪' + parseFloat(item.price).toFixed(0)
                            )
                          )
                        )
                      )
                    )
                  )
                )
              )
            ) :
            e('div', { className: 'card p-8 text-center' },
              e('div', { className: 'w-16 h-16 bg-warning mx-auto mb-4 rounded-full flex items-center justify-center' },
                e('i', { className: 'fas fa-clock color-warning text-2xl' })
              ),
              e('h3', { className: 'text-white font-bold text-xl mb-2' }, 'המתן לאבחון המוסך'),
              e('p', { className: 'text-slate-400' }, 'המוסך עדיין לא הוסיף פעולות לתיקון זה')
            ),

          // Summary and actions
          repairData.repair_items && repairData.repair_items.length > 0 && [
            // Summary
            e('div', { key: 'summary', className: 'card p-6' },
              e('h3', { className: 'text-xl font-bold text-white mb-6 flex items-center gap-2' },
                e('i', { className: 'fas fa-calculator color-info' }),
                'סיכום הזמנה'
              ),
              
              e('div', { className: 'mobile-grid-fix grid grid-cols-2 gap-4' },
                e('div', { className: 'bg-primary p-4 rounded-lg text-center' },
                  e('div', { className: 'text-3xl font-bold color-primary mb-1' }, count),
                  e('div', { className: 'text-blue-200 text-sm' }, 'פעולות נבחרו')
                ),
                e('div', { className: 'bg-success p-4 rounded-lg text-center' },
                  e('div', { className: 'text-3xl font-bold color-success mb-1' }, '₪' + total.toFixed(0)),
                  e('div', { className: 'text-green-200 text-sm' }, 'סה״כ מחיר')
                )
              )
            ),

            // Confirmation
            e('div', { key: 'confirmation', className: 'card p-6' },
              e('div', {
                className: 'flex items-start gap-4 cursor-pointer p-4 rounded-lg bg-warning transition-all hover:bg-yellow-500/20',
                onClick: () => setConfirmed(!confirmed)
              },
                e('div', { className: 'flex-shrink-0 mt-1' },
                  e('input', {
                    type: 'checkbox',
                    className: 'custom-checkbox',
                    checked: confirmed,
                    onChange: () => {}
                  })
                ),
                e('div', null,
                  e('h4', { className: 'text-white font-bold text-lg mb-3 flex items-center gap-2' },
                    e('i', { className: 'fas fa-signature color-warning' }),
                    'אישור ביצוע הפעולות'
                  ),
                  e('div', { className: 'text-yellow-100 text-sm space-y-1 leading-relaxed' },
                    e('div', null, '✓ אני מאשר/ת את ביצוע הפעולות שנבחרו'),
                    e('div', null, '✓ אני מסכים/ה לתשלום בסכום של ₪' + total.toFixed(0)),
                    e('div', null, '✓ אני מבין/ה שלא ניתן לבטל לאחר האישור')
                  )
                )
              )
            ),

            // Action buttons
            e('div', { key: 'buttons', className: 'mobile-stack flex gap-4' },
              e('button', {
                type: 'button',
                onClick: handleSubmit,
                disabled: !canSubmit,
                className: 'btn btn-success mobile-full-width flex-1'
              },
                submitting ? [
                  e('div', { key: 'spinner', className: 'loading-spinner' }),
                  'שולח אישור...'
                ] : [
                  e('i', { key: 'icon', className: 'fas fa-check-double' }),
                  `אשר ${count} פעולות (₪${total.toFixed(0)})`
                ]
              ),
              
              e('a', {
                href: '/',
                className: 'btn btn-secondary mobile-full-width'
              },
                e('i', { className: 'fas fa-home' }),
                'חזרה לדף הבית'
              )
            )
          ]
        )
      ),

      // Help text
      e('div', { className: 'card bg-info p-4 mt-8' },
        e('div', { className: 'flex items-start gap-3' },
          e('i', { className: 'fas fa-info-circle color-info text-xl mt-1' }),
          e('div', { className: 'text-blue-100 text-sm' },
            e('p', { className: 'font-medium mb-1' }, 'איך זה עובד?'),
            e('p', null, 'בחר את הפעולות שברצונך שהמוסך יבצע ולחץ על "אשר". לאחר האישור, הפעולות יועברו לביצוע והמוסך יתחיל לעבוד על האופניים שלך.')
          )
        )
      )
    );
  }

  // Make component available globally
  window.CustomerApproval = CustomerApproval;
})();