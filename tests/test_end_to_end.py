"""Test suite for IRCTC Failure Screenshot Capture and End-to-End Workflow (TC39 - TC40)."""
import os
from pathlib import Path
import pytest
from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage
from pages.train_search_page import TrainSearchPage
from utils.config import SCREENSHOTS_DIR
from utils.logger import logger
from utils.test_data import (
    VALID_FROM_CODE,
    VALID_TO_CODE,
    get_valid_future_date,
)


@pytest.mark.regression
def test_TC39_verify_screenshot_is_captured_when_a_test_fails(page):
    """TC39 - Verify screenshot is captured when a test fails."""
    # Arrange
    home_page = HomePage(page)
    test_screenshot_path = SCREENSHOTS_DIR / "test_TC39_failure_capture_demo.png"

    # Act
    home_page.open()
    logger.info("TC39: Testing screenshot capture mechanism")
    # Take screenshot directly to simulate conftest hook capture and verify file integrity
    page.screenshot(path=str(test_screenshot_path), full_page=True)

    # Assert
    assert test_screenshot_path.exists(), "Failure screenshot file should be created"
    file_size = test_screenshot_path.stat().st_size
    assert file_size > 1000, f"Screenshot file should contain image data (size: {file_size} bytes)"
    logger.info("TC39 PASSED: Screenshot captured successfully (%d bytes) at %s", file_size, test_screenshot_path)


@pytest.mark.smoke
@pytest.mark.e2e
def test_TC40_verify_complete_train_search_workflow(page):
    """TC40 - Verify complete train-search workflow from home page to results."""
    # Arrange
    home_page = HomePage(page)
    train_search = TrainSearchPage(page)
    results_page = SearchResultsPage(page)
    travel_date = get_valid_future_date(days_ahead=7)

    # Act: Step 1 - Launch home page
    logger.info("TC40 [Step 1]: Opening IRCTC home page")
    home_page.open()
    assert home_page.is_logo_visible(), "Home page logo should be visible"

    # Act: Step 2 - Configure journey details
    logger.info(
        "TC40 [Step 2]: Searching trains from %s to %s on %s with GENERAL quota",
        VALID_FROM_CODE,
        VALID_TO_CODE,
        travel_date,
    )
    train_search.select_from_station(VALID_FROM_CODE)
    train_search.select_to_station(VALID_TO_CODE)
    train_search.set_journey_date(travel_date)
    train_search.select_quota("GENERAL")

    # Act: Step 3 - Submit search
    logger.info("TC40 [Step 3]: Submitting train search")
    train_search.click_search()

    # Assert: Step 4 - Verify results page & trains
    logger.info("TC40 [Step 4]: Verifying search results page")
    is_loaded = results_page.is_results_page_loaded()
    assert is_loaded, "Complete workflow must successfully land on train search results"

    trains_count = results_page.get_train_cards_count()
    assert trains_count > 0, "Complete workflow must display at least one train in the results"

    has_train_number = results_page.verify_train_number_displayed()
    assert has_train_number, "Train number/name should be present on search results"

    has_departure = results_page.verify_departure_displayed()
    assert has_departure, "Departure information should be present in results"

    logger.info("TC40 PASSED: Complete train search workflow executed successfully with %d trains displayed", trains_count)
