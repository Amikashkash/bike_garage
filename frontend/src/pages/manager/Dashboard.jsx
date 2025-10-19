import { useState, useEffect, useRef } from 'react';

// Main Dashboard Component
const ManagerDashboard = () => {
    const [dashboardData, setDashboardData] = useState({
        stuck_repairs: [],
        pending_diagnosis: [],
        pending_approval: [],
        approved_waiting_for_mechanic: [],
        in_progress: [],
        awaiting_quality_check: [],
        repairs_not_collected: []
    });
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        fetchDashboardData();
        const interval = setInterval(fetchDashboardData, 30000); // Refresh every 30 seconds
        return () => clearInterval(interval);
    }, []);

    const fetchDashboardData = async () => {
        try {
            const response = await fetch('/api/manager/dashboard/', {
                credentials: 'same-origin',
                headers: {
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]')?.value || ''
                }
            });

            if (!response.ok) throw new Error('Failed to fetch dashboard data');

            const data = await response.json();
            setDashboardData(data);
            setLoading(false);
        } catch (err) {
            setError(err.message);
            setLoading(false);
        }
    };

    if (loading) {
        return (
            <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900 flex items-center justify-center">
                <div className="text-center">
                    <div className="w-16 h-16 border-4 border-blue-400 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
                    <p className="text-slate-300 text-lg">טוען נתוני דשבורד...</p>
                </div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900 flex items-center justify-center">
                <div className="bg-red-900/20 border border-red-500/30 rounded-2xl p-8 max-w-md mx-auto">
                    <div className="text-center">
                        <i className="fas fa-exclamation-triangle text-red-400 text-4xl mb-4"></i>
                        <h2 className="text-xl font-bold text-white mb-2">שגיאה בטעינת הנתונים</h2>
                        <p className="text-red-200 mb-4">{error}</p>
                        <button
                            onClick={fetchDashboardData}
                            className="bg-red-500/20 hover:bg-red-500/30 text-red-300 px-4 py-2 rounded-lg border border-red-400/40 transition-all duration-200"
                        >
                            נסה שוב
                        </button>
                    </div>
                </div>
            </div>
        );
    }

    return (
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
            <DashboardHeader />
            <DashboardSections data={dashboardData} />
            <EmptyState data={dashboardData} />
            <BackToHome />
            <FloatingActionButton />
        </div>
    );
};

// Dashboard Header Component
const DashboardHeader = () => {
    return (
        <div className="text-center mb-8">
            <div className="flex flex-col md:flex-row md:items-center md:justify-between">
                <div className="mb-4 md:mb-0">
                    <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-500 via-purple-500 to-cyan-500 bg-clip-text text-transparent mb-2">
                        🎯 דשבורד מנהל
                    </h1>
                    <p className="text-slate-300">ניהול תיקונים וזרימת עבודה - מבט כולל על כל הפעילות</p>
                </div>

                <div className="flex gap-3 justify-center md:justify-end flex-wrap">
                    <ActionButton
                        href="/repair/new/"
                        icon="fas fa-plus"
                        text="תיקון חדש"
                        gradient="from-blue-500 to-blue-600 hover:from-blue-600 hover:to-blue-700"
                        title="צור תיקון חדש"
                    />
                    <ActionButton
                        href="/backup/menu/"
                        icon="fas fa-download"
                        text="גיבוי"
                        gradient="from-amber-500 to-orange-500 hover:from-amber-600 hover:to-orange-600"
                        title="גיבוי נתונים"
                    />
                    <ActionButton
                        href="/print-labels/"
                        icon="fas fa-print"
                        text="מדבקות"
                        gradient="from-slate-600 to-slate-700 hover:from-slate-700 hover:to-slate-800"
                        title="הדפסת מדבקות"
                    />
                </div>
            </div>
        </div>
    );
};

// Action Button Component
const ActionButton = ({ href, icon, text, gradient, title }) => {
    return (
        <a
            href={href}
            className={`bg-gradient-to-r ${gradient} text-white font-semibold px-4 py-2 rounded-lg transition-all duration-300 shadow-lg hover:shadow-xl transform hover:scale-105 active:scale-95 inline-flex items-center gap-2`}
            title={title}
        >
            <i className={icon}></i>
            {text}
        </a>
    );
};

