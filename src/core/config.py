import os
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

PROJECT_ROOT = os.path.dirname(os.path.dirname(CURRENT_DIR))

CONFIG_DIR = os.path.join(PROJECT_ROOT, "config")
DATA_DIR = os.path.join(PROJECT_ROOT, "data")

SETTING_FILE = os.path.join(CONFIG_DIR, "settings.toml")
PROJECT_JSON = os.path.join(DATA_DIR, "project.json")
SCHEDULE_JSON = os.path.join(DATA_DIR, "schedule.json")
