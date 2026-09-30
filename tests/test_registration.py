"""Test suite for IRCTC User Registration Interface and Validations (TC35 - TC37)."""
import pytest
from pages.registration_page import RegistrationPage
from utils.logger import logger


@pytest.mark.smoke
@pytest.mark.registration
def test_TC35_verify_registration_page_opens(page):
    """TC35 - Verify registration page opens."""
    # Arrange
    reg_page = RegistrationPage(page)

    # Act
    logger.info("TC35: Opening IRCTC registration page")
    reg_page.open()

    # Assert
    assert reg_page.is_registration_page_loaded(), "Registration page should open and load"
    logger.info("TC35 PASSED: Registration page loaded successfully")


@pytest.mark.registration
def test_TC36_verify_registration_form_fields_are_displayed(page):
    """TC36 - Verify registration form fields are displayed."""
    # Arrange
    reg_page = RegistrationPage(page)

    # Act
    logger.info("TC36: Checking registration form fields")
    reg_page.open()
    field_status = reg_page.are_core_fields_visible()

    # Assert
    assert field_status["username"], "User Name field must be visible"
    assert field_status["password"], "Password field must be visible"
    assert field_status["email"], "Email field must be visible"
    logger.info("TC36 PASSED: Core registration fields are displayed: %s", field_status)


@pytest.mark.regression
@pytest.mark.registration
def test_TC37_verify_registration_form_validation_for_required_fields(page):
    """TC37 - Verify registration form validation for required fields."""
    # Arrange
    reg_page = RegistrationPage(page)

    # Act
    logger.info("TC37: Verifying required field validation triggers")
    reg_page.open()
    is_validated = reg_page.verify_required_field_validation()

    # Assert
    assert is_validated, "Leaving required fields empty should trigger validation"
    logger.info("TC37 PASSED: Required fields validation verified")
