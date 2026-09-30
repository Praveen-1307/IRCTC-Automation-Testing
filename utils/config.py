"""Configuration settings and environment variable management for IRCTC automation framework."""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file if available
load_dotenv()

# Base project directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Application URLs
BASE_URL = os.getenv("IRCTC_BASE_URL", "https://www.irctc.co.in/nget/train-search")
HOME_URL = os.getenv("IRCTC_HOME_URL", "https://www.irctc.co.in/")
REGISTRATION_URL = os.getenv(
    "IRCTC_REG_URL", "https://www.irctc.co.in/nget/profile/user-registration"
)
SEARCH_RESULTS_URL = os.getenv(
    "IRCTC_RESULTS_URL", "https://www.irctc.co.in/nget/booking/train-list"
)

# Browser and execution options
# By default we support Chromium, Firefox, WebKit
DEFAULT_BROWSER = os.getenv("IRCTC_BROWSER", "chromium").lower()
HEADLESS_MODE = os.getenv("IRCTC_HEADLESS", "true").lower() in ("true", "1", "yes")

# Timeout configurations (in milliseconds)
DEFAULT_TIMEOUT = int(os.getenv("IRCTC_DEFAULT_TIMEOUT", "30000"))
NAVIGATION_TIMEOUT = int(os.getenv("IRCTC_NAV_TIMEOUT", "45000"))
ACTION_TIMEOUT = int(os.getenv("IRCTC_ACTION_TIMEOUT", "15000"))

# Artifact directories
SCREENSHOTS_DIR = PROJECT_ROOT / "screenshots"
REPORTS_DIR = PROJECT_ROOT / "reports"
VIDEOS_DIR = PROJECT_ROOT / "videos"
TRACES_DIR = PROJECT_ROOT / "traces"

# Ensure directories exist
for directory in [SCREENSHOTS_DIR, REPORTS_DIR, VIDEOS_DIR, TRACES_DIR]:
    directory.mkdir(parents=True, exist_ok=True)
