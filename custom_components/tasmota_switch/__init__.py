"""
Component to integrate with tasmota switches.
"""
import os
from datetime import timedelta
import logging
import voluptuous as vol
from homeassistant import config_entries
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers import discovery
from homeassistant.util import Throttle
from homeassistant.const import CONF_NAME, CONF_PASSWORD, CONF_URL, CONF_USERNAME

from .const import DOMAIN_DATA, DOMAIN, REQUIRED_FILES, VERSION

MIN_TIME_BETWEEN_UPDATES = timedelta(seconds=10)

_LOGGER = logging.getLogger(__name__)

DEVICE_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_URL): cv.string,
        vol.Optional(CONF_NAME): cv.string,
        vol.Optional(CONF_USERNAME): cv.string,
        vol.Optional(CONF_PASSWORD): cv.string,
    }
)

CONFIG_SCHEMA = vol.Schema(
    {DOMAIN: vol.All(cv.ensure_list, [DEVICE_SCHEMA])}, extra=vol.ALLOW_EXTRA,
)


async def async_setup(hass, config):
    """Set up this component using YAML."""
    if config.get(DOMAIN) is None:
        # We get here if the integration is set up using config flow
        return True

    # Print startup message
    _LOGGER.info("{name} - v{version}".format(name=DOMAIN, version=VERSION))

    # Check that all required files are present
    file_check = await check_files(hass)
    if not file_check:
        return False

    # For each configured device
    for entry_config in config[DOMAIN]:
        _LOGGER.warn(f"setup switch {entry_config}")

        hass.async_create_task(
            discovery.async_load_platform(hass, "switch", DOMAIN, entry_config, config)
        )

    hass.async_create_task(
        hass.config_entries.flow.async_init(
            DOMAIN, context={"source": config_entries.SOURCE_IMPORT}, data={}
        )
    )
    return True


async def async_setup_entry(hass, config_entry):
    """Set up this integration using UI."""
    conf = hass.data.get(DOMAIN_DATA)
    if config_entry.source == config_entries.SOURCE_IMPORT:
        if conf is None:
            hass.async_create_task(
                hass.config_entries.async_remove(config_entry.entry_id)
            )
        return False

    # Print startup message
    _LOGGER.info(
        _LOGGER.info("{name} - v{version}".format(name=DOMAIN, version=VERSION))
    )

    # Check that all required files are present
    file_check = await check_files(hass)
    if not file_check:
        return False

    # Add switch
    hass.async_add_job(
        hass.config_entries.async_forward_entry_setup(config_entry, "switch")
    )

    return True


async def check_files(hass):
    """Return bool that indicates if all files are present."""
    # Verify that the user downloaded all files.
    base = f"{hass.config.path()}/custom_components/{DOMAIN}/"
    missing = []
    for file in REQUIRED_FILES:
        fullpath = "{}{}".format(base, file)
        if not os.path.exists(fullpath):
            missing.append(file)

    if missing:
        _LOGGER.critical("The following files are missing: %s", str(missing))
        returnvalue = False
    else:
        returnvalue = True

    return returnvalue


async def async_remove_entry(hass, config_entry):
    """Handle removal of an entry."""

    try:
        await hass.config_entries.async_forward_entry_unload(config_entry, "switch")
        _LOGGER.info("Successfully removed switch from the tasmota switch integration")
    except ValueError:
        pass
