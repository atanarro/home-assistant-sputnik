"""Config flow for Sputnik Climbing integration."""

from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult

from .const import DOMAIN
from .api import SputnikClimbingAPI


class SputnikClimbingConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Sputnik Climbing."""

    VERSION = 1

    async def async_step_user(self, user_input=None) -> FlowResult:
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            # Test the API connection
            api = SputnikClimbingAPI()
            try:
                data = await self.hass.async_add_executor_job(api.get_occupancy)
                if data:
                    await self.async_set_unique_id(DOMAIN)
                    self._abort_if_unique_id_configured()
                    return self.async_create_entry(
                        title="Sputnik Climbing",
                        data={},
                    )
                errors["base"] = "cannot_connect"
            except Exception:
                errors["base"] = "cannot_connect"

        return self.async_show_form(step_id="user", errors=errors)

