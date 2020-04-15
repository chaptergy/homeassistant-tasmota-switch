"""Constants for Tasmota switches."""
# Base component constants
DOMAIN = "tasmota_switch"
DOMAIN_DATA = f"{DOMAIN}_data"
VERSION = "0.0.1"
REQUIRED_FILES = [
    ".translations/en.json",
    "const.py",
    "config_flow.py",
    "manifest.json",
    "switch.py",
]

# Icons and images
ICON = "mdi:power"
