import { useState, useEffect } from 'react';

// Main Mechanic Dashboard Component
const MechanicDashboard = () => {
    const [dashboardData, setDashboardData] = useState({
        assigned_repairs: [],
        stats: {
            total_assigned: 0,
            completed: 0,
            in_progress: 0,
            stuck: 0
        },
        user_info: {}
    });
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [searchTerm, setSearchTerm] = useState('');
    const [filterType, setFilterType] = useState('all');
    const [expandedCards, setExpandedCards] = useState({});

    useEffect(() => {
        fetchDashboardData();
        const interval = setInterval(fetchDashboardData, 30000); // Refresh every 30 seconds
        return () => clearInterval(interval);
    }, []);

    const fetchDashboardData = async () => {
        try {
            const response = await fetch('/api/mechanic/dashboard/', {
                credentials: 'same-origin',
                headers: {
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]')?.value || ''
                }
            });

            if (!response.ok) {
                throw new Error('Failed to fetch dashboard data');
            }

            const data = await response.json();
            setDashboardData(data);
            setLoading(false);
        } catch (err) {
            setError(err.message);
            setLoading(false);
        }
    };

    const toggleCard = (cardId) => {
        setExpandedCards(prev => ({
            ...prev,
            [cardId]: !prev[cardId]
        }));
    };

    const filteredRepairs = dashboardData.assigned_repairs.filter(repair => {
        const matchesSearch = searchTerm === '' ||
            repair.bike?.brand?.toLowerCase().includes(searchTerm.toLowerCase()) ||
            repair.bike?.model?.toLowerCase().includes(searchTerm.toLowerCase()) ||
            repair.bike?.customer?.name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
            repair.id.toString().includes(searchTerm);

        const matchesFilter = filterType === 'all' ||
            (filterType === 'pending' && !repair.is_stuck && repair.progress_percentage < 100) ||
            (filterType === 'completed' && repair.progress_percentage === 100) ||
            (filterType === 'stuck' && repair.is_stuck);

        return matchesSearch && matchesFilter;
    });

    if (loading) {
        return (
            <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900 flex items-center justify-center">
                <div className="text-center">
                    <div className="w-16 h-16 border-4 border-orange-400 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
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
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 sm:py-8">
            <DashboardHeader user={dashboardData.user_info} />
            <StatisticsOverview stats={dashboardData.stats} />
            <SearchAndFilter
                searchTerm={searchTerm}
                setSearchTerm={setSearchTerm}
                filterType={filterType}
                setFilterType={setFilterType}
            />
            <RepairsList
                repairs={filteredRepairs}
                expandedCards={expandedCards}
                toggleCard={toggleCard}
                onStuckReport={fetchDashboardData}
            />
        </div>
    );
};

// Dashboard Header Component
const DashboardHeader = ({ user }) => {
    return (
        <div className="text-center mb-8">
            <div className="flex flex-col items-center space-y-4">
                <div className="w-16 h-16 sm:w-20 sm:h-20 bg-gradient-to-br from-orange-500 to-red-500 rounded-2xl flex items-center justify-center shadow-xl">
                    <i className="fas fa-tools text-white text-2xl sm:text-3xl"></i>
                </div>
                <h1 className="text-3xl sm:text-4xl lg:text-5xl font-bold bg-gradient-to-r from-orange-400 via-red-500 to-purple-500 bg-clip-text text-transparent mb-2">
                    🔧 דשבורד מכונאי
                </h1>
                <h2 className="text-xl sm:text-2xl text-orange-300 font-semibold">
                    שלום {user.first_name || user.username || 'מכונאי'}!
                </h2>
                <p className="text-slate-300 text-sm sm:text-base max-w-2xl">
                    כאן תוכל לנהל ולעדכן את התיקונים שהוקצו לך בצורה יעילה ומקצועית
                </p>
            </div>
        </div>
    );
};

