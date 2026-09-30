# IRCTC Automation Testing

A production-grade, GitHub-ready automated testing framework for the publicly accessible [IRCTC Website](https://www.irctc.co.in/) built with **Python 3**, **Playwright**, and **Pytest**, structured according to the **Page Object Model (POM)** design pattern.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Technologies Used](#technologies-used)
- [Key Features](#key-features)
- [Project Structure](#project-structure)
- [Test Cases (40 Test Cases)](#test-cases)
- [Installation Guide](#installation-guide)
- [Test Execution Guide](#test-execution-guide)
  - [Run All 40 Tests](#run-all-40-tests)
  - [Run Smoke Tests](#run-smoke-tests)
  - [Run Train Search Tests](#run-train-search-tests)
  - [Run Headed Mode](#run-headed-mode)
  - [Run a Single Test](#run-a-single-test)
  - [Parallel Test Execution](#parallel-test-execution)
  - [Generate and View HTML Reports](#generate-and-view-html-reports)
- [Page Object Model Architecture](#page-object-model-architecture)
- [Failure Screenshots, Logs, and Tracing](#failure-screenshots-logs-and-tracing)
- [Limitations & Ethical Boundaries](#limitations--ethical-boundaries)
- [GitHub Upload Commands](#github-upload-commands)

---

## Project Overview

The IRCTC Automation Testing project provides robust end-to-end and regression test coverage for the Indian Railway Catering and Tourism Corporation (IRCTC) web portal. The framework validates search capabilities, station autocomplete suggestions, journey date inputs, quota and travel class preferences, search result train cards, login and registration UI validation, and responsive page behaviors.

All tests operate strictly on the public UI layers without completing transactions, entering payment portals, submitting OTPs, or attempting CAPTCHA bypass.

---

## Technologies Used

- **Language:** Python 3.10+
- **Browser Automation:** [Playwright for Python](https://playwright.dev/python/) (Synchronous API)
- **Test Framework:** [Pytest](https://docs.pytest.org/)
- **HTML Reporting:** [pytest-html](https://pytest-html.readthedocs.io/)
- **Parallel Execution:** [pytest-xdist](https://pytest-xdist.readthedocs.io/)
- **Logging:** Python standard `logging` with synchronized console and rotating file outputs
- **Design Pattern:** Page Object Model (POM)

---

## Key Features

1. **Page Object Model (POM):** Clean separation of web elements, interaction logic, and test assertions across distinct page classes.
2. **40 Complete Test Cases:** Comprehensive test coverage covering launch, navigation, station selection, date pickers, quotas, train results, login, and registration.
3. **Automated Failure Screenshots:** Automatically snaps full-page screenshots whenever any test fails and links them into the HTML report.
4. **Resilient Selectors:** Utilizes role-based locators, ARIA attributes, PrimeNG Angular identifiers, and auto-waiting instead of brittle coordinates or arbitrary sleeps.
5. **Multi-Browser Support:** Native support for Chromium, Firefox, and WebKit engines with headless and headed toggles.
6. **Smart Popup & Advisory Handling:** Automatically handles IRCTC language selection, COVID guidelines, and disclaimer modals.
7. **Custom CLI Runner (`run_tests.py`):** Convenient entry point to trigger target suites, parallel execution, and report generation.

---

## Project Structure

```text
irctc-automation-testing/
│
├── pages/
│   ├── __init__.py               # Exports POM classes
│   ├── home_page.py              # Home page actions, header, logo, and advisories
│   ├── train_search_page.py      # Station inputs, autocomplete, date, quota, class
│   ├── search_results_page.py    # Train list cards, availability, fare, and modify search
│   ├── login_page.py             # Login modal UI and required fields validation
│   └── registration_page.py      # User registration fields and input validations
│
├── tests/
│   ├── __init__.py               # Test package initialization
│   ├── test_home_page.py         # TC01 - TC10, TC38 (Launch, Header, Navigation)
│   ├── test_train_search.py      # TC11 - TC21 (Autocomplete, Quotas, Classes, Dates)
│   ├── test_search_results.py    # TC22 - TC31 (Train cards, Schedules, Fares)
│   ├── test_login.py             # TC32 - TC34 (Login modal and field checks)
│   ├── test_registration.py      # TC35 - TC37 (Registration form validation)
│   └── test_end_to_end.py        # TC39 - TC40 (Screenshot verification and Full E2E)
│
├── utils/
│   ├── __init__.py               # Utilities package initialization
│   ├── config.py                 # URLs, timeouts, and directory paths
│   ├── logger.py                 # Structured console and file logging
│   └── test_data.py              # Station codes, quotas, classes, and dummy data
│
├── screenshots/                  # Directory for test failure screenshots
│   └── .gitkeep
├── reports/                      # Directory for pytest-html report and logs
│   └── .gitkeep
├── videos/                       # Directory for optional test video recordings
│   └── .gitkeep
├── traces/                       # Directory for optional Playwright execution traces
│   └── .gitkeep
│
├── conftest.py                   # Pytest fixtures, browser management, and hooks
├── pytest.ini                   # Pytest test discovery, logging, and marker configuration
├── requirements.txt              # Project dependencies
├── .gitignore                    # Git ignore file for artifacts and virtual environments
├── README.md                     # Comprehensive project documentation
└── run_tests.py                  # CLI test runner script
```

---

## Test Cases

The test suite contains **exactly 40 test cases** mapping to functional specifications:

| Test ID | Test Case Title | Module | Category | Description |
|---|---|---|---|---|
| **TC01** | Verify IRCTC website launches successfully | Home | Smoke | Verifies browser navigates to IRCTC portal and URL is valid |
| **TC02** | Verify IRCTC home page title | Home | Smoke | Validates home page `<title>` contains "IRCTC" |
| **TC03** | Verify IRCTC logo is displayed | Home | Smoke | Checks that the brand logo is displayed on the header |
| **TC04** | Verify main navigation/menu is displayed | Home | Smoke | Ensures the primary navigation bar is visible |
| **TC05** | Verify From station field is visible | Home | Train Search | Verifies origin station input field presence |
| **TC06** | Verify To station field is visible | Home | Train Search | Verifies destination station input field presence |
| **TC07** | Verify journey date field is visible | Home | Train Search | Confirms travel date picker is displayed |
| **TC08** | Verify class/berth preference controls are displayed | Home | Train Search | Validates journey class dropdown is displayed |
| **TC09** | Verify quota option is displayed | Home | Train Search | Checks that quota selection control is displayed |
| **TC10** | Verify Search button is displayed | Home | Smoke | Validates primary "Search Trains" action button |
| **TC11** | Search trains using valid From and To stations | Train Search | Smoke | Executes search with valid stations (NDLS to CNB) |
| **TC12** | Verify From station autocomplete suggestions | Train Search | Functional | Checks dropdown suggestions appear when typing station |
| **TC13** | Verify To station autocomplete suggestions | Train Search | Functional | Checks dropdown suggestions appear when typing destination |
| **TC14** | Verify invalid From station input validation | Train Search | Negative | Ensures invalid string yields no matching station records |
| **TC15** | Verify invalid To station input validation | Train Search | Negative | Ensures invalid destination yields no station records |
| **TC16** | Verify From and To stations cannot be the same | Train Search | Negative | Ensures application validates against identical origin and destination |
| **TC17** | Verify journey date can be selected | Train Search | Functional | Selects a valid date and checks value persistence |
| **TC18** | Verify past journey date validation | Train Search | Negative | Asserts that past journey dates cannot be booked |
| **TC19** | Verify valid future journey date | Train Search | Functional | Verifies travel date in the future is accepted |
| **TC20** | Verify quota dropdown/options | Train Search | Functional | Verifies presence of GENERAL, TATKAL, LADIES, etc. |
| **TC21** | Verify different travel class options where available | Train Search | Functional | Confirms standard classes (1A, 2A, 3A, SL) exist |
| **TC22** | Verify search results page loads | Search Results | Smoke | Validates navigation to `/train-list` after search |
| **TC23** | Verify train search results contain train information | Search Results | Functional | Checks that returned train cards count is greater than zero |
| **TC24** | Verify train number/name is displayed | Search Results | Functional | Confirms train names and 5-digit train numbers are shown |
| **TC25** | Verify train departure information is displayed | Search Results | Functional | Confirms departure time and station on the train card |
| **TC26** | Verify train arrival information is displayed | Search Results | Functional | Confirms arrival time and station on the train card |
| **TC27** | Verify available class information | Search Results | Functional | Verifies travel class badges (SL, 3A, etc.) on cards |
| **TC28** | Verify seat availability information where publicly displayed | Search Results | Functional | Confirms seat availability indicators or Refresh buttons |
| **TC29** | Verify fare information where publicly displayed | Search Results | Functional | Confirms fare display or inquiry capability |
| **TC30** | Verify search results can be refreshed/reloaded | Search Results | Regression | Tests availability refresh interaction on train cards |
| **TC31** | Verify navigation back to search page | Search Results | Functional | Verifies "Modify Search" returns to search interface |
| **TC32** | Verify login page opens | Login | Smoke | Opens login modal/dialog from header link |
| **TC33** | Verify login fields are displayed | Login | Functional | Confirms username, password, and sign-in buttons |
| **TC34** | Verify login validation for empty fields | Login | Negative | Asserts validation triggers upon blank submission |
| **TC35** | Verify registration page opens | Registration | Smoke | Opens user registration portal `/user-registration` |
| **TC36** | Verify registration form fields are displayed | Registration | Functional | Verifies username, password, email, and mobile inputs |
| **TC37** | Verify registration form validation for required fields | Registration | Negative | Asserts validation on required blank fields |
| **TC38** | Verify browser refresh behavior | Home | Regression | Verifies page state and form integrity across reload |
| **TC39** | Verify screenshot is captured when a test fails | E2E | Regression | Tests screenshot capture mechanism and image creation |
| **TC40** | Verify complete train-search workflow from home page to results | E2E | Smoke / E2E | End-to-end journey from home page inputs to search results |

---

## Installation Guide

### 1. Clone the Repository

```bash
git clone https://github.com/<your-username>/irctc-automation-testing.git
cd irctc-automation-testing
```

### 2. Create and Activate a Virtual Environment

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**
```cmd
python -m venv venv
venv\Scripts\activate.bat
```

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Install Playwright Browsers

```bash
playwright install
```

*(Optional: Install system dependencies on Linux: `playwright install-deps`)*

---

## Test Execution Guide

You can run the tests using either the standard `pytest` CLI or the included runner script `run_tests.py`.

### Run All 40 Tests

Using `pytest`:
```bash
pytest --html=reports/report.html --self-contained-html
```

Using the test runner:
```bash
python run_tests.py
```

### Run Smoke Tests

```bash
pytest -m smoke --html=reports/report.html --self-contained-html
```
or:
```bash
python run_tests.py smoke
```

### Run Train Search Tests

```bash
pytest -m train_search --html=reports/report.html --self-contained-html
```
or:
```bash
python run_tests.py train_search
```

### Run Headed Mode

To view the browser actions in real-time on your screen:
```bash
pytest --headed
```
or:
```bash
python run_tests.py --headed
```

### Run a Single Test

Run an individual test case by function name:
```bash
pytest tests/test_train_search.py -k "test_TC11_search_trains_using_valid_stations" -v
```

Run a single module:
```bash
pytest tests/test_login.py -v
```

### Parallel Test Execution

Leverage multi-core CPUs with `pytest-xdist`:
```bash
pytest -n auto --html=reports/report.html --self-contained-html
```
or:
```bash
python run_tests.py --parallel
```

### Generate and View HTML Reports

Execution generates a self-contained HTML report at:
`reports/report.html`

**How to open the report:**
- **Windows (PowerShell):**
  ```powershell
  Start-Process reports\report.html
  ```
- **macOS:**
  ```bash
  open reports/report.html
  ```
- **Linux:**
  ```bash
  xdg-open reports/report.html
  ```
- **Browser:** Simply double-click `reports/report.html` in File Explorer or open it in Chrome/Edge/Firefox.

---

## Page Object Model Architecture

The framework encapsulates page logic into reusable classes:

- **`HomePage` (`pages/home_page.py`):**
  - Controls initial portal navigation and landing state.
  - Automatically detects and dismisses language selection and COVID advisory overlays (`button:has-text('English')`, `button:has-text('OK')`).
  - Verifies brand logos, navigation menus, and header triggers.

- **`TrainSearchPage` (`pages/train_search_page.py`):**
  - Manages PrimeNG autocomplete station inputs (`#origin input`, `#destination input`).
  - Interacts with PrimeNG calendar date controls (`p-calendar input`).
  - Interacts with quota and class preference dropdowns (`#journeyQuota`, `#journeyClass`).
  - Executes search submissions and error toast validations.

- **`SearchResultsPage` (`pages/search_results_page.py`):**
  - Verifies train cards rendered on `/nget/booking/train-list`.
  - Extracts train names, 5-digit train numbers, departure times, and arrival times.
  - Interacts with availability inquiry controls and the "Modify Search" workflow.

- **`LoginPage` (`pages/login_page.py`):**
  - Opens and validates the login dialog modal (`app-login`).
  - Locates `userid`, `password`, and submission triggers.
  - Asserts form validation on empty/invalid credential submission without attempting real authentication.

- **`RegistrationPage` (`pages/registration_page.py`):**
  - Navigates to `/nget/profile/user-registration`.
  - Verifies form fields (`userName`, `fullName`, `usrPwd`, `cnfUsrPwd`, `email`, `mobile`).
  - Tests required field validation rules.

---

## Failure Screenshots, Logs, and Tracing

### Screenshots on Failure
Whenever a test fails during execution, `conftest.py` triggers an automated hook:
1. Captures a full-page snapshot.
2. Saves it inside the `screenshots/` directory with a descriptive name, e.g.:
   `screenshots/test_TC16_verify_from_and_to_stations_cannot_be_the_same_20260930_133000.png`
3. Automatically embeds the screenshot into the corresponding failure card in `reports/report.html`.

### Logging
All major actions, navigation steps, selector resolutions, and errors are logged using Python's standard `logging` module.
- Output appears in the console in real-time.
- Persistent logs are appended to `reports/automation.log`.

### Execution Traces & Video Recording
- Record execution videos:
  ```bash
  pytest --video-record
  ```
- Record full Playwright zip traces for debugging:
  ```bash
  pytest --enable-trace
  ```
  View traces using:
  ```bash
  playwright show-trace traces/<test_name>_trace.zip
  ```

---

## Limitations & Ethical Boundaries

In adherence to responsible testing practices and IRCTC platform policies:

1. **No Real Ticket Booking:** The framework never completes ticket reservations.
2. **No Real Financial Transactions:** Tests stop before payment gateways or bank interfaces.
3. **No CAPTCHA Bypass or OCR:** Tests do not attempt to bypass, solve, or automate CAPTCHA challenges.
4. **No Real User Credentials or OTPs:** All authentication checks are confined to UI presence and input validations.
5. **Anti-Bot / Akamai Detection Note:** Headless Chromium requests may experience server-side TLS protocol drops (`net::ERR_HTTP2_PROTOCOL_ERROR`) from IRCTC's CDN firewall. The framework supports **Firefox** and **WebKit** (both headless and headed) as well as **Chromium in headed mode** (`--headed`).
6. **Dynamic UI:** Train availability, quotas, and schedules reflect live railway data and will vary depending on journey date and route.

---

## GitHub Upload Commands

Follow these steps to push this framework to your GitHub repository:

```bash
# 1. Initialize git repository
git init

# 2. Add all files (respecting .gitignore)
git add .

# 3. Create initial commit
git commit -m "feat: complete IRCTC automation testing framework with 40 test cases"

# 4. Set default branch to main
git branch -M main

# 5. Link your remote GitHub repository
git remote add origin https://github.com/<your-username>/irctc-automation-testing.git

# 6. Push to GitHub
git push -u origin main
```
