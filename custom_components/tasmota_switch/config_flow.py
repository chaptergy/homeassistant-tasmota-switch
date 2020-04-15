"""Adds config flow for Tasmota Switch."""
import voluptuous as vol
from collections import OrderedDict
from tasmotadevicecontroller import TasmotaDevice, AuthenticationError
from homeassistant import config_entries
from homeassistant.const import CONF_NAME, CONF_PASSWORD, CONF_URL, CONF_USERNAME

from .const import DOMAIN


@config_entries.HANDLERS.register(DOMAIN)
class TasmotaSwitchFlowHandler(config_entries.ConfigFlow):
    """Config flow for Tasmota Switch."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    def __init__(self):
        """Initialize."""
        self._errors = {}

    async def async_step_user(self, user_input={}):
        """Handle a flow initialized by the user."""
        # if self._async_current_entries():
        #     return self.async_abort(reason="single_instance_allowed")
        # if self.hass.data.get(DOMAIN):
        #     return self.async_abort(reason="single_instance_allowed")

        if user_input is not None:
            name = await self._get_device_name(user_input.get(CONF_URL), None, None)
            if name["success"] is True:
                if user_input.get(CONF_NAME) == "" or user_input.get(CONF_NAME) is None:
                    user_input[CONF_NAME] = name["name"]
                return self.async_create_entry(
                    title=user_input[CONF_NAME], data=user_input
                )
            elif name["error"] == "auth":
                return await self.async_step_auth_info(user_input)
            else:
                self._errors["base"] = "connection"

        return await self._show_basic_config_form(user_input)

    async def async_step_auth_info(self, user_input):
        """Handle a flow to provide authentication information."""
        print(user_input)
        if user_input.get(CONF_PASSWORD) is not None:
            name = await self._get_device_name(
                user_input.get(CONF_URL),
                user_input.get(CONF_USERNAME),
                user_input.get(CONF_PASSWORD),
            )
            if name["success"] is True:
                if user_input.get(CONF_NAME) == "" or user_input.get(CONF_NAME) is None:
                    user_input[CONF_NAME] = name["name"]
                return self.async_create_entry(
                    title=user_input[CONF_NAME], data=user_input
                )
            elif name["error"] == "auth":
                self._errors["base"] = "authentication"
            else:
                self._errors["base"] = "generic"

        return await self._show_auth_info_form(user_input)

    async def _show_basic_config_form(self, user_input):
        """Show the configuration form to edit integration data."""

        # Defaults
        name = ""
        url = ""

        if user_input is not None:
            if CONF_NAME in user_input:
                name = user_input.get(CONF_NAME)
            if CONF_URL in user_input:
                url = user_input.get(CONF_URL)

        data_schema = vol.Schema(
            {
                vol.Required(CONF_URL, default=url): str,
                vol.Optional(CONF_NAME, default=name): str,
            },
        )

        return self.async_show_form(
            step_id="user", data_schema=data_schema, errors=self._errors
        )

    async def _show_auth_info_form(self, user_input):
        """Show the configuration form to edit authentication data."""

        # Defaults
        name = ""
        url = ""
        username = "admin"
        password = ""

        if user_input is not None:
            if CONF_NAME in user_input:
                name = user_input.get(CONF_NAME)
            if CONF_URL in user_input:
                url = user_input.get(CONF_URL)
            if CONF_USERNAME in user_input:
                username = user_input.get(CONF_USERNAME)
            if CONF_PASSWORD in user_input:
                password = user_input.get(CONF_PASSWORD)

        data_schema = vol.Schema(
            {
                vol.Required(CONF_URL, default=url): str,
                vol.Optional(CONF_NAME, default=name): str,
                vol.Required(CONF_USERNAME, default=username): str,
                vol.Required(CONF_PASSWORD, default=password): str,
            },
        )

        return self.async_show_form(
            step_id="auth_info", data_schema=data_schema, errors=self._errors
        )

    async def async_step_import(self, user_input):
        """Import a config entry.
        Special type of import, we're not actually going to store any data.
        Instead, we're going to rely on the values that are in config file.
        """
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")

        return self.async_create_entry(title="configuration.yaml", data={})

    async def _get_device_name(self, url, username, password):
        """Return true if device can be connected to."""
        try:
            device = await TasmotaDevice.connect(url, username, password)
            name = await device.getFriendlyName()
            return {"success": True, "name": name}
        except AuthenticationError as e:
            print(e)
            return {"success": False, "error": "auth"}
        except Exception as e:
            print(e)
            return {"success": False, "error": str(e)}
