"""Test suite for IRCTC Home Page UI and Launch Verifications (TC01 - TC10, TC38)."""
import pytest
from pages.home_page import HomePage
from pages.train_search_page import TrainSearchPage
from utils.logger import logger


@pytest.mark.smoke
def test_TC01_verify_irctc_website_launches(page):
    """TC01 - Verify IRCTC website launches successfully."""
    # Arrange
    home_page = HomePage(page)

    # Act
    logger.info("TC01: Launching IRCTC website")
    home_page.open()
    current_url = home_page.get_current_url()

    # Assert
    assert "irctc.co.in" in current_url, f"Expected irctc.co.in in URL, got {current_url}"
    logger.info("TC01 PASSED: Website launched successfully at %s", current_url)


@pytest.mark.smoke
def test_TC02_verify_irctc_home_page_title(page):
    """TC02 - Verify IRCTC home page title."""
    # Arrange
    home_page = HomePage(page)

    # Act
    logger.info("TC02: Checking IRCTC home page title")
    home_page.open()
    title = home_page.get_title()

    # Assert
    assert "IRCTC" in title, f"Expected 'IRCTC' in title, got '{title}'"
    logger.info("TC02 PASSED: Verified title contains 'IRCTC': %s", title)


@pytest.mark.smoke
def test_TC03_verify_irctc_logo_is_displayed(page):
    """TC03 - Verify IRCTC logo is displayed."""
    # Arrange
    home_page = HomePage(page)

    # Act
    logger.info("TC03: Checking IRCTC logo visibility")
    home_page.open()
    is_logo_present = home_page.is_logo_visible()

    # Assert
    assert is_logo_present, "IRCTC logo should be visible in the header"
    logger.info("TC03 PASSED: IRCTC logo is displayed")


@pytest.mark.smoke
def test_TC04_verify_main_navigation_is_displayed(page):
    """TC04 - Verify main navigation/menu is displayed."""
    # Arrange
    home_page = HomePage(page)

    # Act
    logger.info("TC04: Checking main navigation menu visibility")
    home_page.open()
    is_nav_visible = home_page.is_nav_menu_visible()

    # Assert
    assert is_nav_visible, "Main navigation menu should be visible"
    logger.info("TC04 PASSED: Main navigation menu is displayed")


@pytest.mark.smoke
@pytest.mark.train_search
def test_TC05_verify_from_station_field_is_visible(page):
    """TC05 - Verify From station field is visible."""
    # Arrange
    home_page = HomePage(page)
    train_search = TrainSearchPage(page)

    # Act
    logger.info("TC05: Checking From station input field")
    home_page.open()
    is_from_visible = train_search.is_from_station_visible()

    # Assert
    assert is_from_visible, "From station input field should be visible on the home page"
    logger.info("TC05 PASSED: From station field is visible")


@pytest.mark.smoke
@pytest.mark.train_search
def test_TC06_verify_to_station_field_is_visible(page):
    """TC06 - Verify To station field is visible."""
    # Arrange
    home_page = HomePage(page)
    train_search = TrainSearchPage(page)

    # Act
    logger.info("TC06: Checking To station input field")
    home_page.open()
    is_to_visible = train_search.is_to_station_visible()

    # Assert
    assert is_to_visible, "To station input field should be visible on the home page"
    logger.info("TC06 PASSED: To station field is visible")


@pytest.mark.train_search
def test_TC07_verify_journey_date_field_is_visible(page):
    """TC07 - Verify journey date field is visible."""
    # Arrange
    home_page = HomePage(page)
    train_search = TrainSearchPage(page)

    # Act
    logger.info("TC07: Checking journey date input field")
    home_page.open()
    is_date_visible = train_search.is_journey_date_visible()

    # Assert
    assert is_date_visible, "Journey date input field should be visible"
    logger.info("TC07 PASSED: Journey date field is visible")


@pytest.mark.train_search
def test_TC08_verify_class_preference_controls_are_displayed(page):
    """TC08 - Verify class/berth preference controls are displayed."""
    # Arrange
    home_page = HomePage(page)
    train_search = TrainSearchPage(page)

    # Act
    logger.info("TC08: Checking class preference dropdown")
    home_page.open()
    is_class_visible = train_search.is_class_visible()

    # Assert
    assert is_class_visible, "Journey class dropdown should be displayed"
    logger.info("TC08 PASSED: Class preference control is displayed")


@pytest.mark.train_search
def test_TC09_verify_quota_option_is_displayed(page):
    """TC09 - Verify quota option is displayed."""
    # Arrange
    home_page = HomePage(page)
    train_search = TrainSearchPage(page)

    # Act
    logger.info("TC09: Checking quota dropdown")
    home_page.open()
    is_quota_visible = train_search.is_quota_visible()

    # Assert
    assert is_quota_visible, "Journey quota dropdown should be displayed"
    logger.info("TC09 PASSED: Quota option is displayed")


@pytest.mark.smoke
@pytest.mark.train_search
def test_TC10_verify_search_button_is_displayed(page):
    """TC10 - Verify Search button is displayed."""
    # Arrange
    home_page = HomePage(page)
    train_search = TrainSearchPage(page)

    # Act
    logger.info("TC10: Checking search button")
    home_page.open()
    is_search_btn_visible = train_search.is_search_button_visible()

    # Assert
    assert is_search_btn_visible, "Search button should be displayed"
    logger.info("TC10 PASSED: Search button is displayed")


@pytest.mark.regression
def test_TC38_verify_browser_refresh_behavior(page):
    """TC38 - Verify browser refresh behavior."""
    # Arrange
    home_page = HomePage(page)
    train_search = TrainSearchPage(page)

    # Act
    logger.info("TC38: Testing page refresh behavior")
    home_page.open()
    home_page.refresh()
    title = home_page.get_title()
    is_form_visible = train_search.is_from_station_visible()

    # Assert
    assert "IRCTC" in title, "Page title should remain intact after refresh"
    assert is_form_visible, "Search form should remain visible after browser refresh"
    logger.info("TC38 PASSED: Browser refresh maintained expected page state")


def test_homepage_dismisses_english_language_prompt_when_rendered_as_link():
    """Language popup should be dismissed even when English is rendered as a link instead of a button."""

    class FakeLocator:
        def __init__(self, selector, visible=False):
            self.selector = selector
            self.visible = visible
            self.first = self

        def is_visible(self, timeout=0):
            return self.visible

        def click(self, **kwargs):
            self.was_clicked = True
            return None

    class FakePage:
        def __init__(self):
            self.clicks = []
            self.locator_map = {
                "a:has-text('English')": FakeLocator("a:has-text('English')", True),
                "button:has-text('English'), button:has-text('OK'), .btn-primary:has-text('OK'), button:has-text('Ok')": FakeLocator(
                    "button:has-text('English'), button:has-text('OK'), .btn-primary:has-text('OK'), button:has-text('Ok')",
                    False,
                ),
            }

        def locator(self, selector):
            return self.locator_map.get(selector, FakeLocator(selector, False))

        def wait_for_timeout(self, timeout):
            return None

    page = FakePage()
    home_page = HomePage(page)

    home_page.dismiss_advisories()

    assert page.locator_map["a:has-text('English')"].was_clicked is True
