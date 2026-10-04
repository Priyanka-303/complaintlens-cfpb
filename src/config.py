"""Central configuration for the ComplaintLens pipeline."""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
FIGURES_DIR = PROJECT_ROOT / "reports" / "figures"

SOURCE_URL = "https://files.consumerfinance.gov/ccdb/complaints.csv.zip"
SOURCE_FILE = RAW_DIR / "complaints.csv.zip"
REPORTING_YEAR = 2024
MIN_COMPANY_COMPLAINTS = 100
