"""Page Object Model for IRCTC Train Search widget and controls."""
from typing import List
from playwright.sync_api import Locator, Page
from utils.logger import logger


class TrainSearchPage:
    """Encapsulates the Train Search Form on IRCTC."""

    def __init__(self, page: Page):
        self.page = page

        # Search Form Locators
        self.from_input = page.locator("#origin input, p-autocomplete#origin input").first
        self.to_input = page.locator("#destination input, p-autocomplete#destination input").first
        self.date_input = page.locator("p-calendar input, .ui-calendar input").first
        self.quota_dropdown = page.locator("#journeyQuota, p-dropdown#journeyQuota").first
        self.class_dropdown = page.locator("#journeyClass, p-dropdown#journeyClass").first
        self.search_button = page.locator(
            "button.search_btn, button[type='submit']:has-text('Search'), button:has-text('Search Trains')"
        ).first
        self.autocomplete_list = page.locator("ul[role='listbox'] li, .ui-autocomplete-items li")
        self.dropdown_items = page.locator(
            "p-dropdownItem li, .ui-dropdown-items li, ul[role='listbox'] li"
        )
        self.error_toast = page.locator(
            ".ui-toast-message, .ui-messages, .alert-danger, .error-msg, div[role='alert']"
        ).first

    def is_from_station_visible(self) -> bool:
        """Check if From station input is visible."""
        visible = self.from_input.is_visible()
        logger.info("From station input visible: %s", visible)
        return visible

    def is_to_station_visible(self) -> bool:
        """Check if To station input is visible."""
        visible = self.to_input.is_visible()
        logger.info("To station input visible: %s", visible)
        return visible

    def is_journey_date_visible(self) -> bool:
        """Check if journey date input is visible."""
        visible = self.date_input.is_visible()
        logger.info("Journey date input visible: %s", visible)
        return visible

    def is_quota_visible(self) -> bool:
        """Check if journey quota control is visible."""
        visible = self.quota_dropdown.is_visible()
        logger.info("Journey quota dropdown visible: %s", visible)
        return visible

    def is_class_visible(self) -> bool:
        """Check if journey class control is visible."""
        visible = self.class_dropdown.is_visible()
        logger.info("Journey class dropdown visible: %s", visible)
        return visible

    def is_search_button_visible(self) -> bool:
        """Check if search button is visible."""
        visible = self.search_button.is_visible()
        logger.info("Search button visible: %s", visible)
        return visible

    def enter_from_station(self, station: str) -> None:
        """Enter station name or code in From input."""
        logger.info("Entering From station: '%s'", station)
        self.from_input.wait_for(state="visible")
        self.from_input.click()
        self.from_input.fill("")
        self.from_input.fill(station)
        # Give autocomplete suggestions time to populate
        self.page.wait_for_timeout(1000)

    def enter_to_station(self, station: str) -> None:
        """Enter station name or code in To input."""
        logger.info("Entering To station: '%s'", station)
        self.to_input.wait_for(state="visible")
        self.to_input.click()
        self.to_input.fill("")
        self.to_input.fill(station)
        # Give autocomplete suggestions time to populate
        self.page.wait_for_timeout(1000)

    def get_from_autocomplete_suggestions(self) -> List[str]:
        """Fetch visible suggestions in the From station dropdown."""
        self.page.wait_for_timeout(1000)
        items = self.autocomplete_list.all()
        texts = [i.inner_text().strip() for i in items if i.inner_text().strip()]
        logger.info("Fetched %d autocomplete suggestions for From station", len(texts))
        return texts

    def get_to_autocomplete_suggestions(self) -> List[str]:
        """Fetch visible suggestions in the To station dropdown."""
        self.page.wait_for_timeout(1000)
        items = self.autocomplete_list.all()
        texts = [i.inner_text().strip() for i in items if i.inner_text().strip()]
        logger.info("Fetched %d autocomplete suggestions for To station", len(texts))
        return texts

    def select_from_station(self, station_code: str) -> None:
        """Type station code and click matching autocomplete suggestion."""
        self.enter_from_station(station_code)
        suggestion = self.page.locator(
            f"ul[role='listbox'] li:has-text('{station_code}')"
        ).first
        if suggestion.is_visible(timeout=3000):
            suggestion.click()
            logger.info("Selected From station option containing: '%s'", station_code)
        else:
            # Fallback to pressing Enter or selecting first item
            first_item = self.autocomplete_list.first
            if first_item.is_visible(timeout=1000):
                first_item.click()
        self.page.wait_for_timeout(500)

    def select_to_station(self, station_code: str) -> None:
        """Type station code and click matching autocomplete suggestion."""
        self.enter_to_station(station_code)
        suggestion = self.page.locator(
            f"ul[role='listbox'] li:has-text('{station_code}')"
        ).first
        if suggestion.is_visible(timeout=3000):
            suggestion.click()
            logger.info("Selected To station option containing: '%s'", station_code)
        else:
            # Fallback to first item
            first_item = self.autocomplete_list.first
            if first_item.is_visible(timeout=1000):
                first_item.click()
        self.page.wait_for_timeout(500)

    def set_journey_date(self, date_str: str) -> None:
        """Input travel date in DD/MM/YYYY format."""
        logger.info("Setting journey date: %s", date_str)
        self.date_input.wait_for(state="visible")
        self.date_input.click()
        self.date_input.press("Control+A")
        self.date_input.press("Backspace")
        self.date_input.fill(date_str)
        self.date_input.press("Escape")
        self.page.wait_for_timeout(500)

    def get_selected_journey_date(self) -> str:
        """Return the current value inside the journey date input."""
        val = self.date_input.input_value()
        logger.info("Current journey date value: '%s'", val)
        return val

    def get_quota_options(self) -> List[str]:
        """Click quota dropdown and return all available quota labels."""
        self.quota_dropdown.click()
        self.page.wait_for_timeout(500)
        items = self.page.locator(
            "p-dropdown#journeyQuota li, ul[role='listbox'] li"
        ).all()
        options = [i.inner_text().strip() for i in items if i.inner_text().strip()]
        logger.info("Retrieved %d quota options", len(options))
        # Close dropdown
        self.page.keyboard.press("Escape")
        return options

    def select_quota(self, quota_name: str) -> None:
        """Select a quota by name."""
        logger.info("Selecting quota: '%s'", quota_name)
        self.quota_dropdown.click()
        self.page.wait_for_timeout(500)
        option = self.page.locator(
            f"p-dropdown#journeyQuota li:has-text('{quota_name}'), ul[role='listbox'] li:has-text('{quota_name}')"
        ).first
        if option.is_visible(timeout=2000):
            option.click()
        else:
            self.page.keyboard.press("Escape")

    def get_class_options(self) -> List[str]:
        """Click class dropdown and return all available travel class options."""
        self.class_dropdown.click()
        self.page.wait_for_timeout(500)
        items = self.page.locator(
            "p-dropdown#journeyClass li, ul[role='listbox'] li"
        ).all()
        options = [i.inner_text().strip() for i in items if i.inner_text().strip()]
        logger.info("Retrieved %d class options", len(options))
        # Close dropdown
        self.page.keyboard.press("Escape")
        return options

    def click_search(self) -> None:
        """Click the Search button."""
        logger.info("Clicking train search button")
        self.search_button.wait_for(state="visible")
        self.search_button.click()

    def search_train(
        self,
        from_station: str,
        to_station: str,
        date_str: str = None,
        quota: str = None,
    ) -> None:
        """Perform complete train search flow."""
        self.select_from_station(from_station)
        self.select_to_station(to_station)
        if date_str:
            self.set_journey_date(date_str)
        if quota:
            self.select_quota(quota)
        self.click_search()

    def is_error_toast_displayed(self) -> bool:
        """Check if an error notification toast is displayed on the page."""
        try:
            return self.error_toast.is_visible(timeout=3000)
        except Exception:
            return False

    def get_error_message(self) -> str:
        """Get the text of the displayed validation error/toast."""
        if self.is_error_toast_displayed():
            text = self.error_toast.inner_text().strip()
            logger.info("Captured error message: '%s'", text)
            return text
        return ""
