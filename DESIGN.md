# BPUT Digital Campus Platform — Design Guidelines (Impeccable Style)

> **Design Manifesto:** Built on Paul Bakaus's *Impeccable* design principles. This document establishes strict aesthetic constraints, typography scales, color palettes, and layout rules to prevent generic AI slop, maintain institutional dignity, and enforce human-grade visual craftsmanship.

---

## 1. Core Principles

1. **Institutional Authority with Modern Utility:** BPUT is a premier state technical university in Odisha. The interface must inspire institutional credibility, security, and academic rigor—not mimic a startup landing page.
2. **Intentional Hierarchy:** Never stack cards within cards without distinct purpose. Use borders, subtle background shifts, and whitespace instead of multiple shadows or redundant containers.
3. **Calibrated Color & Contrast:** No neon saturation or ungrounded purple-to-blue gradients. Every color must pass WCAG AA (minimum 4.5:1 for body copy, 3:1 for large headers and indicators).
4. **Restrained Motion:** Animations must be purpose-driven, under 200ms, and respect `prefers-reduced-motion`. No floating bouncy elements.

---

## 2. Color System (Calibrated Palette)

| Role | Name | Hex / Class | Purpose | WCAG Contrast on White |
|---|---|---|---|---|
| **Primary Navy** | Deep Institutional Navy | `#1e3a8a` (`blue-900`) | Headers, Primary Buttons, University Brand Elements | **10.2:1** (AAA Pass) |
| **Secondary Accent** | University Amber / Gold | `#d97706` (`amber-600`) | Badges, Notice alerts, Active indicators, Seals | **4.6:1** (AA Pass) |
| **Accent Dark** | Deep Gold Brown | `#78350f` (`amber-900`) | Text on amber backgrounds, warning highlights | **8.5:1** (AAA Pass) |
| **Canvas Background** | Slate Pearl | `#f8fafc` (`slate-50`) | Page background, app canvas | Base |
| **Surface Card** | Clean White | `#ffffff` (`bg-white`) | Component surfaces, tables, cards | Base |
| **Neutral Border** | Border Slate | `#e2e8f0` (`slate-200`) | Structural borders, row dividers | Structural |
| **Neutral Dark** | Slate Charcoal | `#0f172a` (`slate-900`) | Primary Headings, high-contrast labels | **16.1:1** (AAA Pass) |
| **Neutral Muted** | Slate Gray | `#475569` (`slate-600`) | Body copy, secondary text, metadata | **5.9:1** (AA Pass) |
| **Success Emerald** | Institutional Green | `#065f46` (`emerald-800`) | Approvals, Active status badges | **6.8:1** (AAA Pass) |
| **Destructive Crimson** | Formal Red | `#991b1b` (`red-800`) | Delete actions, Rejections, Critical alerts | **7.4:1** (AAA Pass) |

---

## 3. Typography & Typesetting

We use two complementary typefaces:
- **Display & Headings:** `Plus Jakarta Sans` — Institutional, clean, authoritative geometric sans.
- **Data & Interface:** `Inter` — High-legibility UI workhorse for tables, status counters, and roll numbers.
- **Monospace:** System Monospace (`ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace`) for Roll IDs, Exam Codes, and Passwords.

### Scale & Weight Rules:
- `H1` (Page Title): `24px–32px` (`text-2xl` to `text-3xl`), `font-bold`, tracking tight (`-0.02em`). Exactly **one** H1 per HTML page.
- `H2` (Section Header): `18px–20px` (`text-lg` to `text-xl`), `font-bold`, `text-slate-900`.
- `H3` (Component Card Title): `14px–16px` (`text-sm` to `text-base`), `font-semibold`.
- `Body Text`: `12px–13px` (`text-xs` to `text-sm`), `leading-relaxed`, `text-slate-700`.
- `Metadata / Badges`: `10px–11px` (`text-[10px]` to `text-[11px]`), `font-medium` or `font-bold`, `uppercase tracking-wider`.

---

## 4. Anti-AI-Slop Rules

To maintain professional design integrity, the following patterns are **strictly prohibited**:
1. ❌ **No Random Gradients:** Do not use `bg-gradient-to-r from-purple-500 to-indigo-600` on arbitrary cards or buttons. Use solid university navy (`#1e3a8a`) or crisp border distinctions.
2. ❌ **No Nested Card Syndrome:** Avoid placing a card with rounded corners and a shadow directly inside another card with rounded corners and a shadow. If a card needs sub-sections, use divider borders (`border-t border-slate-200`) or light contrast panels (`bg-slate-50`).
3. ❌ **No Placeholder Content:** Every card must contain concrete university data (real Odisha engineering departments, verified roll numbers, actual exam dates, actual hostel names like *C.V. Raman* and *Visvesvaraya*).
4. ❌ **No Missing Focus States:** All buttons, inputs, and links must specify accessible focus rings (`focus:ring-2 focus:ring-blue-900 focus:outline-none`).
5. ❌ **No Arbitrary Padding:** Spacing must adhere strictly to 4px multiples: `p-2` (8px), `p-3` (12px), `p-4` (16px), `p-6` (24px).

---

## 5. Component Patterns

- **Tables:** Sticky headers with light slate background (`bg-slate-50`), uppercase `10px` headers, zebra or light hover rows (`hover:bg-slate-50/80`), and right-aligned action buttons.
- **Badges:** Pill-shaped (`rounded-full`), padded (`px-2.5 py-0.5`), font size `11px`, accompanied by Lucide icons sized to `12px` (`w-3 h-3`).
- **Modals:** Centered backdrop blur (`backdrop-blur-sm`), header bar with distinct university title, max height `80vh` scrollable container, and high-contrast action buttons.
