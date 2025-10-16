# 📐 Frontend Migration Rules & Standards

**Version:** 1.1
**Last Updated:** 2025-10-16
**Status:** Active

---

## 🎯 Core Principles

1. **Consistency Over Cleverness** - Write boring, predictable code
2. **One Way to Do Things** - No multiple patterns for same task
3. **Progressive Enhancement** - Start simple, add complexity only when needed
4. **Mobile First** - Design for mobile, enhance for desktop
5. **Accessibility** - WCAG 2.1 AA compliance minimum
6. **🗑️ Clean as You Go** - Delete every file immediately after it becomes unused and redundant

---

## 🎨 Styling Rules

### ✅ DO

```jsx
// Use Tailwind utility classes
<button className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-lg transition">
  Click Me
</button>

// Extract repeated patterns to components
function PrimaryButton({ children, ...props }) {
  return (
    <button
      className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-lg transition"
      {...props}
    >
      {children}
    </button>
  );
}

// Use design tokens for consistency
<div className="bg-brand-primary text-slate-100">
```

### ❌ DON'T

```jsx
// NO inline style objects
<div style={{ backgroundColor: '#1e293b', padding: '1.5rem' }}>

// NO inline <style> tags
<style>{`.custom { background: blue; }`}</style>

// NO components.css classes
<div className="btn-modern primary">

// NO magic numbers
<div className="w-[234px] h-[567px]">  // Use semantic values

// NO !important
className="bg-blue-500 !text-white"  // Fix specificity instead
```

---

## 🎨 Color Palette

Use these standardized colors only:

```javascript
// Tailwind config (already set up)
colors: {
  brand: {
    primary: '#3b82f6',    // Blue
    success: '#10b981',    // Green
    warning: '#f59e0b',    // Orange
    danger: '#ef4444',     // Red
  },
  slate: {
    // Use slate scale for dark theme
    50: '#f8fafc',
    // ...
    900: '#0f172a',
  }
}
```

**Usage:**
```jsx
// ✅ Good
<div className="bg-brand-primary">
<div className="bg-slate-800">

// ❌ Bad
<div className="bg-blue-500">      // Use brand-primary
<div className="bg-[#1e293b]">     // Use slate-700
```

---

## ⚛️ Component Rules

### File Structure

```
frontend/src/
├── pages/              # One page per route
├── components/         # Shared components
│   ├── ui/            # Generic UI (Button, Input, etc.)
│   └── domain/        # Business logic (RepairCard, etc.)
├── hooks/             # Custom React hooks
├── api/               # API client and endpoints
├── utils/             # Pure functions
└── styles/            # Global styles (minimal)
```

### Naming Conventions

```
✅ PascalCase for components:     Button.jsx, RepairCard.jsx
✅ camelCase for files:            useRepairs.js, formatDate.js
✅ kebab-case for CSS/folders:     repair-card.css, customer-dashboard/
```

### Component Template

```jsx
import { useState } from 'react';
import { useRepairs } from '../hooks/useRepairs';
import { Button, Card } from '../components/ui';

/**
 * RepairList - Displays list of repairs
 *
 * @param {Object} props
 * @param {string} props.status - Filter repairs by status
 * @param {Function} props.onSelect - Called when repair is selected
 */
export default function RepairList({ status, onSelect }) {
  // 1. Hooks first
  const { data: repairs, isLoading, error } = useRepairs({ status });
  const [selectedId, setSelectedId] = useState(null);

  // 2. Event handlers
  const handleSelect = (id) => {
    setSelectedId(id);
    onSelect?.(id);
  };

  // 3. Early returns
  if (isLoading) return <LoadingSpinner />;
  if (error) return <ErrorMessage error={error} />;
  if (!repairs?.length) return <EmptyState />;

  // 4. Main render
  return (
    <div className="space-y-4">
      <h2 className="text-2xl font-bold text-slate-100">Repairs</h2>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {repairs.map(repair => (
          <RepairCard
            key={repair.id}
            repair={repair}
            isSelected={selectedId === repair.id}
            onClick={() => handleSelect(repair.id)}
          />
        ))}
      </div>
    </div>
  );
}
```

### Component Rules

```jsx
// ✅ DO - Functional components with hooks
export default function MyComponent() { }

// ❌ DON'T - Class components
export default class MyComponent extends React.Component { }

// ✅ DO - Destructure props
export default function Button({ variant, children }) { }

// ❌ DON'T - Use props object
export default function Button(props) { return <button>{props.children}</button> }

// ✅ DO - Default exports for pages/main components
export default function CustomerDashboard() { }

// ✅ DO - Named exports for utilities
export function formatDate() { }
export function Button() { }
```