// Statistics Overview Component
const StatisticsOverview = ({ stats }) => {
    const metrics = [
        {
            title: "תיקונים מוקצים",
            value: stats.total_assigned,
            icon: "fas fa-clipboard-list",
            color: "orange",
            gradient: "from-orange-500/20 to-orange-600/20",
            borderColor: "border-orange-400/30",
            textColor: "text-orange-300",
            iconBg: "bg-orange-500/20",
            iconColor: "text-orange-400"
        },
        {
            title: "הושלמו",
            value: stats.completed,
            icon: "fas fa-check-circle",
            color: "green",
            gradient: "from-green-500/20 to-emerald-600/20",
            borderColor: "border-green-400/30",
            textColor: "text-green-300",
            iconBg: "bg-green-500/20",
            iconColor: "text-green-400"
        },
        {
            title: "בעבודה",
            value: stats.in_progress,
            icon: "fas fa-cogs",
            color: "blue",
            gradient: "from-blue-500/20 to-cyan-600/20",
            borderColor: "border-blue-400/30",
            textColor: "text-blue-300",
            iconBg: "bg-blue-500/20",
            iconColor: "text-blue-400"
        },
        {
            title: "תקועים",
            value: stats.stuck,
            icon: "fas fa-exclamation-triangle",
            color: "red",
            gradient: "from-red-500/20 to-red-600/20",
            borderColor: "border-red-400/30",
            textColor: "text-red-300",
            iconBg: "bg-red-500/20",
            iconColor: "text-red-400"
        }
    ];

    return (
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
            {metrics.map((metric, index) => (
                <div
                    key={index}
                    className={`bg-slate-800/40 backdrop-blur-sm ${metric.borderColor} border rounded-xl p-4 text-center hover:scale-105 transform transition-all duration-300 hover:bg-slate-800/60 ${metric.gradient}`}
                >
                    <div className={`w-10 h-10 ${metric.iconBg} rounded-lg flex items-center justify-center mx-auto mb-3`}>
                        <i className={metric.icon + ' ' + metric.iconColor + ' text-lg'}></i>
                    </div>
                    <div className={`text-2xl font-bold ${metric.textColor} mb-1`}>
                        {metric.value}
                    </div>
                    <div className="text-xs text-slate-400">{metric.title}</div>
                </div>
            ))}
        </div>
    );
};

// Search and Filter Component
const SearchAndFilter = ({ searchTerm, setSearchTerm, filterType, setFilterType }) => {
    const filters = [
        { key: 'all', label: 'הכל', active: true },
        { key: 'pending', label: 'בעבודה', active: false },
        { key: 'completed', label: 'הושלם', active: false },
        { key: 'stuck', label: 'תקוע', active: false }
    ];

    return (
        <div className="mb-6">
            <div className="bg-slate-800/40 backdrop-blur-sm border border-slate-600/40 rounded-xl p-4">
                <div className="flex flex-col sm:flex-row gap-4">
                    <div className="flex-1">
                        <div className="relative">
                            <input
                                type="text"
                                placeholder="חפש לפי לקוח, דגם או מספר תיקון..."
                                className="w-full bg-slate-700/50 border border-slate-600/50 rounded-lg px-4 py-3 pl-12 text-white placeholder-slate-400 focus:border-orange-400 focus:ring-2 focus:ring-orange-400/20 transition-all"
                                value={searchTerm}
                                onChange={(e) => setSearchTerm(e.target.value)}
                            />
                            <i className="fas fa-search absolute left-4 top-1/2 transform -translate-y-1/2 text-slate-400"></i>
                        </div>
                    </div>
                    <div className="flex gap-2">
                        {filters.map(filter => (
                            <button
                                key={filter.key}
                                className={`px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200 ${
                                    filterType === filter.key
                                        ? 'bg-orange-500/30 border border-orange-400/50 text-orange-200'
                                        : 'bg-slate-600/50 border border-slate-500/30 text-slate-300 hover:bg-slate-600/70'
                                }`}
                                onClick={() => setFilterType(filter.key)}
                            >
                                {filter.label}
                            </button>
                        ))}
                    </div>
                </div>
            </div>
        </div>
    );
};

// Repairs List Component
const RepairsList = ({ repairs, expandedCards, toggleCard, onStuckReport }) => {
    if (repairs.length === 0) {
        return <EmptyState />;
    }

    return (
        <div className="space-y-4" id="repairs-container">
            {repairs.map((repair, index) => (
                <RepairCard
                    key={repair.id}
                    repair={repair}
                    index={index}
                    isExpanded={expandedCards[repair.id]}
                    onToggle={() => toggleCard(repair.id)}
                    onStuckReport={onStuckReport}
                />
            ))}
        </div>
    );
};

