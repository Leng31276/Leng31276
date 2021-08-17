import os

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent

VMANAGE_HOST = os.getenv('VMANAGE_HOST', "localhost")
VMANAGE_PORT = os.getenv('VMANAGE_PORT', "443")
VMANAGE_USER = os.getenv('VMANAGE_USER', "admin")
VMANAGE_PASS = os.getenv('VMANAGE_PASS', "admin")
