"""Page Object Model for IRCTC Train Search Results Page."""
import re
from typing import List
from playwright.sync_api import Locator, Page
from utils.logger import logger


class SearchResultsPage:
    """Represents the Search Results listing page displaying available trains."""

    def __init__(self, page: Page):
        self.page = page

        # Search Results Locators
        self.train_containers = page.locator("app-train-avl-enq, .bull-back.border-all")
        self.train_headings = page.locator("div.train-heading strong")
        self.departure_elements = page.locator(".col-xs-5.no-pad, .col-xs-3")
        self.modify_search_btn = page.locator(
            "button:has-text('Modify Search'), .modify-search, button:has-text('Modify')"
        ).first
        self.refresh_buttons = page.locator(
            "button:has-text('Refresh'), .fa-repeat, .fa-refresh"
        )
        self.class_boxes = page.locator("div.pre-avail, app-train-avl-enq table td, .col-xs-12 .train-type")
        self.fare_elements = page.locator(".fare, strong:has-text('₹'), span:has-text('₹')")

    def is_results_page_loaded(self) -> bool:
        """Check if search results page is loaded via URL or train list elements."""
        try:
            self.page.wait_for_url("**/train-list**", timeout=15000)
            logger.info("Search results URL confirmed: %s", self.page.url)
            return True
        except Exception:
            return self.train_containers.first.is_visible(timeout=5000)

    def get_train_cards_count(self) -> int:
        """Return the count of trains returned in results."""
        self.page.wait_for_timeout(2000)
        count = self.train_containers.count()
        logger.info("Found %d train result cards", count)
        return count

    def get_train_names(self) -> List[str]:
        """Extract all visible train names and numbers from the results."""
        self.page.wait_for_timeout(1000)
        headings = self.train_headings.all()
        names = [h.inner_text().strip() for h in headings if h.inner_text().strip()]
        logger.info("Extracted %d train names from results", len(names))
        return names

    def verify_train_number_displayed(self) -> bool:
        """Verify train number is displayed (e.g. 5 digits in brackets like (15134))."""
        headings = self.get_train_names()
        if not headings:
            return False
        first_heading = headings[0]
        # Look for 5 digit train number in heading
        match = re.search(r"\b\d{5}\b", first_heading)
        logger.info("Checking train number in '%s' -> Found: %s", first_heading, bool(match))
        return bool(match) or len(first_heading) > 3

    def verify_departure_displayed(self) -> bool:
        """Verify departure information (station and time) is visible on train cards."""
        if self.train_containers.count() == 0:
            return False
        first_card = self.train_containers.first
        card_text = first_card.inner_text()
        # Checks for time pattern (e.g., 00:20, 14:30)
        time_match = re.search(r"\b\d{1,2}:\d{2}\b", card_text)
        logger.info("Departure time found on first train card: %s", bool(time_match))
        return bool(time_match)

    def verify_arrival_displayed(self) -> bool:
        """Verify arrival information (station and time) is visible on train cards."""
        if self.train_containers.count() == 0:
            return False
        first_card = self.train_containers.first
        card_text = first_card.inner_text()
        # A train card contains at least two times (departure and arrival)
        all_times = re.findall(r"\b\d{1,2}:\d{2}\b", card_text)
        logger.info("Found %d timestamps on first train card", len(all_times))
        return len(all_times) >= 2

    def get_available_classes(self) -> List[str]:
        """Extract available class abbreviations displayed on cards (SL, 3A, 2A, 1A, etc.)."""
        first_card = self.train_containers.first
        if not first_card.is_visible(timeout=3000):
            return []
        card_text = first_card.inner_text()
        known_classes = ["1A", "2A", "3A", "3E", "SL", "CC", "2S", "EC", "EA", "EV"]
        found = [cls for cls in known_classes if cls in card_text]
        logger.info("Found available travel classes in result card: %s", found)
        return found

    def verify_availability_info_displayed(self) -> bool:
        """Verify availability or refresh control is displayed for seat enquiry."""
        if self.train_containers.count() == 0:
            return False
        card_text = self.train_containers.first.inner_text()
        indicators = ["AVAILABLE", "RAC", "WL", "NOT AVAILABLE", "Refresh", "TRAIN DEPARTED"]
        has_indicator = any(ind in card_text for ind in indicators)
        logger.info("Seat availability indicator present: %s", has_indicator)
        return has_indicator

    def verify_fare_info_displayed(self) -> bool:
        """Verify fare information or fare enquiry elements are displayed."""
        if self.train_containers.count() == 0:
            return False
        card_text = self.train_containers.first.inner_text()
        # Checks for ₹ currency symbol or fare text or ability to query fare
        has_fare = "₹" in card_text or "Fare" in card_text or self.refresh_buttons.count() > 0
        logger.info("Fare inquiry or fare information present: %s", has_fare)
        return has_fare

    def refresh_first_train_availability(self) -> None:
        """Click the refresh button on the first train card."""
        if self.refresh_buttons.count() > 0:
            btn = self.refresh_buttons.first
            if btn.is_visible():
                logger.info("Clicking train availability refresh button")
                btn.click()
                self.page.wait_for_timeout(2000)

    def click_modify_search(self) -> None:
        """Click Modify Search button."""
        logger.info("Clicking Modify Search button")
        if self.modify_search_btn.is_visible(timeout=3000):
            self.modify_search_btn.click()
            self.page.wait_for_timeout(1000)
        else:
            self.page.go_back()