// Dashboard Sections Component
const DashboardSections = ({ data }) => {
    const sections = [
        {
            key: 'stuck_repairs',
            title: 'תיקונים תקועים - דרושה עזרה מיידית',
            subtitle: 'פעולה דרושה עכשיו',
            icon: 'fas fa-exclamation-triangle',
            color: 'red',
            bgColor: 'bg-red-900/20',
            borderColor: 'border-red-500/30',
            headerBg: 'bg-red-500/20',
            headerBorder: 'border-red-500/30',
            iconBg: 'bg-red-500/30',
            iconColor: 'text-red-400',
            buttonBg: 'bg-red-500/30',
            buttonText: 'text-red-200',
            buttonBorder: 'border-red-500/40',
            buttonHover: 'hover:bg-red-500/40',
            animate: 'animate-pulse',
            priority: true,
            countSuffix: 'מכונאי מחכה'
        },
        {
            key: 'pending_diagnosis',
            title: 'ממתינים לאבחון',
            subtitle: 'תיקונים שדורשים אבחון ראשוני',
            icon: 'fas fa-search',
            color: 'orange',
            bgColor: 'bg-slate-800/50',
            borderColor: 'border-slate-700',
            headerBg: 'bg-orange-500/20',
            headerBorder: 'border-orange-500/30',
            iconBg: 'bg-orange-500/20',
            iconColor: 'text-orange-400',
            buttonBg: 'bg-orange-500/30',
            buttonText: 'text-orange-200',
            buttonBorder: 'border-orange-500/40',
            buttonHover: 'hover:bg-orange-500/40',
            countSuffix: 'ממתינים'
        },
        {
            key: 'pending_approval',
            title: 'ממתינים לאישור הלקוח',
            subtitle: 'הצעות מחיר שממתינות לאישור',
            icon: 'fas fa-clipboard-check',
            color: 'blue',
            bgColor: 'bg-slate-800/50',
            borderColor: 'border-slate-700',
            headerBg: 'bg-blue-500/20',
            headerBorder: 'border-blue-500/30',
            iconBg: 'bg-blue-500/30',
            iconColor: 'text-blue-400',
            buttonBg: 'bg-blue-500/30',
            buttonText: 'text-blue-200',
            buttonBorder: 'border-blue-500/40',
            buttonHover: 'hover:bg-blue-500/40',
            countSuffix: 'ממתינים'
        },
        {
            key: 'approved_waiting_for_mechanic',
            title: 'מאושרים - ממתינים להקצאת מכונאי',
            subtitle: 'תיקונים מאושרים שצריכים הקצאת מכונאי',
            icon: 'fas fa-user-plus',
            color: 'purple',
            bgColor: 'bg-slate-800/50',
            borderColor: 'border-slate-700',
            headerBg: 'bg-purple-500/20',
            headerBorder: 'border-purple-500/30',
            iconBg: 'bg-purple-500/30',
            iconColor: 'text-purple-400',
            buttonBg: 'bg-purple-500/30',
            buttonText: 'text-purple-200',
            buttonBorder: 'border-purple-500/40',
            buttonHover: 'hover:bg-purple-500/40',
            countSuffix: 'ממתינים'
        },
        {
            key: 'in_progress',
            title: 'בעבודה',
            subtitle: 'תיקונים פעילים כרגע',
            icon: 'fas fa-cogs',
            color: 'green',
            bgColor: 'bg-slate-800/50',
            borderColor: 'border-slate-700',
            headerBg: 'bg-green-500/20',
            headerBorder: 'border-green-500/30',
            iconBg: 'bg-green-500/30',
            iconColor: 'text-green-400',
            buttonBg: 'bg-green-500/30',
            buttonText: 'text-green-200',
            buttonBorder: 'border-green-500/40',
            buttonHover: 'hover:bg-green-500/40',
            countSuffix: 'פעילים'
        },
        {
            key: 'awaiting_quality_check',
            title: 'ממתינים לבדיקת איכות',
            subtitle: 'תיקונים שהושלמו וממתינים לאישור איכות',
            icon: 'fas fa-search-plus',
            color: 'yellow',
            bgColor: 'bg-slate-800/50',
            borderColor: 'border-slate-700',
            headerBg: 'bg-yellow-500/20',
            headerBorder: 'border-yellow-500/30',
            iconBg: 'bg-yellow-500/30',
            iconColor: 'text-yellow-400',
            buttonBg: 'bg-yellow-500/30',
            buttonText: 'text-yellow-200',
            buttonBorder: 'border-yellow-500/40',
            buttonHover: 'hover:bg-yellow-500/40',
            countSuffix: 'לבדיקה'
        },
        {
            key: 'repairs_not_collected',
            title: 'מוכנים לאיסוף',
            subtitle: 'אופניים שהושלמו וממתינים לאיסוף',
            icon: 'fas fa-check-circle',
            color: 'cyan',
            bgColor: 'bg-slate-800/50',
            borderColor: 'border-slate-700',
            headerBg: 'bg-cyan-500/20',
            headerBorder: 'border-cyan-500/30',
            iconBg: 'bg-cyan-500/30',
            iconColor: 'text-cyan-400',
            buttonBg: 'bg-cyan-500/30',
            buttonText: 'text-cyan-200',
            buttonBorder: 'border-cyan-500/40',
            buttonHover: 'hover:bg-cyan-500/40',
            countSuffix: 'מוכנים'
        }
    ];

    return (
        <div className="space-y-6">
            {sections.map(section => {
                const repairs = data[section.key] || [];
                if (repairs.length === 0) return null;

                return (
                    <DashboardSection
                        key={section.key}
                        section={section}
                        repairs={repairs}
                    />
                );
            })}
        </div>
    );
};