---

## 🔌 API & Data Fetching

### API Client Structure

```javascript
// api/client.js - Base client
import axios from 'axios';

const client = axios.create({
  baseURL: '/api',
  timeout: 10000,
});

// Add CSRF token to all requests
client.interceptors.request.use(config => {
  const token = document.querySelector('[name=csrfmiddlewaretoken]')?.value;
  if (token) config.headers['X-CSRFToken'] = token;
  return config;
});

// Add error handling
client.interceptors.response.use(
  response => response.data,
  error => {
    console.error('API Error:', error);
    return Promise.reject(error);
  }
);

export default client;
```

```javascript
// api/repairs.js - Resource endpoints
import client from './client';

export const repairsAPI = {
  getAll: (params) => client.get('/repairs/', { params }),
  getById: (id) => client.get(`/repairs/${id}/`),
  create: (data) => client.post('/repairs/', data),
  update: (id, data) => client.patch(`/repairs/${id}/`, data),
  delete: (id) => client.delete(`/repairs/${id}/`),
};
```

### React Query Hooks

```javascript
// hooks/useRepairs.js
import { useQuery, useMutation, useQueryClient } from 'react-query';
import { repairsAPI } from '../api/repairs';

// GET list
export function useRepairs(params = {}) {
  return useQuery(
    ['repairs', params],
    () => repairsAPI.getAll(params),
    {
      staleTime: 30000, // 30 seconds
      refetchOnWindowFocus: true,
    }
  );
}

// GET single
export function useRepair(id) {
  return useQuery(
    ['repairs', id],
    () => repairsAPI.getById(id),
    {
      enabled: !!id, // Only fetch if id exists
    }
  );
}

// POST/PATCH/DELETE
export function useCreateRepair() {
  const queryClient = useQueryClient();

  return useMutation(repairsAPI.create, {
    onSuccess: () => {
      // Invalidate and refetch
      queryClient.invalidateQueries('repairs');
    },
    onError: (error) => {
      console.error('Failed to create repair:', error);
    },
  });
}
```

### Usage in Components

```jsx
function RepairList() {
  // ✅ Good - declarative data fetching
  const { data, isLoading, error } = useRepairs({ status: 'active' });
  const createRepair = useCreateRepair();

  const handleCreate = (formData) => {
    createRepair.mutate(formData, {
      onSuccess: (newRepair) => {
        console.log('Created:', newRepair);
      }
    });
  };

  if (isLoading) return <LoadingSpinner />;
  if (error) return <ErrorMessage error={error} />;

  return <div>{/* render data */}</div>;
}
```

### Rules

```jsx
// ✅ DO - Use React Query for server state
const { data } = useRepairs();

// ❌ DON'T - Manual fetch in useEffect
useEffect(() => {
  fetch('/api/repairs/').then(r => r.json()).then(setData);
}, []);

// ✅ DO - Handle all states (loading, error, success)
if (isLoading) return <LoadingSpinner />;
if (error) return <ErrorMessage />;
return <div>{data}</div>;

// ❌ DON'T - Assume data exists
return <div>{data.map(...)}</div>; // Crashes if data is undefined
```

---

## 📦 State Management

### When to Use What

```
Local Component State (useState)
  ↓ Simple, component-scoped

React Query (server state)
  ↓ Data from API

Zustand (global client state)
  ↓ Cross-component state (auth, theme, etc.)

URL State (useSearchParams)
  ↓ Shareable state (filters, pagination)
```

### Local State (useState)

```jsx
// ✅ For UI state within a component
function Modal() {
  const [isOpen, setIsOpen] = useState(false);
  // ...
}
```

### Global State (Zustand)

```javascript
// store/authStore.js
import create from 'zustand';

export const useAuthStore = create((set) => ({
  user: null,
  isAuthenticated: false,

  login: (user) => set({ user, isAuthenticated: true }),
  logout: () => set({ user: null, isAuthenticated: false }),
}));
```

```jsx
// Usage
function Header() {
  const { user, logout } = useAuthStore();

  return (
    <header>
      <span>{user?.name}</span>
      <button onClick={logout}>Logout</button>
    </header>
  );
}
```

### Rules

```jsx
// ✅ DO - Minimal global state
const authStore = { user, login, logout };

// ❌ DON'T - Everything in global state
const globalStore = { user, repairs, customers, bikes, ... }; // Use React Query instead

// ✅ DO - Colocate state with component
function RepairForm() {
  const [formData, setFormData] = useState({});
  // ...
}

// ❌ DON'T - Lift state unnecessarily
// If only one component needs it, keep it local
```

