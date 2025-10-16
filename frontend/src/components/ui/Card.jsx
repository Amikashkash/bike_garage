/**
 * Card Component
 *
 * Glass-morphism card design following the app's aesthetic
 *
 * @param {Object} props
 * @param {React.ReactNode} props.children - Card content
 * @param {string} props.className - Additional CSS classes
 * @param {boolean} props.hoverable - Enable hover effect
 */
export default function Card({ children, className = '', hoverable = false }) {
  const hoverStyles = hoverable
    ? 'hover:border-slate-500/70 hover:shadow-lg cursor-pointer'
    : '';

  return (
    <div
      className={`
        bg-slate-800/60
        backdrop-blur-sm
        border border-slate-600/20
        rounded-xl
        overflow-hidden
        transition-all duration-300
        ${hoverStyles}
        ${className}
      `}
    >
      {children}
    </div>
  );
}
