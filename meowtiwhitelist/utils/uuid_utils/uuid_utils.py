import requests
import re
from typing import Optional, Dict

from meowtiwhitelist.utils.logger_utils import *
from meowtiwhitelist.utils.uuid_utils.service_loader import api_services

_UUID_PATTERN = re.compile(
    r"([a-fA-F0-9]{8})"
    r"([a-fA-F0-9]{4})"
    r"([a-fA-F0-9]{4})"
    r"([a-fA-F0-9]{4})"
    r"([a-fA-F0-9]{12})"
)

def _format_uuid(raw_id: str) -> str:
    m = _UUID_PATTERN.search(raw_id)
    return f"{m.group(1)}-{m.group(2)}-{m.group(3)}-{m.group(4)}-{m.group(5)}" if m else ""

def get_mojang_uuid(username: str) -> Optional[str]:
    url = f"https://api.mojang.com/users/profiles/minecraft/{username}"
    response = requests.get(url, timeout=5)
    if response.status_code == 200:
        return _format_uuid(response.json().get("id", ""))
    return None

def get_blessing_skin_uuid(username: str, api_root: str) -> int | str | None:
    url = f"{api_root}/api/profiles/minecraft"
    response = requests.post(url, json=[username], timeout=5)
    if response.status_code == 200:
        items = response.json()
        if items and isinstance(items, list) and len(items) > 0:
            return _format_uuid(items[0].get("id", ""))
    else:
        return response.status_code
    return None

class UUIDFetcher:
    @staticmethod
    def create_fetchers(api_services) -> Dict[int, callable]:
        fetchers = {}
        for service in api_services:
            service_id = service.get("id", -1)
            service_type = service.get("serviceType", "").upper()
            api_root = service.get("yggdrasilAuth", {}).get("blessingSkin", {}).get("apiRoot", "")

            if service_type == "MOJANG":
                fetchers[service_id] = get_mojang_uuid
            elif service_type == "BLESSING_SKIN":
                    fetchers[service_id] = lambda username: get_blessing_skin_uuid(username, api_root)

        return fetchers

fetchers = UUIDFetcher.create_fetchers(api_services)