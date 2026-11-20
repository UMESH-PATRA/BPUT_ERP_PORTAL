import { defineConfig, devices } from "@playwright/test";

/**
 * BPUT Digital Campus Platform — Playwright Test Configuration
 * Configured for multi-browser end-to-end testing of university student & admin portals.
 */
export default defineConfig({
  testDir: "./tests",
  timeout: 30000,
  expect: {
    timeout: 5000
  },
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: [
    ["html", { outputFolder: "audits/playwright-report" }],
    ["list"]
  ],
  use: {
    baseURL: process.env.BASE_URL || "http://127.0.0.1:5000",
    trace: "on-first-retry",
    screenshot: "only-on-failure",
    video: "retain-on-failure"
  },
  projects: [
    {
      name: "chromium",
      use: { ...devices["Desktop Chrome"] }
    },
    {
      name: "firefox",
      use: { ...devices["Desktop Firefox"] }
    },
    {
      name: "webkit",
      use: { ...devices["Desktop Safari"] }
    },
    {
      name: "Mobile Chrome",
      use: { ...devices["Pixel 5"] }
    }
  ],
  webServer: {
    command: "python server.py",
    url: "http://127.0.0.1:5000",
    reuseExistingServer: !process.env.CI,
    timeout: 10000
  }
});