---

## 🧪 Testing Standards

### What to Test

```
✅ User interactions (clicks, form submissions)
✅ Conditional rendering (loading, error states)
✅ Data transformations (utils, formatters)
✅ Critical user flows (create repair, approve repair)

❌ Implementation details (state variable names)
❌ Third-party libraries (React Query, etc.)
❌ Styling/CSS (use visual regression instead)
```

### Test Template

```javascript
// __tests__/RepairForm.test.jsx
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from 'react-query';
import RepairForm from '../pages/RepairForm';

// Setup wrapper with providers
const createWrapper = () => {
  const queryClient = new QueryClient({
    defaultOptions: { queries: { retry: false } }
  });

  return ({ children }) => (
    <QueryClientProvider client={queryClient}>
      {children}
    </QueryClientProvider>
  );
};

describe('RepairForm', () => {
  it('submits form with valid data', async () => {
    render(<RepairForm />, { wrapper: createWrapper() });

    // Fill form
    fireEvent.change(screen.getByLabelText('Description'), {
      target: { value: 'Broken chain' }
    });

    // Submit
    fireEvent.click(screen.getByText('Save Repair'));

    // Assert success
    await waitFor(() => {
      expect(screen.getByText('Repair created successfully')).toBeInTheDocument();
    });
  });

  it('shows error for invalid data', async () => {
    render(<RepairForm />, { wrapper: createWrapper() });

    // Submit empty form
    fireEvent.click(screen.getByText('Save Repair'));

    // Assert error
    await waitFor(() => {
      expect(screen.getByText('Description is required')).toBeInTheDocument();
    });
  });
});
```

---

## 🚀 Performance Rules

### Code Splitting

```jsx
// ✅ DO - Lazy load pages
import { lazy, Suspense } from 'react';

const CustomerDashboard = lazy(() => import('./pages/CustomerDashboard'));

function App() {
  return (
    <Suspense fallback={<LoadingSpinner />}>
      <CustomerDashboard />
    </Suspense>
  );
}

// ❌ DON'T - Import everything upfront
import CustomerDashboard from './pages/CustomerDashboard';
import ManagerDashboard from './pages/ManagerDashboard';
// etc...
```

### Memoization

```jsx
// ✅ DO - Memoize expensive calculations
const expensiveValue = useMemo(() => {
  return repairs.filter(r => r.status === 'active').length;
}, [repairs]);

// ✅ DO - Memoize callbacks passed to children
const handleSelect = useCallback((id) => {
  setSelectedId(id);
}, []);

// ❌ DON'T - Premature optimization
const count = useMemo(() => repairs.length, [repairs]); // Not expensive, don't memo
```

### List Rendering

```jsx
// ✅ DO - Use stable keys
{repairs.map(repair => (
  <RepairCard key={repair.id} repair={repair} />
))}

// ❌ DON'T - Use index as key
{repairs.map((repair, index) => (
  <RepairCard key={index} repair={repair} />
))}
```

---

## 📱 Responsive Design

### Breakpoints (Tailwind defaults)

```
sm:  640px   (tablets)
md:  768px   (tablets landscape)
lg:  1024px  (laptops)
xl:  1280px  (desktops)
2xl: 1536px  (large desktops)
```

### Mobile-First Pattern

```jsx
// ✅ DO - Start mobile, enhance for desktop
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
  {/* 1 column mobile, 2 tablet, 3 desktop */}
</div>

<button className="w-full md:w-auto">
  {/* Full width on mobile, auto on desktop */}
</button>

// ❌ DON'T - Desktop-first
<div className="grid-cols-3 sm:grid-cols-1">
```

---

## ♿ Accessibility Rules

```jsx
// ✅ DO - Semantic HTML
<button onClick={handleClick}>Click</button>

// ❌ DON'T - Div soup
<div onClick={handleClick}>Click</div>

// ✅ DO - ARIA labels
<button aria-label="Close modal" onClick={onClose}>
  <XIcon />
</button>

// ✅ DO - Keyboard navigation
<div role="button" tabIndex={0} onKeyDown={handleKeyDown} onClick={handleClick}>

// ✅ DO - Focus management
<input ref={inputRef} />
useEffect(() => inputRef.current?.focus(), []);

// ✅ DO - Form labels
<label htmlFor="email">Email</label>
<input id="email" type="email" />
```

---

## 🔒 Security Rules

