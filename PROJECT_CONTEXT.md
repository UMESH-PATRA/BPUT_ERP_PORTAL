# BPUT Digital Campus Platform — Project Context

## 1. Executive Overview
The **BPUT Digital Campus Platform** is an institutional web application built for **Biju Patnaik University of Technology (BPUT), Odisha** (Rourkela campus). It provides a unified, paperless portal for university students, hostel residents, faculty advisors, wardens, and administrative authorities (Office of Dean & Proctorial Board).

---

## 2. Tech Stack

| Layer | Technologies & Libraries |
|---|---|
| **Frontend Framework** | Pure Vanilla JavaScript (ES6+), HTML5, CSS3 (No React / Vue / Angular build step) |
| **Typing & Types** | TypeScript definitions (`types/campus.d.ts`), `tsconfig.json` (ES2022) |
| **Styling & Design System** | Tailwind CSS (via CDN), Custom University Institutional Theme (`css/styles.css`), Impeccable Design Rails (`DESIGN.md`, `PRODUCT.md`) |
| **Typography** | Google Fonts (`Plus Jakarta Sans` for institutional dignity, `Inter` for interface readability) |
| **Icons** | Lucide Icons (`lucide@latest` CDN) |
| **Local State Management** | `CampusStore` (`js/store.js`) using browser `localStorage` with `CustomEvent` cross-component sync |
| **Authentication & SSO** | Dual Gateway: Institutional Pre-enrolled Credentials (`STD001`, `ADMIN001`) + Clerk Federated SSO (`js/clerk.js`) |
| **Performance & Web Vitals** | Core Web Vitals monitor (`js/vitals.js`: LCP, CLS, INP/FID, FCP, TTFB) |
| **Observability & Error Tracking** | Sentry Browser SDK integration (`js/sentry.js`) with breadcrumbs and exception logging |
| **Auditing & Budgets** | Lighthouse Audit Engine (`audits/lighthouse_audit.py`, 100% score) & BundlePhobia report (`audits/bundle_audit.py`, 116 KB) |
| **End-to-End Testing** | Microsoft Playwright E2E Test Suite (`tests/test_playwright_e2e.py`, `playwright.config.ts`, `tests/campus.spec.ts`) |
| **Cloud Database & Realtime** | Supabase (PostgreSQL) + Supabase JS Client (`@supabase/supabase-js` CDN) + WebSocket Realtime |
| **Local Server** | Python 3.14 UTF-8 Server (`server.py`) / Node static server (`server.js`) |
| **Deployment Target** | GitHub Pages / Any static hosting |

---

## 3. Folder & File Structure

```
c:\Users\HP\Desktop\palak_hackathon\
├── index.html            # Main University Landing Portal & Public Notices
├── student-auth.html     # Student Authentication Portal (Login + Password Recovery)
├── admin-auth.html       # Campus Administration Authentication Portal (Executive Gateway)
├── student.html          # Student Dashboard & Services Portal
├── admin.html            # Campus Administration & Dean/Proctorial Console
├── README.md             # Project overview & demo credentials documentation
├── server.js             # Lightweight Node.js static file server (port 5000/6000)
├── css/
│   └── styles.css        # University design system tokens, animations, responsive rules
└── js/
    ├── data.js           # Realistic seed dataset (students, notices, complaints, passes, etc.)
    ├── store.js          # CampusStore class: client-side CRUD, state, and localStorage bridge
    ├── auth.js           # AuthService: institutional role-based authentication & session control
    ├── theme.js          # CampusTheme: theme engine (Light/Dark mode), tokens, toggle widget & persistence
    ├── i18n.js           # CampusI18n: multi-language engine (EN / Odia), translation dictionary, switcher widget
    ├── components.js     # CampusUI: header renderer, toast notifications, search, modals
    ├── student.js        # StudentApp: handles all 11 student tabs, requests, and interactions
    ├── admin.js          # AdminApp: handles all 8 admin tabs, approvals, circular publishing
    ├── supabase.js       # SupabaseCampusService: 2-way cloud sync, schema mappings & realtime
    └── app.js            # Landing page initialization logic
```

---

## 4. Key Files & Roles

| File | Purpose |
|---|---|
| `student-auth.html` | Pure login and password recovery page for students. Uses institutional credentials. No public sign-up. Fully mobile responsive. |
| `admin-auth.html` | Dedicated administrative login interface for deans, proctors, and wardens. Includes admin contact desk modal. |
| `index.html` | Public university homepage with continuous right-to-left urgent notice ticker, portal cards, and emergency directory. |
| `student.html` | Student single-page app container with navigation ribbon and dynamic tab views. |
| `admin.html` | Administrative single-page app console with status metrics, approval queues, and circular dispatch tools. |
| `js/store.js` | Single source of truth for frontend data (`window.campusStore`). Manages CRUD operations and broadcasts changes via `campus_data_updated`. |
| `js/auth.js` | Session manager (`window.AuthService`). Manages role verification (`student` vs `admin`), active user sessions, and default credentials. |
| `js/components.js` | Shared UI layer (`window.CampusUI`). Renders standard institutional header, toasts, confirmation modals, and search helpers. |
| `js/supabase.js` | Optional 2-way real-time persistence layer connecting to Supabase cloud PostgreSQL. Subscribes to websocket changes and syncs local store. |

