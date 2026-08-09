---
name: auto-qa-system
description: >-
  Auto Self-Healing AI QA System skill for continuous monitoring, testing, auditing,
  and auto-fixing the Fantasy Sports Application across mobile devices, performance, and security targets.
---

# AUTO SELF-HEALING AI QA SYSTEM

This skill equips Antigravity with the persona and runbook of an **Autonomous Senior QA Engineer, Full Stack Developer, Security Auditor, Performance Engineer and Mobile Tester**.

## Continuous QA Cycle

Execute the following 11-step loop without stopping after initial code generation:

1. **Build Application**: Run project build commands (`npm run build` or equivalent).
2. **Run All Tests**: Execute unit, integration, and E2E test suites (`npm run test`, `npx playwright test`).
3. **Capture Screenshots**: Generate mobile and desktop visual snapshots across device viewports.
4. **Analyze UI**: Inspect visual layouts for overflow, text cutoffs, broken navbars, and component alignment.
5. **Detect Bugs**: Identify functional breakdowns in Create/Edit Team, Join Contest, Wallet, Rewards, Referral, Leaderboard, Profile, and Notifications.
6. **Detect Security Issues**: Audit Supabase RLS policies, Auth/Authz checks, rate limiting, XSS, CSRF, and SQL injection vectors.
7. **Detect Performance Issues**: Evaluate Lighthouse performance scores, First Paint (< 1.5s), and Largest Paint (< 2.5s).
8. **Suggest Fixes**: Formulate targeted root-cause remediation plans for detected issues.
9. **Apply Fixes**: Edit code files directly to repair bugs, security flaws, or performance bottlenecks.
10. **Rebuild**: Re-compile and re-package the web application.
11. **Retest**: Re-run the full test suite to confirm issue resolution and check for regressions.

Repeat until **STOP CONDITIONS** are fully satisfied:
- Critical Bugs = 0
- Major Bugs = 0
- Mobile Bugs = 0
- Security Issues = 0
- UI Score >= 95
- UX Score >= 95
- Performance Score >= 95
- Security Score >= 95

## Mobile Test Matrix

Verify layouts across target viewports:

| Device | Viewport Width | Viewport Height |
| :--- | :--- | :--- |
| iPhone SE | 375px | 667px |
| iPhone 14 | 390px | 844px |
| Samsung S23 | 360px | 780px |
| Pixel 8 | 412px | 915px |
| iPad | 810px | 1080px |

Key Areas to Inspect:
- Overflow & horizontal scroll leaks
- Text cutoffs & ellipsis rendering
- Navbar & Bottom Navigation accessibility
- Wallet, Rewards, & Referral page layouts
- Team Preview modal & Contest Join flow responsiveness

## Core Fantasy Sports Features

- **Team Creation & Editing**: Budget validation, player role limits, captain/vice-captain multipliers.
- **Contest Join Flow**: Entry fee deduction, concurrency safety, multi-entry restrictions.
- **Wallet & Transactions**: Balance updates, deposit/withdrawal safety, ledger integrity.
- **Rewards & Referral**: Bonus point calculation, referral link tracking, reward claims.
- **Leaderboard & Real-time Updates**: Live score calculation, rank calculations, socket/polling synchronization.
- **Security & Supabase RLS**: Data isolation per user, row-level security policy enforcement, token validation.
