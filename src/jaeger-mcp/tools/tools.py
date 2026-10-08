from helper import tool_helper
from schemas import services

DEFAULT_URL = "http://localhost:16686"

def ping_jaeger(ping_url: str = DEFAULT_URL) -> str:
    return tool_helper.ping_jaeger(ping_url)

def get_all_services(ping_url: str = DEFAULT_URL) -> services.GetAllServices | str:
    return tool_helper.get_all_services(ping_url)