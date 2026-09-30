"""Test data constants and generators for IRCTC automation test cases."""
from datetime import datetime, timedelta

# Valid Indian Railway Station codes and labels
VALID_FROM_CODE = "NDLS"
VALID_FROM_NAME = "NEW DELHI - NDLS"

VALID_TO_CODE = "CNB"
VALID_TO_NAME = "KANPUR CENTRAL - CNB"

CHENNAI_STATION_CODE = "MAS"
CHENNAI_STATION_NAME = "MGR CHENNAI CTL - MAS"

BANGALORE_STATION_CODE = "SBC"
BANGALORE_STATION_NAME = "KSR BENGALURU - SBC"

# Invalid Station names for negative test cases
INVALID_STATION_NAME = "INVALID_STATION_NAME_XYZ"
INVALID_SPECIAL_CHARS = "!@#$%^"
NUMERIC_STATION_INPUT = "123456"

# Quota Options available on IRCTC
QUOTA_OPTIONS = [
    "GENERAL",
    "LADIES",
    "LOWER BERTH/SR.CITIZEN",
    "PERSON WITH DISABILITY",
    "DUTY PASS",
    "TATKAL",
    "PREMIUM TATKAL",
]

# Travel Class Options available on IRCTC
TRAVEL_CLASSES = [
    "All Classes",
    "AC First Class (1A)",
    "AC 2 Tier (2A)",
    "AC 3 Tier (3A)",
    "AC 3 Economy (3E)",
    "AC Chair car (CC)",
    "Sleeper (SL)",
    "Second Sitting (2S)",
]

# Journey date helpers
def get_valid_future_date(days_ahead: int = 7) -> str:
    """Return a formatted future date string (DD/MM/YYYY) suitable for IRCTC input."""
    target_date = datetime.now() + timedelta(days=days_ahead)
    return target_date.strftime("%d/%m/%Y")


def get_past_date(days_behind: int = 2) -> str:
    """Return a formatted past date string (DD/MM/YYYY) suitable for negative testing."""
    target_date = datetime.now() - timedelta(days=days_behind)
    return target_date.strftime("%d/%m/%Y")


def get_today_date() -> str:
    """Return today's date formatted as DD/MM/YYYY."""
    return datetime.now().strftime("%d/%m/%Y")


# Test Credentials for safe non-transactional UI verification
DUMMY_LOGIN_USER = "irctc_demo_tester"
DUMMY_LOGIN_PASS = "Test@Pass2026!"

# Registration Form Test Data
DUMMY_REG_USERNAME = "tester_demo_2026"
DUMMY_REG_FULLNAME = "IRCTC Automation Tester"
DUMMY_REG_PASSWORD = "Password@2026"
DUMMY_REG_EMAIL = "tester.irctc.automation@example.com"
DUMMY_REG_MOBILE = "9876543210"