// Dashboard Section Component
const DashboardSection = ({ section, repairs }) => {
    const [isExpanded, setIsExpanded] = useState(false);

    const toggleSection = () => {
        setIsExpanded(!isExpanded);
    };

    return (
        <div className={`${section.bgColor} backdrop-blur-sm border ${section.borderColor} rounded-2xl overflow-hidden ${section.animate || ''}`}>
            {/* Section Header */}
            <div className={`${section.headerBg} px-6 py-4 border-b ${section.headerBorder}`}>
                <div className="flex items-center justify-between">
                    <div className="flex items-center gap-4">
                        <div className={`w-12 h-12 ${section.iconBg} rounded-xl flex items-center justify-center`}>
                            <i className={`${section.icon} ${section.iconColor} text-xl ${section.animate || ''}`}></i>
                        </div>
                        <div>
                            <h2 className="text-xl font-bold text-white">{section.title}</h2>
                            <p className={`${section.buttonText} text-sm`}>{section.subtitle}</p>
                        </div>
                    </div>
                    <button
                        className={`flex items-center justify-between w-48 md:w-56 px-4 py-3 ${section.buttonBg} ${section.buttonText} rounded-lg border ${section.buttonBorder} ${section.buttonHover} transition-all duration-300 cursor-pointer ${section.animate || ''}`}
                        onClick={toggleSection}
                    >
                        <div className="flex items-center gap-2">
                            <i className={section.icon}></i>
                            <span className="text-sm md:text-base">
                                {repairs.length} {section.countSuffix}
                            </span>
                        </div>
                        <i className={`fas fa-chevron-down transition-transform duration-300 text-sm ${isExpanded ? 'rotate-180' : ''}`}></i>
                    </button>
                </div>
            </div>

            {/* Section Content */}
            <div className={`transition-all duration-500 ease-in-out overflow-hidden ${isExpanded ? 'max-h-screen opacity-100' : 'max-h-0 opacity-0'}`}>
                <div className="p-6">
                    <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6">
                        {repairs.map(repair => (
                            <RepairCard
                                key={repair.id}
                                repair={repair}
                                section={section}
                            />
                        ))}
                    </div>
                </div>
            </div>
        </div>
    );
};

