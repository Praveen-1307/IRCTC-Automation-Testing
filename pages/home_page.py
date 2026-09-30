"""Page Object Model for IRCTC Home Page."""
from playwright.sync_api import Locator, Page
from utils.config import BASE_URL, HOME_URL
from utils.logger import logger


class HomePage:
    """Represents the IRCTC Portal Home and Landing Page."""

    def __init__(self, page: Page):
        self.page = page
        # Locators
        self.logo = page.locator("img[alt*='IRCTC'], .header-icon-logo, a.header-icon-logo").first
        self.nav_menu = page.locator("nav, .h-menu, .navigation-box, .nav-item").first
        self.login_button = page.locator("a.loginText, a:has-text('LOGIN'), button:has-text('LOGIN')").first
        self.register_link = page.locator("a:has-text('REGISTER'), a[routerlink*='registration']").first
        self.advisory_ok_button = page.locator(
            "button:has-text('English'), button:has-text('OK'), .btn-primary:has-text('OK'), button:has-text('Ok')"
        ).first
        self.advisory_dialog = page.locator("p-dialog, .ui-dialog, .modal").first
        self.disha_close_btn = page.locator("#disha-banner-close, .close-disha, #askDishaClose").first

    def open(self, url: str = BASE_URL) -> None:
        """Navigate to the IRCTC base URL and dismiss any initial dialogs."""
        logger.info("Opening IRCTC Portal at URL: %s", url)
        self.page.goto(url, wait_until="domcontentloaded")
        self.dismiss_advisories()

    def dismiss_advisories(self) -> None:
        """Dismiss initial welcome/language selection, COVID, or advisory modals if present."""
        language_selectors = [
            "button:has-text('English')",
            "a:has-text('English')",
            "span:has-text('English')",
            "div:has-text('English')",
            "[aria-label*='English' i]",
            "button:has-text('OK')",
            "button:has-text('Ok')",
            "a:has-text('OK')",
            "a:has-text('Ok')",
            ".btn-primary:has-text('OK')",
            "button:has-text('Continue')",
            "a:has-text('Continue')",
        ]

        for selector in language_selectors:
            try:
                candidate = self.page.locator(selector).first
                if candidate.is_visible(timeout=2000):
                    logger.info(
                        "Dismissing IRCTC advisory/language selection popup using selector: %s",
                        selector,
                    )
                    candidate.click(force=True)
                    self.page.wait_for_timeout(500)
                    break
            except Exception:
                continue

        try:
            # Check for AskDisha chatbot overlay if present
            if self.disha_close_btn.is_visible(timeout=1000):
                self.disha_close_btn.click()
        except Exception:
            pass

    def get_title(self) -> str:
        """Get the current page title."""
        title = self.page.title()
        logger.info("IRCTC page title: '%s'", title)
        return title

    def is_logo_visible(self) -> bool:
        """Check if IRCTC brand logo is visible."""
        visible = self.logo.is_visible()
        logger.info("IRCTC logo visible: %s", visible)
        return visible

    def is_nav_menu_visible(self) -> bool:
        """Check if navigation menu bar is visible."""
        visible = self.nav_menu.is_visible()
        logger.info("Navigation menu visible: %s", visible)
        return visible

    def open_login(self) -> None:
        """Click the Login action on the header."""
        logger.info("Clicking Login button on Home Page")
        self.login_button.wait_for(state="visible")
        self.login_button.click()

    def click_register(self) -> None:
        """Click the Register action on the header."""
        logger.info("Clicking Register button on Home Page")
        self.register_link.wait_for(state="visible")
        self.register_link.click()

    def refresh(self) -> None:
        """Reload the page and re-handle any advisories."""
        logger.info("Refreshing the home page")
        self.page.reload(wait_until="domcontentloaded")
        self.dismiss_advisories()

    def get_current_url(self) -> str:
        """Return the current URL of the page."""
        return self.page.url
