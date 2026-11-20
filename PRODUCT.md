# BPUT Digital Campus Platform — Product Requirements & Boundaries

> **Document Scope:** Product definition, user personas, privilege matrices, and operational boundaries for Biju Patnaik University of Technology (BPUT) Digital Campus Platform.

---

## 1. Product Mission & Value Proposition

The **BPUT Digital Campus Platform** digitizes paper-heavy university administrative procedures across BPUT's Rourkela constituent campus and affiliated colleges. It replaces paper outpasses, physical notices, and manual grievance registers with a real-time, authenticated web portal.

---

## 2. User Personas & Permissions Matrix

| Feature Module | Student (`role: student`) | Campus Admin (`role: admin`) | Super Admin (`ADMIN001`) |
|---|---|---|---|
| **Digital Gate Pass** | Create, view status, access QR badge | Approve / Reject requests | Approve / Reject requests |
| **Hostel Leave Application** | Submit leave, view sanction status | Sanction / Deny leave | Sanction / Deny leave |
| **Hostel Complaints Register** | File complaints (plumbing, Wi-Fi, etc.) | Update status (Open → Working → Resolved) | Manage all complaints |
| **Fee Statements & Queries** | Review ledger, submit queries | Answer student fee queries | Full fee audit |
| **Official Circulars & Notices** | Read public & category notices | Draft, publish, and delete notices | Full publishing control |
| **Exam Datesheets & Hall Slips** | View timetable, portion syllabus | Post & update exam dates | Full datesheet control |
| **Campus Directory & Credentialing** | ❌ Strictly hidden | ❌ Access restricted | **Full Super Admin Access** (Add/Remove students & admins) |

---

## 3. Core Technical & Performance Non-Negotiables

1. **Zero Downtime Local Fallback:** The application must function offline or on a local intranet without external cloud dependencies.
2. **Deterministic Authentication:** Primary Super Admin (`ADMIN001`) and standard Student Roll (`STD001`, `230101`–`230110`) logins must work deterministically.
3. **Core Web Vitals Thresholds:**
   - **LCP:** < 2.5s
   - **FID / INP:** < 100ms
   - **CLS:** < 0.1
4. **Accessible Semantics:** Single `<h1>` per page, complete ARIA landmark roles (`nav`, `main`, `footer`), keyboard navigability, and breadcrumbs on all subpages.