// Mark as picked up function
const markAsPickedUp = (repairId) => {
    if (!confirm('האם לסמן את האופניים כנאספו על ידי הלקוח?')) {
        return;
    }

    const button = document.querySelector(`button[onclick*="markAsPickedUp(${repairId})"]`);
    if (button) {
        button.disabled = true;
        button.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
    }

    fetch(`/manager/mark-delivered/${repairId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]')?.value || '',
            'Content-Type': 'application/json',
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            const card = button.closest('.bg-slate-800\\/60');
            if (card) {
                card.style.transition = 'all 0.5s ease-out';
                card.style.opacity = '0';
                card.style.transform = 'scale(0.9)';
                setTimeout(() => {
                    card.remove();
                }, 500);
            }
            alert('האופניים סומנו כנאספו בהצלחה!');
        } else {
            alert('שגיאה בעדכון הסטטוס: ' + (data.error || 'שגיאה לא ידועה'));
            if (button) {
                button.disabled = false;
                button.innerHTML = '<i class="fas fa-check"></i>';
            }
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('שגיאה בעדכון הסטטוס. נסה שוב.');
        if (button) {
            button.disabled = false;
            button.innerHTML = '<i class="fas fa-check"></i>';
        }
    });
};

// Repair Card Component
const RepairCard = ({ repair, section }) => {
    const getCardActions = () => {
        switch (section.key) {
            case 'stuck_repairs':
                return (
                    <div className="flex items-center justify-between gap-3">
                        <a href={`/repair/status/${repair.id}/`}
                           className="flex items-center gap-2 px-4 py-2 bg-slate-700/50 hover:bg-slate-600/50 text-slate-300 hover:text-white rounded-lg border border-slate-600 hover:border-slate-500 transition-all duration-200">
                            <i className="fas fa-eye"></i>
                            <span className="text-sm">צפה</span>
                        </a>
                        <a href={`/manager/repair/${repair.id}/`}
                           className={`flex items-center gap-2 px-4 py-2 bg-${section.color}-500/20 hover:bg-${section.color}-500/30 text-${section.color}-300 hover:text-${section.color}-200 rounded-lg border border-${section.color}-400/40 hover:border-${section.color}-400/60 transition-all duration-200`}>
                            <i className="fas fa-reply"></i>
                            <span className="text-sm">הגב</span>
                        </a>
                    </div>
                );

            case 'pending_diagnosis':
                return (
                    <a href={`/manager/repair/${repair.id}/diagnosis/`}
                       className={`flex items-center gap-2 px-6 py-2 bg-${section.color}-500/20 hover:bg-${section.color}-500/30 text-${section.color}-300 hover:text-${section.color}-200 rounded-lg border border-${section.color}-400/40 hover:border-${section.color}-400/60 transition-all duration-200 w-full justify-center`}>
                        <i className="fas fa-stethoscope"></i>
                        <span className="text-sm font-medium">אבחן עכשיו</span>
                    </a>
                );

            case 'pending_approval':
                return (
                    <a href={`/customer/approval/${repair.id}/`}
                       className={`flex items-center gap-2 px-6 py-2 bg-${section.color}-500/20 hover:bg-${section.color}-500/30 text-${section.color}-300 hover:text-${section.color}-200 rounded-lg border border-${section.color}-400/40 hover:border-${section.color}-400/60 transition-all duration-200 w-full justify-center`}>
                        <i className="fas fa-check"></i>
                        <span className="text-sm font-medium">נהל אישור</span>
                    </a>
                );

            case 'approved_waiting_for_mechanic':
                return (
                    <a href={`/assign/mechanic/${repair.id}/`}
                       className={`flex items-center gap-2 px-6 py-2 bg-${section.color}-500/20 hover:bg-${section.color}-500/30 text-${section.color}-300 hover:text-${section.color}-200 rounded-lg border border-${section.color}-400/40 hover:border-${section.color}-400/60 transition-all duration-200 w-full justify-center`}>
                        <i className="fas fa-user-plus"></i>
                        <span className="text-sm font-medium">הקצה מכונאי</span>
                    </a>
                );

            case 'in_progress':
                return (
                    <a href={`/repair/status/${repair.id}/`}
                       className={`flex items-center gap-2 px-6 py-2 bg-${section.color}-500/20 hover:bg-${section.color}-500/30 text-${section.color}-300 hover:text-${section.color}-200 rounded-lg border border-${section.color}-400/40 hover:border-${section.color}-400/60 transition-all duration-200 w-full justify-center`}>
                        <i className="fas fa-eye"></i>
                        <span className="text-sm font-medium">צפה בפרטים</span>
                    </a>
                );

            case 'awaiting_quality_check':
                return (
                    <a href={`/manager/quality-check/${repair.id}/`}
                       className={`flex items-center gap-2 px-6 py-2 bg-${section.color}-500/20 hover:bg-${section.color}-500/30 text-${section.color}-300 hover:text-${section.color}-200 rounded-lg border border-${section.color}-400/40 hover:border-${section.color}-400/60 transition-all duration-200 w-full justify-center`}>
                        <i className="fas fa-check-double"></i>
                        <span className="text-sm font-medium">בדוק איכות</span>
                    </a>
                );

            case 'repairs_not_collected':
                return (
                    <div className="flex items-center justify-between gap-2">
                        <a href={`/repair/status/${repair.id}/`}
                           className="flex items-center gap-1 px-3 py-2 bg-slate-700/50 hover:bg-slate-600/50 text-slate-300 hover:text-white rounded-lg border border-slate-600 hover:border-slate-500 transition-all duration-200 text-xs">
                            <i className="fas fa-eye"></i>
                            <span>צפה</span>
                        </a>
                        <a href={`tel:${repair.bike?.customer?.phone || ''}`}
                           className={`flex items-center gap-1 px-3 py-2 bg-${section.color}-500/20 hover:bg-${section.color}-500/30 text-${section.color}-300 hover:text-${section.color}-200 rounded-lg border border-${section.color}-400/40 hover:border-${section.color}-400/60 transition-all duration-200 text-xs`}>
                            <i className="fas fa-phone"></i>
                            <span>התקשר</span>
                        </a>
                        <button
                            onClick={() => markAsPickedUp(repair.id)}
                            className="flex items-center gap-1 px-3 py-2 bg-green-500/20 hover:bg-green-500/30 text-green-300 hover:text-green-200 rounded-lg border border-green-400/40 hover:border-green-400/60 transition-all duration-200 text-xs">
                            <i className="fas fa-check"></i>
                            <span>נאסף</span>
                        </button>
                    </div>
                );

            default:
                return null;
        }
    };

    const getBadgeContent = () => {
        switch (section.key) {
            case 'stuck_repairs':
                return { text: 'דרושה עזרה', color: 'bg-red-500/30 border-red-400/40 text-red-200', animate: 'animate-pulse' };
            case 'pending_approval':
                return { text: `₪${repair.get_total_price || '0'}`, color: 'bg-green-500/30 border-green-400/40 text-green-200' };
            case 'approved_waiting_for_mechanic':
                return { text: `₪${repair.get_total_approved_price || '0'}`, color: 'bg-green-500/30 border-green-400/40 text-green-200' };
            case 'in_progress':
                return { text: `${repair.progress_percentage || 0}%`, color: 'bg-green-500/30 border-green-400/40 text-green-200' };
            case 'awaiting_quality_check':
                return { text: 'בדיקת איכות', color: `bg-${section.color}-500/30 border-${section.color}-400/40 text-${section.color}-200` };
            case 'repairs_not_collected':
                return { text: 'מוכן לאיסוף', color: `bg-${section.color}-500/30 border-${section.color}-400/40 text-${section.color}-200` };
            default:
                return null;
        }
    };

    const badge = getBadgeContent();

    return (
        <div className={`bg-slate-800/60 backdrop-blur-sm border border-${section.color}-400/40 rounded-xl overflow-hidden hover:border-${section.color}-400/60 transition-all duration-300 hover:shadow-lg hover:shadow-${section.color}-500/20`}>
            {/* Card Header */}
            <div className={`bg-${section.color}-500/10 border-b border-${section.color}-400/30 p-4`}>
                <div className="flex items-center justify-between">
                    <div className="flex items-center gap-3">
                        <div className={`w-10 h-10 bg-${section.color}-500/20 rounded-lg flex items-center justify-center`}>
                            <i className={`${section.icon} ${section.iconColor} ${section.key === 'in_progress' ? 'animate-spin' : ''} ${section.key === 'stuck_repairs' ? 'animate-pulse' : ''}`}></i>
                        </div>
                        <div>
                            <h3 className="text-lg font-bold text-white">#{repair.id}</h3>
                            <p className={`${section.buttonText} text-sm`}>
                                {repair.bike?.brand} {repair.bike?.model}
                            </p>
                        </div>
                    </div>
                    {badge && (
                        <div className={`px-3 py-1 rounded-full border ${badge.color} ${badge.animate || ''}`}>
                            <span className="text-xs font-bold">{badge.text}</span>
                        </div>
                    )}
                </div>
            </div>

            {/* Card Body */}
            <div className="p-4 space-y-3">
                <div className="flex items-center gap-3 text-sm">
                    <i className="fas fa-user text-slate-400 w-4"></i>
                    <span className="text-white">{repair.bike?.customer?.name || 'ללא שם'}</span>
                </div>

                {repair.assigned_mechanic && (
                    <div className="flex items-center gap-3 text-sm">
                        <i className="fas fa-wrench text-slate-400 w-4"></i>
                        <span className="text-white">
                            {repair.assigned_mechanic.get_full_name || repair.assigned_mechanic.username}
                        </span>
                    </div>
                )}

                <div className="flex items-center gap-3 text-sm">
                    <i className={`fas fa-clock ${section.iconColor} w-4`}></i>
                    <span className={section.buttonText}>
                        {section.key === 'stuck_repairs' ? `תקוע ${repair.created_at_display || ''}` :
                         section.key === 'pending_diagnosis' ? 'ממתין לאבחון' :
                         section.key === 'pending_approval' ? 'ממתין לאישור הלקוח' :
                         section.key === 'approved_waiting_for_mechanic' ? 'ממתין להקצאת מכונאי' :
                         section.key === 'in_progress' ? 'בעבודה כרגע' :
                         section.key === 'awaiting_quality_check' ? 'ממתין לבדיקת איכות' :
                         section.key === 'repairs_not_collected' ? `הושלם ${repair.completed_at_display || ''}` :
                         'סטטוס לא ידוע'}
                    </span>
                </div>

                {/* Special content for stuck repairs */}
                {section.key === 'stuck_repairs' && repair.stuck_reason && (
                    <div className="bg-red-500/10 border border-red-400/30 rounded-lg p-3 mt-3">
                        <div className="flex items-start gap-2">
                            <i className="fas fa-exclamation-circle text-red-400 mt-0.5"></i>
                            <span className="text-red-200 text-sm">{repair.stuck_reason}</span>
                        </div>
                    </div>
                )}

                {/* Additional info for ready for collection */}
                {section.key === 'repairs_not_collected' && (
                    <div className="flex items-center gap-3 text-sm">
                        <i className="fas fa-shekel-sign text-green-400 w-4"></i>
                        <span className="text-green-300">₪{repair.get_total_approved_price || '0'}</span>
                    </div>
                )}
            </div>

            {/* Card Footer */}
            <div className={`border-t border-${section.color}-400/30 bg-${section.color}-500/5 p-4`}>
                <div className="flex items-center justify-center">
                    {getCardActions()}
                </div>
            </div>
        </div>
    );
};

// Empty State Component
const EmptyState = ({ data }) => {
    const hasAnyData = Object.values(data).some(arr => arr && arr.length > 0);

    if (hasAnyData) return null;

    return (
        <div className="text-center py-20">
            <div className="bg-slate-800/50 backdrop-blur-sm border border-slate-700 rounded-2xl p-12 max-w-2xl mx-auto">
                <div className="w-24 h-24 bg-green-500/20 rounded-full flex items-center justify-center mx-auto mb-6">
                    <i className="fas fa-clipboard-check text-green-400 text-4xl"></i>
                </div>
                <h2 className="text-2xl font-bold text-white mb-4">כל התיקונים במצב תקין</h2>
                <p className="text-slate-400 mb-8">אין תיקונים הדורשים טיפול מיוחד כרגע</p>
                <a href="/" className="bg-gradient-to-r from-blue-500 to-blue-600 hover:from-blue-600 hover:to-blue-700 text-white font-bold px-8 py-4 rounded-xl transition-all duration-300 shadow-lg hover:shadow-xl transform hover:scale-105 active:scale-95 inline-flex items-center gap-2">
                    <i className="fas fa-home"></i>חזרה לדף הבית
                </a>
            </div>
        </div>
    );
};

// Back to Home Component
const BackToHome = () => {
    return (
        <div className="text-center mt-8">
            <a href="/" className="bg-gradient-to-r from-slate-600 to-slate-700 hover:from-slate-700 hover:to-slate-800 text-white font-semibold px-6 py-3 rounded-lg transition-all duration-300 shadow-lg hover:shadow-xl transform hover:scale-105 active:scale-95 inline-flex items-center gap-2">
                <i className="fas fa-home"></i>חזרה לדף הבית
            </a>
        </div>
    );
};

// Floating Action Button Component
const FloatingActionButton = () => {
    return (
        <div className="fixed bottom-6 left-6 z-40">
            <a href="/repair/new/"
               className="group flex items-center gap-3 bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700 text-white px-4 py-3 rounded-full shadow-lg hover:shadow-xl transition-all duration-300 transform hover:scale-105 border border-blue-400/20"
               title="צור תיקון חדש">
                <i className="fas fa-plus text-lg"></i>
                <span className="hidden group-hover:inline-block transition-all duration-300 text-sm font-medium">תיקון חדש</span>
            </a>
        </div>
    );
};

export default ManagerDashboard;

// Initialize and render the app
import { createRoot } from 'react-dom/client';

const rootElement = document.getElementById('root');
if (rootElement) {
    const root = createRoot(rootElement);
    root.render(<ManagerDashboard />);
}
