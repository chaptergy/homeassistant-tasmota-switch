"""Switch platform for Tasmota."""
import requests
import logging
from asyncio import run_coroutine_threadsafe
from tasmotadevicecontroller import TasmotaDevice
from tasmotadevicecontroller import tasmota_commands as cmd
from tasmotadevicecontroller import tasmota_types as t
from homeassistant.components.switch import SwitchEntity
from homeassistant.const import CONF_NAME, CONF_PASSWORD, CONF_URL, CONF_USERNAME

from .const import DOMAIN_DATA, ICON, DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_platform(
    hass, config, async_add_entities, discovery_info=None
):  # pylint: disable=unused-argument
    """Setup switch platform."""

    url = discovery_info.get(CONF_URL)
    name = discovery_info.get(CONF_NAME, None)
    username = discovery_info.get(CONF_USERNAME, None)
    password = discovery_info.get(CONF_PASSWORD, None)

    # Check if one is set but the other isn't
    if (username is None) != (password is None):
        _LOGGER.error("Username and password must either both be unset or set.")
        return

    tasmotaDevice = await TasmotaDevice.connect(url, username, password)

    deviceInfo = await tasmotaDevice.getStatus(t.StatusType.ALL)

    async_add_entities(
        [TasmotaBinarySwitch(hass, tasmotaDevice, name, deviceInfo)], True
    )


async def async_setup_entry(hass, config_entry, async_add_devices):
    """Setup switch device."""
    config = config_entry.as_dict()["data"]
    name = config.get(CONF_NAME, None)
    username = config.get(CONF_USERNAME, None)
    password = config.get(CONF_PASSWORD, None)

    # Check if one is set but the other isn't
    if (username is None) != (password is None):
        _LOGGER.error("Username and password must either both be unset or set.")
        return

    tasmotaDevice = await TasmotaDevice.connect(
        config.get(CONF_URL), username, password
    )

    deviceInfo = await tasmotaDevice.getStatus(t.StatusType.ALL)

    async_add_devices(
        [TasmotaBinarySwitch(hass, tasmotaDevice, name, deviceInfo)], True
    )


class TasmotaBinarySwitch(SwitchEntity):
    """Tasmota switch class."""

    def __init__(self, hass, tasmotaDevice, name, deviceInfo):
        self.hass = hass
        self.attr = {}
        self._status = False
        self._tasmotaDevice = tasmotaDevice

        if name is None:
            self._name = deviceInfo["Status"]["FriendlyName"][0]
        else:
            self._name = name

        self._mac_address = deviceInfo["StatusNET"]["Mac"]
        self._hardware = deviceInfo["StatusFWR"]["Hardware"]
        self._sw_version = deviceInfo["StatusFWR"]["Version"]

        _LOGGER.warn("setup done")

    async def async_update(self):
        """Update the switch."""
        self._status = await self._tasmotaDevice.getPower()

    async def async_turn_on(self, **kwargs):
        """Turn on the switch."""
        try:
            response = await self._tasmotaDevice.setPower(t.PowerType.ON)

            if response != True:
                _LOGGER.error("Failed to switch on tasmota switch!")

            self._status = True
        except Exception as e:
            _LOGGER.error(f"Failed to switch on tasmota switch: {str(e)}!")

    async def async_turn_off(self, **kwargs):
        """Turn off the switch."""
        try:
            response = await self._tasmotaDevice.setPower(t.PowerType.OFF)

            if response != False:
                _LOGGER.error("Failed to switch off tasmota switch!")

            self._status = False
        except Exception as e:
            _LOGGER.error(f"Failed to switch off tasmota switch: {str(e)}!")

    async def async_toggle(self, **kwargs):
        """Toggle the switch."""
        try:
            response = await self._tasmotaDevice.setPower(t.PowerType.TOGGLE)

            if response != True and response != False:
                _LOGGER.error("Failed to toggle on tasmota switch!")

            self._status = response
        except Exception as e:
            _LOGGER.error(f"Failed to toggle tasmota switch: {str(e)}!")

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self.unique_id)},
            "name": self._name,
            "manufacturer": "Tasmota",
            "model": self._hardware,
            "sw_version": self._sw_version,
        }

    @property
    def unique_id(self):
        """Return the unique id of the switch."""
        return self._mac_address

    @property
    def name(self):
        """Return the name of the switch."""
        return self._name

    @property
    def icon(self):
        """Return the icon of this switch."""
        return ICON

    @property
    def is_on(self):
        """Return true if the switch is on."""
        return self._status