```jsx
// ✅ DO - Always include CSRF token
const client = axios.create({
  headers: {
    'X-CSRFToken': getCsrfToken(),
  }
});

// ❌ DON'T - Store sensitive data in localStorage
localStorage.setItem('password', password); // Never do this

// ✅ DO - Sanitize user input (if displaying HTML)
import DOMPurify from 'dompurify';
const clean = DOMPurify.sanitize(userInput);

// ✅ DO - Validate on backend too
// Never trust client-side validation alone
```

---

## 📝 Code Quality

### ESLint Rules (to be configured)

```javascript
// .eslintrc.js
module.exports = {
  extends: ['react-app', 'react-app/jest'],
  rules: {
    'no-console': ['warn', { allow: ['warn', 'error'] }],
    'no-unused-vars': 'warn',
    'react/prop-types': 'off', // If using TypeScript
    'react-hooks/rules-of-hooks': 'error',
    'react-hooks/exhaustive-deps': 'warn',
  }
};
```

### Prettier Config

```json
// .prettierrc
{
  "semi": true,
  "trailingComma": "es5",
  "singleQuote": true,
  "printWidth": 100,
  "tabWidth": 2
}
```

---

## 🔄 Git Workflow

### Commit Messages

```
✅ Good:
feat: Add customer approval page
fix: Repair form validation error
refactor: Extract Button component
perf: Lazy load manager dashboard

❌ Bad:
update stuff
fixed bug
changes
WIP
```

### Branch Strategy

```
main              (production, always deployable)
  └─ feat/customer-approval
  └─ fix/repair-form-bug
  └─ refactor/styling-cleanup
```

---

## 🎓 Learning Resources

- [React Docs](https://react.dev)
- [Tailwind Docs](https://tailwindcss.com/docs)
- [React Query Docs](https://tanstack.com/query/latest)
- [Zustand Docs](https://github.com/pmndrs/zustand)

---

## 🗑️ File Cleanup Rules

### When to Delete Files

**Delete immediately when:**
- ✅ File replaced by new React version (e.g., `manager_dashboard_react.html` → `ManagerDashboard.jsx`)
- ✅ Old CSS file superseded (e.g., `components.css` after migrating to Tailwind components)
- ✅ Legacy JavaScript replaced (e.g., jQuery code → React hooks)
- ✅ Unused imports or dead code detected
- ✅ Template no longer referenced in URLs

### Migration File Deletion Process

```bash
# 1. After migrating a template, verify it works
# 2. Remove old template file
git rm workshop/templates/workshop/old_template.html

# 3. Remove associated static files if any
git rm workshop/static/js/old-script.js

# 4. Commit with clear message
git commit -m "refactor: Remove old_template.html (replaced by React component)"
```

### Examples

```bash
# ✅ Good - Clean deletion after migration
- Migrated manager_dashboard_react.html → ManagerDashboard.jsx
- Tested new component works
- git rm workshop/templates/workshop/manager_dashboard_react.html
- git commit -m "refactor: Remove manager_dashboard_react.html (replaced by Vite build)"

# ❌ Bad - Keeping "just in case"
- Migrated but kept old file
- Result: 2 files doing same thing = confusion
```

### Exceptions

**Keep temporarily (but document):**
```python
# views.py - during testing period
def dashboard(request):
    # TODO: Remove legacy template after 1 week (2025-10-23)
    if request.GET.get('legacy'):
        return render(request, 'workshop/legacy/dashboard.html')
    return render(request, 'workshop/dashboard.html')  # New React version
```

After testing period expires: **DELETE** the legacy template.

### No "Backup" Folders

```
❌ DON'T create backup folders:
templates/
  workshop/
    old/
    backup/
    legacy/
    archive/

✅ DO use git history for backups:
git log --all --full-history -- path/to/deleted/file.html
git show commit_hash:path/to/file.html
```

**Git is your backup.** Don't clutter the codebase.

---

## ✅ Pre-Commit Checklist

Before committing code, verify:

- [ ] No console.errors or warnings
- [ ] All imports used
- [ ] Follows naming conventions
- [ ] No inline styles (except edge cases)
- [ ] Responsive on mobile
- [ ] Tested in browser
- [ ] Runs `npm run build` successfully
- [ ] **🗑️ Deleted all unused/replaced files**
- [ ] **🗑️ No commented-out code blocks**

---

## 🆘 Getting Help

If unsure about a pattern:
1. Check this document first
2. Look at existing migrated components
3. Ask for code review
4. When in doubt, keep it simple

---

**Remember:** These rules exist to make the codebase maintainable. If a rule doesn't make sense in a specific case, document why you're breaking it.

**Last Updated:** 2025-10-16
**Next Review:** After Phase 2 completion