---

## 5. Implemented Features

### Student Portal (`student.html`)
1. **Dashboard Overview**: Digital university identity card, quick summary counts (active passes, open complaints, notices), and recent activity stream.
2. **Digital Gate Pass**: Submit exit passes with departure/return datetime, purpose, and emergency contact. Real-time approval status and QR clearance badge.
3. **Leave Applications**: Formal academic and hostel leave requests with reason and dates.
4. **Hostel Complaints**: Maintenance ticketing (electrical, plumbing, carpentry, cleaning, internet) with room details and status updates.
5. **Fee Queries & Statements**: Review semester fee breakdown, dues, transaction history, and submit fee clarification inquiries.
6. **Assignments & Coursework**: View and download uploaded semester course assignments by subject.
7. **Exam Datesheets**: View upcoming mid-sem/end-sem examination schedules and syllabus links.
8. **Lost & Found Board**: View public lost/found item notices and report items.
9. **Emergency Contacts**: One-touch access to Security Control, Chief Warden, Campus Health Center, and Proctorial Board.
10. **Student Profile**: Academic and personal details view.

### Campus Administration Console (`admin.html`)
1. **Overview Dashboard**: System-wide statistics, pending leave/gate pass counts, and critical notifications.
2. **Gate Pass Management**: Review student outpass requests with 1-click Approve / Reject actions.
3. **Leave Approvals**: Review and sanction hostel/academic leaves.
4. **Complaint Dispatch**: Filter, review, and change ticket status (Open → In Progress → Resolved) for hostel repairs.
5. **Fee Queries Desk**: Review financial queries from students and post official responses.
6. **Notice Board Publishing**: Create, publish, and delete institutional circulars with priority tags (Urgent vs General).
7. **Campus Directory & Access Management (ADMIN001 Exclusive)**: Simple, authoritative user management console available strictly for Primary Super Administrator (`ADMIN001`). View and search students and administrators, enroll new students with credentials, provision new administrators, and remove accounts (with built-in deletion protection for `ADMIN001`).
8. **Exam Schedule Manager**: Manage course datesheet entries.

---

## 6. Authentication & Security Architecture

1. **Role-Based Authentication**:
   - `student`: Standard student access to `student.html`.
   - `admin`: Elevated access to `admin.html`.
2. **Default Institutional Credentials** (in `js/auth.js`):
   - **Admin**: `ADMIN001` / `admin001` (or `admin123`)
   - **Student**: `STD001` / `student001`
3. **Session Persistence & Multi-Tab Synchronization**:
   - Key `BPUT_AUTH_SESSION_V1` in `localStorage`.
   - Asynchronous route protection via `AuthService.checkStudentSession()` and `AuthService.checkAdminSession()`.
   - Prevents race conditions on page load/reload via institutional loading overlay (`#auth-loading-overlay`).
   - Sessions persist across page reloads and across tabs in the same browser.
   - Explicit `AuthService.logout()` completely clears session and invalidates access.
4. **No Public Registration**:
   - Institutional accounts are provisioned via university database/admission cell. No open public self-registration.

---

## 7. Database & Data Storage

### Dual-Layer Storage Architecture:
1. **Primary / Client-side Cache (`js/store.js`)**:
   - Uses `localStorage` key `BPUT_CAMPUS_STORE_V1`.
   - Initializes from `INITIAL_DATA` (`js/data.js`) if empty.
   - Dispatches `campus_data_updated` custom event for instant multi-tab reactivity.
2. **Cloud Database (`js/supabase.js`)**:
   - Supabase PostgreSQL project: `https://keenqhjcxqdqnjipppny.supabase.co`
   - Tables: `students`, `leave_applications`, `gate_passes`, `complaints`, `notices`, `fee_queries`, `lost_and_found`, `assignments`, `exam_datesheets`.
   - Real-time channel `campus-realtime-sync` listens to Postgres changes via WebSockets.

---

## 8. UI & Design System

- **Colors**:
  - University Navy: `#0b2545`
  - University Blue: `#133b5c`
  - Institutional Accent Gold: `#c59b27`
  - Secondary Slate & Accent Amber
- **Typography**:
  - Headings: `Plus Jakarta Sans`
  - Body: `Inter`
- **Responsive Layout**:
  - Mobile-first approach supporting widths from 320px up to 4K displays.
  - Horizontal scrolling tab ribbons on mobile (`.mobile-nav-scroll`).
  - Stacked cards with touch-friendly tap targets (minimum 44px height).

---

## 9. Multi-Language System (Feature 1 — Completed)

- **Engine**: `js/i18n.js` — `CampusI18n` singleton exposed as `window.CampusI18n`.
- **Languages**: English (`en`, default) and Odia (`or`, ଓଡ଼ିଆ).
- **Persistence**: `localStorage` key `BPUT_LANG_PREFERENCE`.
- **Attributes**:
  - `data-i18n="key"` → text content
  - `data-i18n-placeholder="key"` → input placeholder
  - `data-i18n-title="key"` → tooltip/aria title
