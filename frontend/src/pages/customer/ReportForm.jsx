import { useState, useEffect } from 'react';

const CustomerReportForm = () => {
    const [bikes, setBikes] = useState([]);
    const [categories, setCategories] = useState([]);
    const [selectedBike, setSelectedBike] = useState('');
    const [selectedSubcategories, setSelectedSubcategories] = useState([]);
    const [customRepair, setCustomRepair] = useState(false);
    const [description, setDescription] = useState('');
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [submitting, setSubmitting] = useState(false);
    const [expandedCategories, setExpandedCategories] = useState([]);

    useEffect(() => {
        fetchData();
    }, []);

    const fetchData = async () => {
        try {
            const [bikesRes, categoriesRes] = await Promise.all([
                fetch('/api/customer/bikes/', { credentials: 'same-origin' }),
                fetch('/api/categories/', { credentials: 'same-origin' })
            ]);

            if (!bikesRes.ok || !categoriesRes.ok) {
                throw new Error('Failed to fetch data');
            }

            const bikesData = await bikesRes.json();
            const categoriesData = await categoriesRes.json();

            setBikes(bikesData);
            setCategories(categoriesData);

            // Auto-select if only one bike
            if (bikesData.length === 1) {
                setSelectedBike(bikesData[0].id.toString());
            }

            setLoading(false);
        } catch (err) {
            setError(err.message);
            setLoading(false);
        }
    };

    const toggleCategory = (categoryId) => {
        setExpandedCategories(prev =>
            prev.includes(categoryId)
                ? prev.filter(id => id !== categoryId)
                : [...prev, categoryId]
        );
    };

    const handleSubcategoryToggle = (subcategoryId) => {
        setSelectedSubcategories(prev =>
            prev.includes(subcategoryId)
                ? prev.filter(id => id !== subcategoryId)
                : [...prev, subcategoryId]
        );
    };

    const isFormValid = () => {
        return selectedBike && (selectedSubcategories.length > 0 || customRepair);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        if (!isFormValid()) return;

        setSubmitting(true);

        try {
            const response = await fetch('/api/customer/report/', {
                method: 'POST',
                credentials: 'same-origin',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]')?.value || ''
                },
                body: JSON.stringify({
                    bike: selectedBike,
                    subcategories: selectedSubcategories,
                    problem_description: description
                })
            });

            if (!response.ok) {
                throw new Error('Failed to submit report');
            }

            // Redirect to success page
            window.location.href = '/customer/report/done/';
        } catch (err) {
            alert('שגיאה בשליחת הדיווח: ' + err.message);
            setSubmitting(false);
        }
    };

    if (loading) {
        return (
            <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 flex items-center justify-center">
                <div className="text-center">
                    <div className="w-16 h-16 border-4 border-blue-400 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
                    <p className="text-slate-300 text-lg">טוען...</p>
                </div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 flex items-center justify-center">
                <div className="bg-red-900/20 border border-red-500/30 rounded-2xl p-8 max-w-md mx-auto">
                    <i className="fas fa-exclamation-triangle text-red-400 text-4xl mb-4"></i>
                    <h2 className="text-xl font-bold text-white mb-2">שגיאה בטעינת הנתונים</h2>
                    <p className="text-red-200">{error}</p>
                </div>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 py-8 px-4">
            <div className="max-w-4xl mx-auto">
                {/* Header */}
                <div className="text-center mb-8">
                    <h1 className="text-3xl md:text-4xl font-bold text-white mb-4">🔧 דיווח תקלה חדשה</h1>
                    <p className="text-slate-300 text-lg">תאר את התקלה בפירוט ונטפל בה בהקדם</p>
                </div>

                {/* Form */}
                <div className="bg-slate-800/80 border border-slate-600 rounded-2xl p-6 mb-6">
                    <form onSubmit={handleSubmit}>
                        {/* Bike Selection */}
                        <div className="mb-6">
                            <label className="block text-white font-bold mb-3 text-lg">בחר אופניים:</label>
                            <select
                                value={selectedBike}
                                onChange={(e) => setSelectedBike(e.target.value)}
                                className="w-full bg-slate-700 border border-slate-600 text-white rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                            >
                                <option value="">בחר אופניים</option>
                                {bikes.map(bike => (
                                    <option key={bike.id} value={bike.id}>
                                        {bike.brand} {bike.model}
                                    </option>
                                ))}
                            </select>
                        </div>

                        {/* Categories Accordion */}
                        <div className="mb-6">
                            <label className="block text-white font-bold mb-4 text-lg">בחר סוגי התקלות:</label>
                            <div className="space-y-3">
                                {categories.map(category => (
                                    <div key={category.id} className="bg-slate-700/50 border border-slate-600 rounded-xl overflow-hidden">
                                        {/* Category Header */}
                                        <div
                                            onClick={() => toggleCategory(category.id)}
                                            className="bg-gradient-to-r from-blue-600/30 to-blue-500/30 px-4 py-3 cursor-pointer flex items-center justify-between hover:from-blue-600/40 hover:to-blue-500/40 transition-all duration-300"
                                        >
                                            <h3 className="text-blue-300 font-bold text-lg flex items-center gap-2">
                                                <i className="fas fa-tools text-blue-400"></i>
                                                {category.name}
                                            </h3>
                                            <i className={`fas fa-chevron-down transition-transform duration-300 text-blue-300 ${expandedCategories.includes(category.id) ? 'rotate-180' : ''}`}></i>
                                        </div>

                                        {/* Category Content */}
                                        {expandedCategories.includes(category.id) && (
                                            <div className="bg-slate-800/30 p-4">
                                                <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                                                    {category.subcategories.map(sub => (
                                                        <label key={sub.id} className="flex items-center gap-3 p-3 bg-slate-700/30 rounded-lg hover:bg-slate-600/40 transition-colors cursor-pointer">
                                                            <input
                                                                type="checkbox"
                                                                checked={selectedSubcategories.includes(sub.id)}
                                                                onChange={() => handleSubcategoryToggle(sub.id)}
                                                                className="w-4 h-4 text-blue-600 bg-slate-700 border-slate-500 rounded focus:ring-blue-500"
                                                            />
                                                            <span className="text-white text-sm">{sub.name}</span>
                                                        </label>
                                                    ))}
                                                </div>
                                            </div>
                                        )}
                                    </div>
                                ))}
                            </div>
                        </div>

                        {/* Custom Repair Checkbox */}
                        <div className="bg-amber-500/20 border border-amber-400/40 rounded-xl p-4 mb-6">
                            <label className="flex items-center gap-3 cursor-pointer text-white">
                                <input
                                    type="checkbox"
                                    checked={customRepair}
                                    onChange={(e) => setCustomRepair(e.target.checked)}
                                    className="w-5 h-5 text-amber-500 bg-slate-700 border-slate-500 rounded focus:ring-amber-500"
                                />
                                <span className="font-semibold">לא מצאתי את התקלה שלי ברשימה</span>
                            </label>
                            <p className="text-slate-300 text-sm mt-2 mr-8">
                                בחר באפשרות זו אם התקלה שלך לא מופיעה ברשימת הקטגוריות
                            </p>
                        </div>

                        {/* Description */}
                        <div className="mb-6">
                            <label className="block text-white font-bold mb-3 text-lg">תיאור התקלה:</label>
                            <textarea
                                value={description}
                                onChange={(e) => setDescription(e.target.value)}
                                className="w-full bg-slate-700 border border-slate-600 text-white rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent min-h-[120px] resize-vertical"
                                placeholder="תאר את התקלה בפירוט..."
                            />
                        </div>

                        {/* Submit Button */}
                        <div className="text-center">
                            <button
                                type="submit"
                                disabled={!isFormValid() || submitting}
                                className={`px-8 py-4 text-lg font-bold rounded-xl transition-all duration-300 shadow-lg ${
                                    isFormValid() && !submitting
                                        ? 'bg-gradient-to-r from-green-500 to-green-600 text-white hover:from-green-600 hover:to-green-700 transform hover:scale-105 cursor-pointer'
                                        : 'bg-gradient-to-r from-slate-500 to-slate-600 text-slate-300 cursor-not-allowed'
                                }`}
                            >
                                {submitting ? (
                                    <>
                                        <i className="fas fa-spinner fa-spin mr-2"></i>
                                        שולח...
                                    </>
                                ) : (
                                    'שלח דיווח תקלה'
                                )}
                            </button>

                            {!isFormValid() && (
                                <div className="bg-blue-500/10 border border-blue-400/30 rounded-xl p-4 mt-4 text-blue-200">
                                    <div className="font-semibold mb-2">כדי לשלוח דיווח:</div>
                                    <div className="text-sm space-y-1">
                                        <div>• בחר אופניים מהרשימה</div>
                                        <div>• בחר קטגוריות תקלה או סמן "לא מצאתי את התקלה שלי"</div>
                                    </div>
                                </div>
                            )}
                        </div>
                    </form>
                </div>
            </div>
        </div>
    );
};

export default CustomerReportForm;

// Initialize and render
import { createRoot } from 'react-dom/client';

const rootElement = document.getElementById('root');
if (rootElement) {
    const root = createRoot(rootElement);
    root.render(<CustomerReportForm />);
}
