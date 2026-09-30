"""Pytest fixtures and configuration hooks for IRCTC Automation Suite."""
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Generator
import pytest
from playwright.sync_api import (
    Browser,
    BrowserContext,
    Page,
    Playwright,
    sync_playwright,
)

from utils.config import (
    DEFAULT_BROWSER,
    DEFAULT_TIMEOUT,
    HEADLESS_MODE,
    NAVIGATION_TIMEOUT,
    PROJECT_ROOT,
    REPORTS_DIR,
    SCREENSHOTS_DIR,
    TRACES_DIR,
    VIDEOS_DIR,
)
from utils.logger import logger


def pytest_addoption(parser):
    """Add custom command-line options if not already added by plugins."""
    try:
        parser.addoption(
            "--browser-type",
            action="store",
            default=os.getenv("IRCTC_BROWSER", "chromium"),
            help="Browser type to run tests: chromium, firefox, webkit",
        )
    except ValueError:
        pass

    try:
        parser.addoption(
            "--video-record",
            action="store_true",
            default=False,
            help="Record video for all test runs into videos directory",
        )
    except ValueError:
        pass

    try:
        parser.addoption(
            "--enable-trace",
            action="store_true",
            default=False,
            help="Enable Playwright tracing into traces directory",
        )
    except ValueError:
        pass


@pytest.fixture(scope="session")
def playwright_instance() -> Generator[Playwright, None, None]:
    """Provide a managed Playwright instance for the test session."""
    logger.info("Starting Playwright instance")
    with sync_playwright() as playwright:
        yield playwright
    logger.info("Stopped Playwright instance")


@pytest.fixture(scope="session")
def browser(request, playwright_instance: Playwright) -> Generator[Browser, None, None]:
    """Launch and provide the selected browser (Chromium, Firefox, or WebKit)."""
    # Check if --browser was provided by pytest-playwright or --browser-type
    browser_type_name = "chromium"
    try:
        if request.config.getoption("--browser", default=None):
            browser_type_name = request.config.getoption("--browser")
    except Exception:
        pass

    try:
        if request.config.getoption("--browser-type", default=None):
            browser_type_name = request.config.getoption("--browser-type")
    except Exception:
        pass

    if not browser_type_name:
        browser_type_name = DEFAULT_BROWSER

    browser_type_name = browser_type_name.lower()

    # Determine headless mode
    headed_flag = False
    try:
        headed_flag = request.config.getoption("--headed", default=False)
    except Exception:
        pass

    headless = not headed_flag if headed_flag else HEADLESS_MODE

    logger.info(
        "Launching browser: %s (Headless: %s)", browser_type_name, headless
    )

    launch_args = [
        "--disable-blink-features=AutomationControlled",
        "--no-sandbox",
        "--disable-setuid-sandbox",
    ]

    if browser_type_name == "firefox":
        browser_obj = playwright_instance.firefox.launch(
            headless=headless,
            slow_mo=50 if not headless else 0,
        )
    elif browser_type_name == "webkit":
        browser_obj = playwright_instance.webkit.launch(
            headless=headless,
            slow_mo=50 if not headless else 0,
        )
    else:
        # Default: Chromium
        browser_obj = playwright_instance.chromium.launch(
            headless=headless,
            args=launch_args,
            slow_mo=50 if not headless else 0,
        )

    yield browser_obj

    logger.info("Closing browser: %s", browser_type_name)
    browser_obj.close()


@pytest.fixture(scope="function")
def context(request, browser: Browser) -> Generator[BrowserContext, None, None]:
    """Create an isolated browser context per test case with video/trace support."""
    record_video = False
    try:
        record_video = request.config.getoption("--video-record", default=False)
    except Exception:
        pass

    video_dir = str(VIDEOS_DIR) if record_video else None

    context_obj = browser.new_context(
        viewport={"width": 1366, "height": 768},
        user_agent=(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
        ),
        record_video_dir=video_dir,
        ignore_https_errors=True,
    )

    # Enable Playwright tracing if requested
    enable_trace = False
    try:
        enable_trace = request.config.getoption("--enable-trace", default=False)
    except Exception:
        pass

    if enable_trace:
        context_obj.tracing.start(screenshots=True, snapshots=True, sources=True)

    yield context_obj

    if enable_trace:
        test_slug = re.sub(r"[^\w\-]", "_", request.node.name)
        trace_path = TRACES_DIR / f"{test_slug}_trace.zip"
        context_obj.tracing.stop(path=str(trace_path))
        logger.info("Saved Playwright trace: %s", trace_path)

    context_obj.close()


@pytest.fixture(scope="function")
def page(request, context: BrowserContext) -> Generator[Page, None, None]:
    """Provide a fresh page instance and automatically capture screenshots on failure."""
    page_obj = context.new_page()
    page_obj.set_default_timeout(DEFAULT_TIMEOUT)
    page_obj.set_default_navigation_timeout(NAVIGATION_TIMEOUT)

    # Remove automation flags from navigator object
    page_obj.add_init_script(
        """
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
        });
        """
    )

    test_name = request.node.name
    logger.info("=== STARTING TEST: %s ===", test_name)

    yield page_obj

    # Capture screenshot if test failed
    test_failed = False
    if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
        test_failed = True
    elif hasattr(request.node, "rep_setup") and request.node.rep_setup.failed:
        test_failed = True

    if test_failed:
        clean_name = re.sub(r"[^\w\-]", "_", test_name)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_filename = f"{clean_name}_{timestamp}.png"
        screenshot_path = SCREENSHOTS_DIR / screenshot_filename
        try:
            page_obj.screenshot(path=str(screenshot_path), full_page=True)
            logger.error("Test failed! Captured screenshot: %s", screenshot_path)

            # Attach to pytest-html if present
            if hasattr(request.node, "rep_call"):
                pytest_html = request.config.pluginmanager.getplugin("html")
                if pytest_html is not None:
                    extra = getattr(request.node.rep_call, "extra", [])
                    extra.append(pytest_html.extras.image(str(screenshot_path)))
                    request.node.rep_call.extra = extra
        except Exception as exc:
            logger.warning("Could not capture failure screenshot: %s", exc)

    logger.info("=== FINISHED TEST: %s ===", test_name)
    page_obj.close()


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    """Pytest hook to track test results for screenshot capture and reporting."""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


def pytest_html_report_title(report):
    """Set custom title for pytest-html report."""
    report.title = "IRCTC Automation Test Execution Report"


def pytest_configure(config):
    """Add custom metadata to pytest HTML report."""
    metadata = getattr(config, "_metadata", None)
    if metadata is not None:
        metadata["Project"] = "IRCTC Playwright Automation Framework"
        metadata["Tested Website"] = "https://www.irctc.co.in/"
        metadata["Execution Environment"] = "Public Web Portal"
        metadata["Framework"] = "Pytest + Playwright (POM)"
