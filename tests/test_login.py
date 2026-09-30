"""Test suite for IRCTC Login Modal and Field Validations (TC32 - TC34)."""
import pytest
from pages.home_page import HomePage
from pages.login_page import LoginPage
from utils.logger import logger


@pytest.mark.smoke
@pytest.mark.login
def test_TC32_verify_login_page_opens(page):
    """TC32 - Verify login page opens."""
    # Arrange
    home_page = HomePage(page)
    login_page = LoginPage(page)

    # Act
    home_page.open()
    logger.info("TC32: Opening Login modal/dialog")
    home_page.open_login()

    # Assert
    assert login_page.is_login_dialog_open(), "Login modal or container should open"
    logger.info("TC32 PASSED: Login modal opened successfully")


@pytest.mark.login
def test_TC33_verify_login_fields_are_displayed(page):
    """TC33 - Verify login fields are displayed."""
    # Arrange
    home_page = HomePage(page)
    login_page = LoginPage(page)

    # Act
    home_page.open()
    home_page.open_login()

    # Assert
    assert login_page.is_username_field_visible(), "Username input field should be visible"
    assert login_page.is_password_field_visible(), "Password input field should be visible"
    assert login_page.is_sign_in_button_visible(), "Sign In button should be visible"
    logger.info("TC33 PASSED: All login form fields are displayed")


@pytest.mark.regression
@pytest.mark.login
def test_TC34_verify_login_validation_for_empty_fields(page):
    """TC34 - Verify login validation for empty fields."""
    # Arrange
    home_page = HomePage(page)
    login_page = LoginPage(page)

    # Act
    home_page.open()
    home_page.open_login()
    validation_triggered = login_page.verify_empty_field_validation()

    # Assert
    assert validation_triggered, "Submitting empty credentials should trigger field validation"
    logger.info("TC34 PASSED: Empty fields validation verified")
