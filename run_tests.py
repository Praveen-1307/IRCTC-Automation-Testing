"""CLI Test Runner script for IRCTC Automation Suite."""
import argparse
import sys
from pathlib import Path
import pytest

PROJECT_ROOT = Path(__file__).resolve().parent
REPORTS_DIR = PROJECT_ROOT / "reports"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)
REPORT_FILE = REPORTS_DIR / "report.html"


def build_pytest_args(target: str, browser: str, headed: bool, parallel: bool) -> list:
    """Construct command-line arguments for pytest."""
    args = [
        "-v",
        f"--html={REPORT_FILE}",
        "--self-contained-html",
    ]

    # Target module or marker
    if target == "smoke":
        args.extend(["-m", "smoke"])
    elif target == "train_search":
        args.extend(["-m", "train_search"])
    elif target == "regression":
        args.extend(["-m", "regression"])
    elif target == "login":
        args.extend(["-m", "login"])
    elif target == "registration":
        args.extend(["-m", "registration"])
    elif target == "search_results":
        args.extend(["-m", "search_results"])
    elif target == "e2e":
        args.extend(["-m", "e2e"])
    elif target and target != "all":
        # Specific file or test path
        args.append(target)
    else:
        args.append("tests")

    # Browser selection
    if browser:
        args.extend(["--browser-type", browser])

    # Headed mode
    if headed:
        args.append("--headed")

    # Parallel execution with pytest-xdist
    if parallel:
        args.extend(["-n", "auto"])

    return args


def main():
    """Main CLI entrypoint for running IRCTC automation tests."""
    parser = argparse.ArgumentParser(
        description="IRCTC Playwright + Pytest Automation Runner",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "suite",
        nargs="?",
        default="all",
        help=(
            "Test suite or marker to execute:\n"
            "  all           : Run all 40 test cases (default)\n"
            "  smoke         : Run critical smoke test cases\n"
            "  train_search  : Run train search and station autocomplete tests\n"
            "  search_results: Run search results and train card tests\n"
            "  login         : Run login modal UI validation tests\n"
            "  registration  : Run registration form validation tests\n"
            "  e2e           : Run complete end-to-end workflows\n"
            "  <path>        : Run specific test file (e.g., tests/test_login.py)"
        ),
    )
    parser.add_argument(
        "--browser",
        default="chromium",
        choices=["chromium", "firefox", "webkit"],
        help="Target browser engine (default: chromium)",
    )
    parser.add_argument(
        "--headed",
        action="store_true",
        help="Run browser in headed (visible) mode",
    )
    parser.add_argument(
        "--parallel",
        action="store_true",
        help="Execute tests in parallel using pytest-xdist",
    )

    args = parser.parse_args()

    pytest_args = build_pytest_args(
        target=args.suite,
        browser=args.browser,
        headed=args.headed,
        parallel=args.parallel,
    )

    print("=" * 65)
    print("        IRCTC AUTOMATION TEST SUITE RUNNER")
    print("=" * 65)
    print(f" Target Suite : {args.suite}")
    print(f" Browser      : {args.browser}")
    print(f" Headed Mode  : {args.headed}")
    print(f" HTML Report  : {REPORT_FILE}")
    print(f" Pytest Flags : {' '.join(pytest_args)}")
    print("=" * 65)

    exit_code = pytest.main(pytest_args)

    print("=" * 65)
    print(f" Execution completed with exit code: {exit_code}")
    print(f" Open HTML Report: {REPORT_FILE}")
    print("=" * 65)

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
