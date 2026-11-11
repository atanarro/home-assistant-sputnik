"""Sputnik Climbing API client."""

import re

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

BASE_URL = "https://sputnikclimbing.deporsite.net"
AJAX_URL = f"{BASE_URL}/ajax/TInnova_v2/Listado_OcupacionAforo/llamadaAjax/obtenerOcupacion"
TIMEOUT_SECONDS = 15


def _new_session() -> requests.Session:
    """Build a session that retries transient connection failures.

    A fresh session per fetch avoids reusing pooled keep-alive connections that
    the server has silently closed during the idle time between polls, which
    surfaced as 'Connection reset by peer'.
    """
    session = requests.Session()
    retry = Retry(
        total=2,
        backoff_factor=1,
        status_forcelist=(502, 503, 504),
        allowed_methods=None,  # the POST is a read-only query, safe to retry
    )
    session.mount("https://", HTTPAdapter(max_retries=retry))
    return session


class SputnikClimbingAPI:
    """Fetches current occupancy data from Sputnik climbing centers."""

    def get_occupancy(self) -> dict | None:
        """Fetch occupancy data for all Sputnik climbing centers."""
        with _new_session() as session:
            # Get CSRF token from page (also sets the session cookie)
            page = session.get(f"{BASE_URL}/aforo-legazpi", timeout=TIMEOUT_SECONDS)
            page.raise_for_status()
            csrf = re.search(r'csrf-token" content="([^"]+)"', page.text)
            if not csrf:
                return None

            # Fetch occupancy data
            resp = session.post(
                AJAX_URL,
                headers={
                    "X-CSRF-TOKEN": csrf.group(1),
                    "X-Requested-With": "XMLHttpRequest",
                },
                timeout=TIMEOUT_SECONDS,
            )
            resp.raise_for_status()

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
