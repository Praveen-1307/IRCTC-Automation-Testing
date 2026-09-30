"""Page Object Model (POM) classes for IRCTC website."""
from pages.home_page import HomePage
from pages.train_search_page import TrainSearchPage
from pages.search_results_page import SearchResultsPage
from pages.login_page import LoginPage
from pages.registration_page import RegistrationPage

__all__ = [
    "HomePage",
    "TrainSearchPage",
    "SearchResultsPage",
    "LoginPage",
    "RegistrationPage",
]
