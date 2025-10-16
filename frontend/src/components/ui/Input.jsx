/**
 * Input Component
 *
 * Styled input field with label and error state
 *
 * @param {Object} props
 * @param {string} props.label - Input label
 * @param {string} props.error - Error message
 * @param {string} props.type - Input type (text, email, password, etc.)
 * @param {boolean} props.required - Required field indicator
 */
export default function Input({
  label,
  error,
  type = 'text',
  required = false,
  className = '',
  ...props
}) {
  const baseStyles = `
    w-full px-4 py-2
    bg-slate-700/50
    border border-slate-600
    rounded-lg
    text-slate-100
    placeholder-slate-400
    focus:outline-none
    focus:ring-2
    focus:ring-blue-500
    focus:border-transparent
    transition-all duration-200
  `;

  const errorStyles = error
    ? 'border-red-500 focus:ring-red-500'
    : '';

  return (
    <div className="space-y-1">
      {label && (
        <label className="block text-sm font-medium text-slate-200">
          {label}
          {required && <span className="text-red-400 ml-1">*</span>}
        </label>
      )}

      <input
        type={type}
        className={`${baseStyles} ${errorStyles} ${className}`}
        {...props}
      />

      {error && (
        <p className="text-sm text-red-400 mt-1">{error}</p>
      )}
    </div>
  );
}
