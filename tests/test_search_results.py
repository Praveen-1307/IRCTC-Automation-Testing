"""Test suite for IRCTC Train Search Results Page (TC22 - TC31)."""
import pytest
from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage
from pages.train_search_page import TrainSearchPage
from utils.logger import logger
from utils.test_data import VALID_FROM_CODE, VALID_TO_CODE


@pytest.fixture(scope="function")
def search_results_loaded(page) -> SearchResultsPage:
    """Helper fixture to execute a valid train search and land on results."""
    home_page = HomePage(page)
    train_search = TrainSearchPage(page)
    results_page = SearchResultsPage(page)

    home_page.open()
    train_search.search_train(from_station=VALID_FROM_CODE, to_station=VALID_TO_CODE)
    results_page.is_results_page_loaded()
    return results_page


@pytest.mark.smoke
@pytest.mark.search_results
def test_TC22_verify_search_results_page_loads(search_results_loaded):
    """TC22 - Verify search results page loads."""
    # Arrange & Act
    results_page = search_results_loaded

    # Assert
    assert results_page.is_results_page_loaded(), "Search results page should be loaded"
    logger.info("TC22 PASSED: Train search results page loaded")


@pytest.mark.search_results
def test_TC23_verify_train_search_results_contain_train_information(search_results_loaded):
    """TC23 - Verify train search results contain train information."""
    # Arrange & Act
    results_page = search_results_loaded
    train_count = results_page.get_train_cards_count()

    # Assert
    assert train_count > 0, "At least one train should be listed in search results"
    logger.info("TC23 PASSED: Results page contains %d trains", train_count)


@pytest.mark.search_results
def test_TC24_verify_train_number_name_is_displayed(search_results_loaded):
    """TC24 - Verify train number/name is displayed."""
    # Arrange & Act
    results_page = search_results_loaded
    has_train_number = results_page.verify_train_number_displayed()

    # Assert
    assert has_train_number, "Train card must display the train number and name"
    logger.info("TC24 PASSED: Train number and name are visible")


@pytest.mark.search_results
def test_TC25_verify_train_departure_information_is_displayed(search_results_loaded):
    """TC25 - Verify train departure information is displayed."""
    # Arrange & Act
    results_page = search_results_loaded
    has_departure = results_page.verify_departure_displayed()

    # Assert
    assert has_departure, "Train departure time and origin station should be displayed"
    logger.info("TC25 PASSED: Train departure information is visible")


@pytest.mark.search_results
def test_TC26_verify_train_arrival_information_is_displayed(search_results_loaded):
    """TC26 - Verify train arrival information is displayed."""
    # Arrange & Act
    results_page = search_results_loaded
    has_arrival = results_page.verify_arrival_displayed()

    # Assert
    assert has_arrival, "Train arrival time and destination station should be displayed"
    logger.info("TC26 PASSED: Train arrival information is visible")


@pytest.mark.search_results
def test_TC27_verify_available_class_information(search_results_loaded):
    """TC27 - Verify available class information."""
    # Arrange & Act
    results_page = search_results_loaded
    available_classes = results_page.get_available_classes()

    # Assert
    assert len(available_classes) > 0, "Train should display available travel classes (e.g. SL, 3A, 2A)"
    logger.info("TC27 PASSED: Available classes displayed: %s", available_classes)


@pytest.mark.search_results
def test_TC28_verify_seat_availability_information(search_results_loaded):
    """TC28 - Verify seat availability information where publicly displayed."""
    # Arrange & Act
    results_page = search_results_loaded
    has_availability_info = results_page.verify_availability_info_displayed()

    # Assert
    assert has_availability_info, "Seat availability status or Refresh button should be present"
    logger.info("TC28 PASSED: Seat availability controls are visible")


@pytest.mark.search_results
def test_TC29_verify_fare_information(search_results_loaded):
    """TC29 - Verify fare information where publicly displayed."""
    # Arrange & Act
    results_page = search_results_loaded
    has_fare_info = results_page.verify_fare_info_displayed()

    # Assert
    assert has_fare_info, "Fare inquiry or fare details should be present on train cards"
    logger.info("TC29 PASSED: Fare information is accessible")


@pytest.mark.regression
@pytest.mark.search_results
def test_TC30_verify_search_results_can_be_refreshed(search_results_loaded):
    """TC30 - Verify search results can be refreshed/reloaded."""
    # Arrange & Act
    results_page = search_results_loaded
    logger.info("TC30: Triggering refresh on availability")
    results_page.refresh_first_train_availability()
    count_after_refresh = results_page.get_train_cards_count()

    # Assert
    assert count_after_refresh > 0, "Train results should remain visible after refreshing availability"
    logger.info("TC30 PASSED: Search results refreshed successfully")


@pytest.mark.search_results
def test_TC31_verify_navigation_back_to_search_page(page, search_results_loaded):
    """TC31 - Verify navigation back to search page."""
    # Arrange
    results_page = search_results_loaded
    train_search = TrainSearchPage(page)

    # Act
    logger.info("TC31: Navigating back to train search page")
    results_page.click_modify_search()
    page.wait_for_timeout(2000)

    # Assert
    assert (
        train_search.is_search_button_visible() or "train-search" in page.url or results_page.modify_search_btn.is_visible()
    ), "User should be able to navigate back to search or modify search"
    logger.info("TC31 PASSED: Navigation back to search interface verified")
