"""Data coordinator for Sputnik Climbing."""

import logging
from datetime import timedelta

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN, SCAN_INTERVAL_SECONDS
from .api import SputnikClimbingAPI

_LOGGER = logging.getLogger(__name__)


class SputnikCoordinator(DataUpdateCoordinator):
    """Coordinator to fetch Sputnik climbing occupancy data."""

    def __init__(self, hass: HomeAssistant) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=SCAN_INTERVAL_SECONDS),
        )
        self.api = SputnikClimbingAPI()

    async def _async_update_data(self) -> dict:
        """Fetch data from API."""
        try:
            data = await self.hass.async_add_executor_job(self.api.get_occupancy)
            if data is None:
                raise UpdateFailed("Failed to fetch occupancy data")
            return data
        except Exception as err:
            raise UpdateFailed(f"Error fetching data: {err}") from err