// Individual Repair Card Component
const RepairCard = ({ repair, index, isExpanded, onToggle, onStuckReport }) => {
    const getStatusInfo = () => {
        if (repair.is_stuck) {
            return {
                badge: { text: 'תקוע', color: 'bg-red-500/20 border-red-400/30 text-red-300', icon: 'fas fa-exclamation-triangle' },
                status: 'stuck'
            };
        } else if (repair.progress_percentage === 100) {
            return {
                badge: { text: 'הושלם', color: 'bg-green-500/20 border-green-400/30 text-green-300', icon: 'fas fa-check-circle' },
                status: 'completed'
            };
        } else {
            return {
                badge: { text: 'בעבודה', color: 'bg-blue-500/20 border-blue-400/30 text-blue-300', icon: 'fas fa-cogs' },
                status: 'pending'
            };
        }
    };

    const statusInfo = getStatusInfo();

    const animationStyle = { animationDelay: (index * 0.1) + 's' };
    const progressBarStyle = { width: repair.progress_percentage + '%' };

    return (
        <div
            className="bg-slate-800/50 backdrop-blur-sm border border-slate-600/40 rounded-2xl shadow-xl hover:shadow-2xl transition-all duration-300 hover:border-slate-500/60 animate-fade-in-up"
            style={animationStyle}
        >
            {/* Compact Header (Always Visible) */}
            <div className="p-6 cursor-pointer select-none" onClick={onToggle}>
                <div className="flex items-center justify-between">
                    <div className="flex items-center gap-4 flex-1">
                        <div className="flex-shrink-0 w-12 h-12 bg-gradient-to-br from-orange-500 to-red-500 rounded-xl flex items-center justify-center shadow-lg">
                            <i className="fas fa-bicycle text-white text-lg"></i>
                        </div>
                        <div className="flex-1 min-w-0">
                            <div className="flex items-center gap-3 mb-2">
                                <h3 className="text-lg font-bold text-white truncate">
                                    {repair.bike?.brand} {repair.bike?.model}
                                </h3>
                                <span className="text-sm text-slate-400 flex-shrink-0">#{repair.id}</span>
                            </div>
                            <div className="flex items-center gap-4 flex-wrap">
                                <p className="text-base text-slate-300 truncate">
                                    <i className="fas fa-user text-slate-400 mr-2"></i>
                                    {repair.bike?.customer?.name}
                                </p>
                                <div className="flex items-center gap-3">
                                    <span className={`px-3 py-1 border rounded-lg text-sm font-medium ${statusInfo.badge.color}`}>
                                        <i className={statusInfo.badge.icon + ' mr-1'}></i>
                                        {statusInfo.badge.text}
                                    </span>
                                    <span className="text-sm text-slate-400">
                                        {repair.progress_percentage}% הושלם
                                    </span>
                                </div>
                            </div>
                        </div>
                    </div>

                    {/* Right side actions and expand icon */}
                    <div className="flex items-center gap-4">
                        <div className="text-sm text-slate-400 text-right">
                            <div className="mb-1">
                                <i className="fas fa-tasks text-slate-500 mr-1"></i>
                                {repair.completed_count || 0}/{repair.total_items_count || 0} משימות
                            </div>
                            <div>
                                <i className="fas fa-calendar text-slate-500 mr-1"></i>
                                {new Date(repair.created_at).toLocaleDateString('he-IL')}
                            </div>
                        </div>

                        {/* Primary Action Button - Redesigned */}
                        <a
                            href={`/mechanic/repair/${repair.id}/complete/`}
                            className="bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700 text-white font-semibold px-4 py-3 rounded-xl transition-all duration-300 shadow-lg hover:shadow-xl transform hover:scale-105 active:scale-95 text-sm flex items-center gap-2"
                            onClick={(e) => e.stopPropagation()}
                        >
                            <i className="fas fa-edit"></i>
                            <span className="hidden sm:inline">עדכן</span>
                        </a>

                        <i className={`fas fa-chevron-down text-slate-400 transition-transform duration-300 ${isExpanded ? 'rotate-180' : ''}`}></i>
                    </div>
                </div>
            </div>

            {/* Expandable Content */}
            <div className={`overflow-hidden transition-all duration-500 ease-in-out ${isExpanded ? 'max-h-screen opacity-100' : 'max-h-0 opacity-0'}`}>
                <div className="border-t border-slate-600/30"></div>

                <RepairCardDetails repair={repair} onStuckReport={onStuckReport} progressBarStyle={progressBarStyle} />
            </div>
        </div>
    );
};

