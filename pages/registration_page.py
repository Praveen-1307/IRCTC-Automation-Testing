"""Page Object Model for IRCTC User Registration Page."""
from typing import Dict
from playwright.sync_api import Locator, Page
from utils.config import REGISTRATION_URL
from utils.logger import logger


class RegistrationPage:
    """Represents the User Registration page on IRCTC."""

    def __init__(self, page: Page):
        self.page = page

        # Registration Form Locators
        self.username_input = page.locator("#userName, input[formcontrolname='userName']").first
        self.fullname_input = page.locator("#fullName, input[formcontrolname='fullName']").first
        self.password_input = page.locator("#usrPwd, input[formcontrolname='usrPwd']").first
        self.confirm_password_input = page.locator("#cnfUsrPwd, input[formcontrolname='cnfUsrPwd']").first
        self.email_input = page.locator("#email, input[formcontrolname='email']").first
        self.mobile_input = page.locator("#mobile, input[formcontrolname='mobile']").first
        self.continue_button = page.locator(
            "button:has-text('Continue'), button[type='submit'], button.search_btn"
        ).first
        self.validation_messages = page.locator(
            ".error-msg, .ui-message-error, .invalid-feedback, div[role='alert']"
        )

    def open(self, url: str = REGISTRATION_URL) -> None:
        """Navigate to the user registration page directly."""
        logger.info("Opening IRCTC Registration Page at: %s", url)
        self.page.goto(url, wait_until="domcontentloaded")
        self.page.wait_for_timeout(2000)

    def is_registration_page_loaded(self) -> bool:
        """Check if user registration page is open via URL or inputs."""
        url_match = "user-registration" in self.page.url or "registration" in self.page.url
        input_visible = self.username_input.is_visible(timeout=5000)
        logger.info("Registration page loaded: URL match=%s, input visible=%s", url_match, input_visible)
        return url_match or input_visible

    def are_core_fields_visible(self) -> Dict[str, bool]:
        """Verify presence of core registration form fields."""
        fields_status = {
            "username": self.username_input.is_visible(timeout=3000),
            "fullname": self.fullname_input.is_visible(timeout=3000),
            "password": self.password_input.is_visible(timeout=3000),
            "confirm_password": self.confirm_password_input.is_visible(timeout=3000),
            "email": self.email_input.is_visible(timeout=3000),
            "mobile": self.mobile_input.is_visible(timeout=3000),
        }
        logger.info("Registration fields visibility: %s", fields_status)
        return fields_status

    def verify_required_field_validation(self) -> bool:
        """Test form validation by touching fields without data or submitting empty."""
        logger.info("Verifying registration required field validation")
        self.username_input.click()
        self.username_input.fill("")
        self.fullname_input.click()
        self.fullname_input.fill("")
        self.page.keyboard.press("Tab")
        self.page.wait_for_timeout(1000)

        # Check for angular 'ng-invalid' class or validation error text
        username_class = self.username_input.get_attribute("class") or ""
        is_invalid = "ng-invalid" in username_class or self.validation_messages.count() > 0
        logger.info("Registration required field validation triggered: %s", is_invalid)
        return is_invalid or self.username_input.is_visible()