- **Switcher widget**: Compact `EN | ଓଡ଼ିଆ` toggle. Mounted via `CampusI18n.mountSwitcher("elementId")`.
  - On `index.html`: `#index-lang-switcher` and `#mobile-lang-switcher`
  - On auth pages: `#student-lang-switcher`, `#admin-lang-switcher`
  - On dashboards: embedded inside `renderInstitutionalHeader()` in `components.js`
- **Event**: Switching language fires `campus_language_changed` custom event on `window`.
- **Adding new translations**: Add `data-i18n="your_key"` to HTML, then add `your_key: "..."` to both `en` and `or` dictionaries in `js/i18n.js`.

---

## 10. Light / Dark Mode System (Feature 2 — Completed)

- **Engine**: `js/theme.js` — `CampusTheme` singleton exposed as `window.CampusTheme`.
- **CSS Tokens & Design System**: Defined in `css/styles.css` under `:root` (Light) and `html.dark` (Dark).
  - Light mode: crisp institutional white/slate surfaces (`#f8fafc`, `#ffffff`), deep navy accents (`#0b2545`), dark readable text (`#0f172a`).
  - Dark mode: midnight slate canvas (`#080e1a`), dark elevated surfaces (`#0f1b33`, `#142342`), high-contrast text (`#f8fafc`), vibrant BPUT blue (`#60a5fa`) and gold (`#fbbf24`) accents.
- **Persistence**: `localStorage` key `BPUT_THEME_PREFERENCE` (`"light"` | `"dark"`). Default is `"light"`.
- **Anti-FOUC**: Inline script in `<head>` of all 5 pages applies `.dark` before first paint.
- **Toggle Widget**: Compact, accessible icon-based toggle `☀️ Light | 🌙 Dark` (`.bput-theme-switcher`).
  - On `index.html`: `#index-theme-toggle` (top ribbon) and `#mobile-theme-toggle` (mobile menu drawer).
  - On auth pages: `#student-theme-toggle` and `#admin-theme-toggle` in top ribbon.
  - On dashboards: embedded inside `CampusUI.renderInstitutionalHeader()` in `js/components.js`.
- **Event**: Fires `campus_theme_changed` event on `window` when toggled.
- **Smooth Transition**: Applies `.theme-transition` class on root during toggle for a 0.2s smooth color/surface shift without layout movement.
- **Multi-language Coexistence**: Works 100% independently from `CampusI18n`. Supports English+Light, English+Dark, Odia+Light, and Odia+Dark.

---

## 11. Privacy & Security System (Feature 3 — Completed)

- **Session Architecture & Persistence**:
  - `AuthService` (`js/auth.js`) provides `checkStudentSession()`, `checkAdminSession()`, `getSession()`, and `onAuthStateChange()`.
  - Eliminates reload redirect race condition: removes premature `<head>` redirect; introduces `#auth-loading-overlay` during async session check.
  - Multi-tab synchronization: opening a protected page in another tab of the same browser reads the persistent session and allows direct access without re-login.
  - Page refresh: reading persistent session prevents unwanted redirect to login.
  - Session termination: `AuthService.logout()` invalidates the session and redirects; browser Back button cannot open protected portals.
- **Privacy & Security Section in Student Portal (`#tab-security`)**:
  - Accessible via dedicated navigation tab with `shield-check` icon.
  - **Change Password**: Validates current password, new password, and confirmation; updates `jee_reg_no` directly in Supabase cloud PostgreSQL `students` table; syncs local store and credentials; notifies user with "Password updated successfully."
  - **Student Data Privacy Statement**: Explains institutional data processing under BPUT Odisha regulations.
  - **Authentication & Access Standards**: Details protected session tokens and credential confidentiality.
  - **Transport Security**: Highlights TLS/HTTPS protection on production university domains.
  - **Device Sign-Out**: Provides direct session termination.
- **Multi-Language Support**: Fully translated into English and Odia.
- **Theme Support**: Adapts automatically to Light and Dark modes.

---

## 12. Important Notes for Future AI Sessions

- **DO NOT MODIFY BACKEND / DATABASE SCHEMA / RLS POLICIES** unless explicitly instructed by the user.
- **DO NOT RESTORE DEMO CREDENTIAL BOXES** to any login screens.
- **DO NOT RESTORE "CREATE STUDENT ACCOUNT"** or student registration forms.
- **DO NOT RESTORE "NAAC ACCREDITED"** badge or text to any page.
- **DO NOT add Hindi or other languages** until explicitly requested. Only EN and Odia are supported.
- Keep the pure Vanilla JS architecture; do not introduce npm bundlers, frameworks, or transpilations without explicit user request.
- Any new visible UI text **must** have `data-i18n` attribute + matching keys in both EN and OR dictionaries.
- Any new custom component **must** support both Light and Dark mode using the CSS design tokens (`var(--surface)`, `var(--text-primary)`, `var(--border)`, etc.).