// Repair Card Details Component
const RepairCardDetails = ({ repair, onStuckReport, progressBarStyle }) => {
    const handleStuckReport = async (reason) => {
        try {
            const response = await fetch(`/api/mechanic/repair/${repair.id}/stuck/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]')?.value || ''
                },
                body: JSON.stringify({ reason })
            });

            if (response.ok) {
                onStuckReport(); // Refresh dashboard
            } else {
                alert('שגיאה בדיווח התקיעה');
            }
        } catch (error) {
            console.error('Error reporting stuck repair:', error);
            alert('שגיאה בדיווח התקיעה');
        }
    };

    return (
        <div className="p-6">
            <div className="grid grid-cols-1 xl:grid-cols-3 gap-6">

                {/* Customer & Repair Info */}
                <div className="xl:col-span-2 space-y-6">
                    {/* Customer Details */}
                    <div className="bg-slate-700/30 border border-slate-600/30 rounded-xl p-5">
                        <h4 className="text-white font-semibold mb-4 flex items-center gap-2 text-lg">
                            <i className="fas fa-user text-blue-400"></i>
                            פרטי לקוח ואופניים
                        </h4>
                        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                            <div className="space-y-3">
                                <div className="flex items-center gap-3 text-base">
                                    <i className="fas fa-user text-slate-400 w-4"></i>
                                    <span className="text-slate-200">{repair.bike?.customer?.name}</span>
                                </div>
                                <div className="flex items-center gap-3 text-base">
                                    <i className="fas fa-bicycle text-slate-400 w-4"></i>
                                    <span className="text-slate-200">{repair.bike?.brand} {repair.bike?.model}</span>
                                </div>
                            </div>
                            <div className="space-y-3">
                                <div className="flex items-center gap-3 text-base">
                                    <i className="fas fa-phone text-slate-400 w-4"></i>
                                    <span className="text-slate-200">{repair.bike?.customer?.phone || 'לא זמין'}</span>
                                </div>
                                <div className="flex items-center gap-3 text-base">
                                    <i className="fas fa-calendar text-slate-400 w-4"></i>
                                    <span className="text-slate-200">
                                        {new Date(repair.created_at).toLocaleDateString('he-IL', {
                                            year: 'numeric',
                                            month: 'long',
                                            day: 'numeric',
                                            hour: '2-digit',
                                            minute: '2-digit'
                                        })}
                                    </span>
                                </div>
                            </div>
                        </div>
                    </div>

                    {/* Diagnosis */}
                    {repair.diagnosis && (
                        <div className="bg-blue-500/10 border border-blue-400/30 rounded-xl p-5">
                            <h4 className="text-white font-semibold mb-3 flex items-center gap-2 text-lg">
                                <i className="fas fa-stethoscope text-blue-400"></i>
                                אבחון
                            </h4>
                            <p className="text-slate-200 text-base leading-relaxed">{repair.diagnosis}</p>
                        </div>
                    )}

                    {/* Approved Tasks */}
                    {repair.approved_items && repair.approved_items.length > 0 && (
                        <div className="bg-slate-700/30 border border-slate-600/30 rounded-xl p-5">
                            <h4 className="text-white font-semibold mb-4 flex items-center gap-2 text-lg">
                                <i className="fas fa-tasks text-green-400"></i>
                                פעולות מאושרות
                            </h4>
                            <div className="space-y-3">
                                {repair.approved_items.map((item, index) => (
                                    <div key={index} className="flex items-center justify-between p-4 bg-slate-800/50 rounded-lg border border-slate-600/20">
                                        <div className="flex-1">
                                            <div className="text-white text-base font-medium mb-1">{item.description}</div>
                                            {item.notes && (
                                                <div className="text-slate-400 text-sm">{item.notes}</div>
                                            )}
                                        </div>
                                        <div className="flex items-center gap-4">
                                            <span className="text-green-300 font-bold text-lg">₪{item.price}</span>
                                            {item.status === 'completed' ? (
                                                <span className="px-3 py-1 bg-green-500/20 border border-green-400/30 rounded-lg text-green-300 text-sm font-medium">
                                                    <i className="fas fa-check mr-1"></i>הושלם
                                                </span>
                                            ) : item.status === 'blocked' ? (
                                                <span className="px-3 py-1 bg-red-500/20 border border-red-400/30 rounded-lg text-red-300 text-sm font-medium">
                                                    <i className="fas fa-times mr-1"></i>תקוע
                                                </span>
                                            ) : (
                                                <span className="px-3 py-1 bg-blue-500/20 border border-blue-400/30 rounded-lg text-blue-300 text-sm font-medium">
                                                    <i className="fas fa-clock mr-1"></i>ממתין
                                                </span>
                                            )}
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>
                    )}
                </div>

                {/* Progress & Actions */}
                <div className="space-y-6">

                    {/* Progress Section */}
                    <div className="bg-slate-700/30 border border-slate-600/30 rounded-xl p-5">
                        <h4 className="text-white font-semibold mb-4 flex items-center gap-2 text-lg">
                            <i className="fas fa-chart-pie text-purple-400"></i>
                            התקדמות מפורטת
                        </h4>

                        {/* Progress Stats */}
                        <div className="grid grid-cols-2 gap-4 mb-6">
                            <div className="text-center">
                                <div className="text-3xl font-bold text-green-300">{repair.completed_count || 0}</div>
                                <div className="text-sm text-slate-400">הושלמו</div>
                            </div>
                            <div className="text-center">
                                <div className="text-3xl font-bold text-blue-300">{repair.pending_count || 0}</div>
                                <div className="text-sm text-slate-400">ממתינות</div>
                            </div>
                        </div>

                        {/* Progress Bar */}
                        <div className="relative mb-4">
                            <div className="w-full bg-slate-600 rounded-full h-8">
                                <div
                                    className="bg-gradient-to-r from-green-500 to-emerald-500 h-8 rounded-full flex items-center justify-center transition-all duration-1000 shadow-lg"
                                    style={progressBarStyle}
                                >
                                    <span className="text-white text-sm font-bold">
                                        {repair.progress_percentage}%
                                    </span>
                                </div>
                            </div>
                        </div>

                        {/* Stuck Alert */}
                        {repair.is_stuck && (
                            <div className="p-4 bg-red-500/10 border border-red-400/30 rounded-lg">
                                <div className="text-red-300 text-base font-semibold mb-2 flex items-center gap-2">
                                    <i className="fas fa-stop-circle"></i>
                                    תיקון תקוע
                                </div>
                                <p className="text-red-200 text-sm mb-3">{repair.stuck_reason}</p>
                                {repair.manager_response && (
                                    <div className="mt-3 p-3 bg-blue-500/10 border border-blue-400/30 rounded-lg">
                                        <div className="text-blue-300 text-sm font-semibold">תגובת מנהל:</div>
                                        <div className="text-blue-200 text-sm">{repair.manager_response}</div>
                                    </div>
                                )}
                            </div>
                        )}
                    </div>

                    {/* Action Buttons */}
                    <div className="space-y-3">
                        <a
                            href={`/mechanic/repair/${repair.id}/complete/`}
                            className="w-full bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700 text-white font-bold py-4 px-6 rounded-xl transition-all duration-300 shadow-lg hover:shadow-xl transform hover:scale-105 active:scale-95 text-base text-center block flex items-center justify-center gap-2"
                        >
                            <i className="fas fa-edit"></i>
                            עדכן התקדמות
                        </a>

                        <div className="grid grid-cols-2 gap-3">
                            <a
                                href={`/repair/${repair.id}/status/`}
                                className="bg-slate-600/50 hover:bg-slate-600/70 text-slate-200 font-medium py-3 px-4 rounded-lg transition-all text-sm text-center flex items-center justify-center gap-2"
                            >
                                <i className="fas fa-eye"></i>
                                פרטים
                            </a>
                            <a
                                href={`/repair/${repair.id}/print-label/`}
                                target="_blank"
                                className="bg-purple-600/50 hover:bg-purple-600/70 text-purple-200 font-medium py-3 px-4 rounded-lg transition-all text-sm text-center flex items-center justify-center gap-2"
                            >
                                <i className="fas fa-print"></i>
                                מדבקה
                            </a>
                        </div>

                        {!repair.is_stuck ? (
                            <StuckReportButton repairId={repair.id} onReport={handleStuckReport} />
                        ) : (
                            <button
                                className="w-full bg-green-600/50 hover:bg-green-600/70 text-green-200 font-medium py-3 px-4 rounded-lg transition-all text-sm flex items-center justify-center gap-2"
                                onClick={() => {
                                    if (confirm('האם אתה בטוח שברצונך להמשיך בעבודה?')) {
                                        // Handle resume work
                                        location.reload();
                                    }
                                }}
                            >
                                <i className="fas fa-play"></i>
                                המשך עבודה
                            </button>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
};

// Stuck Report Button Component
const StuckReportButton = ({ repairId, onReport }) => {
    const [showModal, setShowModal] = useState(false);
    const [reason, setReason] = useState('');
    const [loading, setLoading] = useState(false);

    const handleSubmit = async () => {
        if (!reason.trim()) {
            alert('נא לתאר את סיבת התקיעה');
            return;
        }

        setLoading(true);
        await onReport(reason.trim());
        setLoading(false);
        setShowModal(false);
        setReason('');
    };

    return (
        <>
            <button
                className="w-full bg-red-600/50 hover:bg-red-600/70 text-red-200 font-medium py-3 px-4 rounded-lg transition-all text-sm flex items-center justify-center gap-2"
                onClick={() => setShowModal(true)}
            >
                <i className="fas fa-exclamation-triangle"></i>
                דווח תקיעה
            </button>

            {showModal && (
                <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
                    <div className="bg-slate-800/90 backdrop-blur-xl border border-red-400/30 rounded-2xl p-6 w-full max-w-md">
                        <div className="flex items-center justify-between mb-4">
                            <h3 className="text-lg font-bold text-white flex items-center gap-2">
                                <i className="fas fa-exclamation-triangle text-red-400"></i>
                                דיווח על תקיעה
                            </h3>
                            <button
                                onClick={() => setShowModal(false)}
                                className="text-slate-400 hover:text-white transition-colors"
                            >
                                <i className="fas fa-times text-xl"></i>
                            </button>
                        </div>

                        <div className="mb-4">
                            <label className="block text-slate-300 text-sm font-medium mb-2">סיבת התקיעה:</label>
                            <textarea
                                rows="4"
                                className="w-full bg-slate-700/50 border border-slate-600/50 rounded-lg px-3 py-2 text-white placeholder-slate-400 focus:border-red-400 focus:ring-2 focus:ring-red-400/20 transition-all resize-none"
                                placeholder="תאר את הבעיה או מה שמונע ממך להמשיך..."
                                value={reason}
                                onChange={(e) => setReason(e.target.value)}
                            />
                        </div>

                        <div className="flex gap-3">
                            <button
                                onClick={() => setShowModal(false)}
                                className="flex-1 bg-slate-600/50 hover:bg-slate-600/70 text-slate-200 font-medium py-2 px-4 rounded-lg transition-all"
                            >
                                ביטול
                            </button>
                            <button
                                onClick={handleSubmit}
                                disabled={loading}
                                className="flex-1 bg-red-600 hover:bg-red-700 text-white font-medium py-2 px-4 rounded-lg transition-all disabled:opacity-50"
                            >
                                {loading ? (
                                    <>
                                        <i className="fas fa-spinner fa-spin mr-2"></i>
                                        שולח...
                                    </>
                                ) : (
                                    'דווח תקיעה'
                                )}
                            </button>
                        </div>
                    </div>
                </div>
            )}
        </>
    );
};

// Empty State Component
const EmptyState = () => {
    return (
        <div className="text-center py-16">
            <div className="bg-slate-800/40 backdrop-blur-sm border border-slate-600/40 rounded-2xl p-8 max-w-md mx-auto">
                <div className="w-20 h-20 bg-gradient-to-br from-orange-500 to-red-500 rounded-2xl flex items-center justify-center mx-auto mb-6 shadow-xl">
                    <i className="fas fa-tools text-white text-3xl"></i>
                </div>
                <h3 className="text-xl font-bold text-white mb-2">אין תיקונים מוקצים כרגע</h3>
                <p className="text-slate-400 mb-6">כאשר יוקצו לך תיקונים, הם יופיעו כאן</p>
                <a
                    href="/"
                    className="bg-gradient-to-r from-orange-500 to-red-500 hover:from-orange-600 hover:to-red-600 text-white font-semibold py-3 px-6 rounded-xl transition-all duration-300 shadow-lg hover:shadow-xl transform hover:scale-105 active:scale-95 inline-flex items-center gap-2"
                >
                    <i className="fas fa-home"></i>
                    חזור לדף הבית
                </a>
            </div>
        </div>
    );
};

export default MechanicDashboard;
