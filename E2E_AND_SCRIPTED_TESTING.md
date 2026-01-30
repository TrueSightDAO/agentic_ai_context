# E2E and scripted testing: prevent regressions like sentiment_importer 500

This doc describes the **best way** to have automated tests that “navigate like a human” and run **predefined scripts** so errors (e.g. 500s on key pages) don’t reach production again.

---

## 1. Two layers (both useful)

| Layer | What it does | Catches | Tooling |
|-------|----------------|---------|---------|
| **Critical-path request specs** | Hit key URLs (no browser), assert 200 and key content | Broken controllers, missing methods, 500s on important pages | RSpec request specs (Rails) |
| **Full E2E (browser)** | Real browser: visit pages, click, fill forms, assert UI | Broken JS, layout, auth flows, cross-page journeys | Playwright or Cypress |

Use **both**: request specs for fast, stable coverage of “does this page load?”; E2E for a smaller set of full user journeys.

---

## 2. Predefined scripts = test scenarios

“Predefined script” = a **test scenario** written in code:

- **Request spec**: “GET /companies/RELX/2026-01-30/180 → 200 and body contains ‘Buy this dip’ or ‘Avoid this dip’.”
- **E2E**: “Open /large_dips → click company RELX → expect company page to load and show dip recommendation.”

Define these in:

- **Rails**: `spec/requests/` (and optionally `spec/features/` or `spec/system/` with Capybara).
- **Playwright/Cypress**: Test files (e.g. `e2e/critical_path.spec.js`).

Run them in **CI** (e.g. GitHub Actions) on every PR so regressions are caught before merge.

---

## 3. What was added for sentiment_importer

- **Request spec** that would have caught the `dip_model_prediction` 500:
  - **File**: `sentiment_importer/spec/requests/companies_controller_spec.rb`
  - **Flow**: Sign in user, create company + daily_trade, GET company show URL, expect 200 and body to match “Buy this dip” or “Avoid this dip”.
- **Devise**: `spec/spec_helper.rb` now includes `Devise::Test::IntegrationHelpers` for `type: :request` so `sign_in` works in request specs.

Run from repo root (ensure test DB exists and is migrated first):

```bash
cd sentiment_importer
RAILS_ENV=test bundle exec rails db:create db:migrate   # if needed
bundle exec rspec spec/requests/companies_controller_spec.rb
```

---

## 4. Extending with more “human-like” scripts

### Option A: More request specs (recommended first)

Add one request spec per critical URL so each important page is asserted:

- `GET /large_dips` → 200, body includes expected structure.
- `GET /companies/:id/:the_date/:period` (already added).
- Any other key routes (e.g. prediction form, game API).

No browser; fast and reliable in CI.

### Option B: Full E2E with Playwright (or Cypress)

When you want **real browser** behavior (click, navigate, forms):

1. **Install Playwright** (or Cypress) in the repo or in a small e2e project.
2. **Define scripts** (e.g. `e2e/sentiment_importer_critical.spec.ts`):
   - Start app (or hit a deployed URL).
   - Visit `/large_dips`, then click through to a company page.
   - Assert: status 200, and text like “Buy this dip” or “Avoid this dip” is visible.
3. **Run in CI** after the app is up (or against staging).

Playwright is language-agnostic (Node/TypeScript) and can test any site; Cypress is JS-focused and also works well.

### Option C: Capybara + RSpec (Rails-native E2E)

If you prefer to stay inside Rails:

- Uncomment `config.include Capybara::DSL` in `spec_helper.rb` and add the Capybara gem.
- Add `spec/features/` or `spec/system/` specs that use `visit`, `click_link`, `expect(page).to have_text(...)`.
- Use a headless browser (e.g. Selenium with Chrome headless) so CI can run them.

---

## 5. Summary

- **Best way** to prevent regressions like the sentiment_importer 500: **automated tests driven by predefined scripts** (request specs + optional E2E).
- **Request specs** = “navigate” to key URLs (no browser), assert status and content; they’re the fastest way to catch 500s and missing methods.
- **E2E (Playwright/Cypress/Capybara)** = real browser, for full “human-like” flows when you need them.
- **Scripts** = test files that encode the scenarios; run them in **CI** on every PR so such errors don’t happen again.

The new `companies_controller_spec.rb` is an example of a predefined script that would have caught the recent error; add more request specs (and optionally E2E) for other critical pages.
