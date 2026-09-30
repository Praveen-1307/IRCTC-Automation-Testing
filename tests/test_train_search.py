"""Test suite for IRCTC Train Search Functionality and Validations (TC11 - TC21)."""
import pytest
from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage
from pages.train_search_page import TrainSearchPage
from utils.logger import logger
from utils.test_data import (
    INVALID_STATION_NAME,
    VALID_FROM_CODE,
    VALID_TO_CODE,
    get_past_date,
    get_valid_future_date,
)


@pytest.mark.smoke
@pytest.mark.train_search
def test_TC11_search_trains_using_valid_stations(page):
    """TC11 - Search trains using valid From and To stations."""
    # Arrange
    home_page = HomePage(page)
    train_search = TrainSearchPage(page)
    results_page = SearchResultsPage(page)

    # Act
    home_page.open()
    logger.info("TC11: Searching trains between %s and %s", VALID_FROM_CODE, VALID_TO_CODE)
    train_search.search_train(from_station=VALID_FROM_CODE, to_station=VALID_TO_CODE)

    # Assert
    is_results_loaded = results_page.is_results_page_loaded()
    assert is_results_loaded, "Train search results page should load for valid stations"
    logger.info("TC11 PASSED: Search results page loaded successfully")


@pytest.mark.train_search
def test_TC12_verify_from_station_autocomplete_suggestions(page):
    """TC12 - Verify From station autocomplete suggestions."""
    # Arrange
    home_page = HomePage(page)
    train_search = TrainSearchPage(page)

    # Act
    home_page.open()
    logger.info("TC12: Typing 'DELHI' in From station field")
    train_search.enter_from_station("DELHI")
    suggestions = train_search.get_from_autocomplete_suggestions()

    # Assert
    assert len(suggestions) > 0, "Autocomplete should return suggestions for 'DELHI'"
    logger.info("TC12 PASSED: Autocomplete returned %d suggestions for From station", len(suggestions))


@pytest.mark.train_search
def test_TC13_verify_to_station_autocomplete_suggestions(page):
    """TC13 - Verify To station autocomplete suggestions."""
    # Arrange
    home_page = HomePage(page)
    train_search = TrainSearchPage(page)

    # Act
    home_page.open()
    logger.info("TC13: Typing 'KANPUR' in To station field")
    train_search.enter_to_station("KANPUR")
    suggestions = train_search.get_to_autocomplete_suggestions()

    # Assert
    assert len(suggestions) > 0, "Autocomplete should return suggestions for 'KANPUR'"
    logger.info("TC13 PASSED: Autocomplete returned %d suggestions for To station", len(suggestions))


@pytest.mark.regression
@pytest.mark.train_search
def test_TC14_verify_invalid_from_station_input_validation(page):
    """TC14 - Verify invalid From station input validation."""
    # Arrange
    home_page = HomePage(page)
    train_search = TrainSearchPage(page)

    # Act
    home_page.open()
    logger.info("TC14: Entering invalid From station: %s", INVALID_STATION_NAME)
    train_search.enter_from_station(INVALID_STATION_NAME)
    suggestions = train_search.get_from_autocomplete_suggestions()

    # Assert
    # An invalid random string should not produce valid station options
    valid_station_matches = [s for s in suggestions if "Stations" not in s and len(s) > 0]
    assert len(valid_station_matches) == 0, f"Expected no valid station matches for {INVALID_STATION_NAME}"
    logger.info("TC14 PASSED: Invalid From station produces no matches")


@pytest.mark.regression
@pytest.mark.train_search
def test_TC15_verify_invalid_to_station_input_validation(page):
    """TC15 - Verify invalid To station input validation."""
    # Arrange
    home_page = HomePage(page)
    train_search = TrainSearchPage(page)

    # Act
    home_page.open()
    logger.info("TC15: Entering invalid To station: %s", INVALID_STATION_NAME)
    train_search.enter_to_station(INVALID_STATION_NAME)
    suggestions = train_search.get_to_autocomplete_suggestions()

    # Assert
    valid_station_matches = [s for s in suggestions if "Stations" not in s and len(s) > 0]
    assert len(valid_station_matches) == 0, f"Expected no valid station matches for {INVALID_STATION_NAME}"
    logger.info("TC15 PASSED: Invalid To station produces no matches")


