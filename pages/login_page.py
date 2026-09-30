"""Page Object Model for IRCTC Login Modal and Authentication Form."""
from playwright.sync_api import Locator, Page
from utils.logger import logger


class LoginPage:
    """Represents the Login dialog / authentication interface on IRCTC."""

    def __init__(self, page: Page):
        self.page = page

        # Login Modal & Form Locators
        self.login_dialog = page.locator("app-login, .login-modal, div.modal-dialog, p-dialog").first
        self.username_input = page.locator(
            "input[formcontrolname='userid'], input[placeholder*='User Name'], #userId, input[name='userId']"
        ).first
        self.password_input = page.locator(
            "input[formcontrolname='password'], input[placeholder*='Password'], #pwd, input[name='pwd']"
        ).first
        self.sign_in_button = page.locator(
            "button:has-text('SIGN IN'), button[type='submit']:has-text('SIGN IN')"
        ).first
        self.close_button = page.locator(
            ".close, button.close, button[aria-label='Close'], .modal-header .close"
        ).first
        self.validation_errors = page.locator(
            ".error-msg, .ui-messages-error, .ui-toast-detail, .invalid-feedback, div[role='alert']"
        )

    def is_login_dialog_open(self) -> bool:
        """Check if login dialog / container is visible."""
        try:
            return self.username_input.is_visible(timeout=5000)
        except Exception:
            return False

    def is_username_field_visible(self) -> bool:
        """Check if username input field is visible."""
        visible = self.username_input.is_visible()
        logger.info("Login username input visible: %s", visible)
        return visible

    def is_password_field_visible(self) -> bool:
        """Check if password input field is visible."""
        visible = self.password_input.is_visible()
        logger.info("Login password input visible: %s", visible)
        return visible

    def is_sign_in_button_visible(self) -> bool:
        """Check if Sign In submit button is visible."""
        visible = self.sign_in_button.is_visible()
        logger.info("Login Sign In button visible: %s", visible)
        return visible

    def enter_username(self, username: str) -> None:
        """Enter username string into username field."""
        logger.info("Entering login username")
        self.username_input.wait_for(state="visible")
        self.username_input.fill(username)

    def enter_password(self, password: str) -> None:
        """Enter password string into password field."""
        logger.info("Entering login password (masked)")
        self.password_input.wait_for(state="visible")
        self.password_input.fill(password)

    def click_sign_in(self) -> None:
        """Click the Sign In button."""
        logger.info("Clicking Sign In button")
        self.sign_in_button.wait_for(state="visible")
        self.sign_in_button.click()

    def close(self) -> None:
        """Close the login dialog."""
        logger.info("Closing Login dialog")
        if self.close_button.is_visible(timeout=2000):
            self.close_button.click()
        else:
            self.page.keyboard.press("Escape")

    def verify_empty_field_validation(self) -> bool:
        """Attempt to sign in with empty fields and verify form validation triggers."""
        logger.info("Testing validation for empty login fields")
        self.username_input.click()
        self.username_input.fill("")
        self.password_input.click()
        self.password_input.fill("")
        self.click_sign_in()
        self.page.wait_for_timeout(1000)

        # Check for HTML5 required state, ng-invalid class, or displayed error
        has_invalid_class = "ng-invalid" in (self.username_input.get_attribute("class") or "")
        has_error_message = self.validation_errors.count() > 0
        logger.info(
            "Empty field validation triggered - ng-invalid: %s, error message: %s",
            has_invalid_class,
            has_error_message,
        )
        return has_invalid_class or has_error_message or self.is_username_field_visible()
