"""Sputnik Climbing API client."""

import re
import requests

BASE_URL = "https://sputnikclimbing.deporsite.net"
AJAX_URL = f"{BASE_URL}/ajax/TInnova_v2/Listado_OcupacionAforo/llamadaAjax/obtenerOcupacion"


class SputnikClimbingAPI:
    """Fetches current occupancy data from Sputnik climbing centers."""

    def __init__(self):
        self.session = requests.Session()

    def get_occupancy(self) -> dict | None:
        """Fetch occupancy data for all Sputnik climbing centers."""
        # Get CSRF token from page
        page = self.session.get(f"{BASE_URL}/aforo-legazpi")
        csrf = re.search(r'csrf-token" content="([^"]+)"', page.text)
        if not csrf:
            return None

        # Fetch occupancy data
        resp = self.session.post(AJAX_URL, headers={
            "X-CSRF-TOKEN": csrf.group(1),
            "X-Requested-With": "XMLHttpRequest",
        })

        # Parse response into simple dict, skipping venues with no reported capacity
        return {
            item["Recinto"].replace(" Principal", "").lower(): {
                "current": item["Ocupacion"],
                "max": item["Aforo"],
                "percentage": round(item["Ocupacion"] / item["Aforo"] * 100, 1),
            }
            for item in resp.json()
            if item["Aforo"] > 0
        }