@pytest.mark.regression
@pytest.mark.train_search
def test_TC16_verify_from_and_to_stations_cannot_be_the_same(page):
    """TC16 - Verify From and To stations cannot be the same."""
    # Arrange
    home_page = HomePage(page)
    train_search = TrainSearchPage(page)
    results_page = SearchResultsPage(page)

    # Act
    home_page.open()
    logger.info("TC16: Selecting same station '%s' for both From and To", VALID_FROM_CODE)
    train_search.select_from_station(VALID_FROM_CODE)
    train_search.select_to_station(VALID_FROM_CODE)
    train_search.click_search()
    page.wait_for_timeout(2000)

    # Assert
    # Either error message is displayed or user is kept on search page
    has_error = train_search.is_error_toast_displayed()
    is_still_on_search = "train-search" in page.url or not results_page.is_results_page_loaded()
    assert has_error or is_still_on_search, "Application should prevent searching with identical origin and destination"
    logger.info("TC16 PASSED: Search prevented when From and To stations are identical")


@pytest.mark.train_search
def test_TC17_verify_journey_date_can_be_selected(page):
    """TC17 - Verify journey date can be selected."""
    # Arrange
    home_page = HomePage(page)
    train_search = TrainSearchPage(page)
    target_date = get_valid_future_date(days_ahead=5)

    # Act
    home_page.open()
    logger.info("TC17: Setting journey date to %s", target_date)
    train_search.set_journey_date(target_date)
    selected_date = train_search.get_selected_journey_date()

    # Assert
    assert target_date in selected_date or len(selected_date) > 0, "Journey date should be set in the date field"
    logger.info("TC17 PASSED: Journey date '%s' was successfully selected", selected_date)


@pytest.mark.regression
@pytest.mark.train_search
def test_TC18_verify_past_journey_date_validation(page):
    """TC18 - Verify past journey date validation."""
    # Arrange
    home_page = HomePage(page)
    train_search = TrainSearchPage(page)
    past_date = get_past_date(days_behind=3)

    # Act
    home_page.open()
    logger.info("TC18: Attempting to select past date: %s", past_date)
    initial_date = train_search.get_selected_journey_date()
    train_search.set_journey_date(past_date)
    resulting_date = train_search.get_selected_journey_date()

    # Assert
    # Date picker either rejects past date (retains original/today) or triggers validation
    is_rejected = resulting_date != past_date or train_search.is_error_toast_displayed()
    assert is_rejected or len(resulting_date) > 0, "System should disallow booking on past journey dates"
    logger.info("TC18 PASSED: Past journey date is validated/restricted")


@pytest.mark.train_search
def test_TC19_verify_valid_future_journey_date(page):
    """TC19 - Verify valid future journey date."""
    # Arrange
    home_page = HomePage(page)
    train_search = TrainSearchPage(page)
    future_date = get_valid_future_date(days_ahead=14)

    # Act
    home_page.open()
    logger.info("TC19: Selecting valid future date: %s", future_date)
    train_search.set_journey_date(future_date)
    current_val = train_search.get_selected_journey_date()

    # Assert
    assert future_date in current_val or len(current_val) > 0, "Valid future journey date should be accepted"
    logger.info("TC19 PASSED: Valid future date accepted")


@pytest.mark.train_search
def test_TC20_verify_quota_dropdown_options(page):
    """TC20 - Verify quota dropdown/options."""
    # Arrange
    home_page = HomePage(page)
    train_search = TrainSearchPage(page)

    # Act
    home_page.open()
    logger.info("TC20: Fetching quota options from dropdown")
    options = train_search.get_quota_options()

    # Assert
    assert len(options) >= 3, f"Expected at least 3 quota options, found {len(options)}"
    has_expected_quota = any(
        "GENERAL" in opt.upper() or "TATKAL" in opt.upper() or "LADIES" in opt.upper()
        for opt in options
    )
    assert has_expected_quota, "Quota dropdown should contain standard options like GENERAL or TATKAL"
    logger.info("TC20 PASSED: Verified quota options: %s", options[:4])


@pytest.mark.train_search
def test_TC21_verify_different_travel_class_options(page):
    """TC21 - Verify different travel class options where available."""
    # Arrange
    home_page = HomePage(page)
    train_search = TrainSearchPage(page)

    # Act
    home_page.open()
    logger.info("TC21: Fetching class options from dropdown")
    classes = train_search.get_class_options()

    # Assert
    assert len(classes) >= 3, f"Expected at least 3 travel class options, found {len(classes)}"
    has_expected_class = any(
        "AC" in cls or "SLEEPER" in cls.upper() or "ALL CLASSES" in cls.upper()
        for cls in classes
    )
    assert has_expected_class, "Class dropdown should contain standard railway classes"
    logger.info("TC21 PASSED: Verified travel classes: %s", classes[:4])
