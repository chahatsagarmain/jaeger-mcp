from helper import tool_helper
from schemas import services, traces

DEFAULT_URL = "http://localhost:16686"

def ping_jaeger(ping_url: str = DEFAULT_URL) -> str:
    return tool_helper.ping_jaeger(ping_url)

def get_all_services(ping_url: str = DEFAULT_URL) -> services.GetAllServices | str:
    return tool_helper.get_all_services(ping_url)

def get_operations_for_service(service_name: str , ping_url: str = DEFAULT_URL) -> services.GetServiceOperations | str:
    return tool_helper.get_service_operations(ping_url , service_name)

def get_trace_summaries(
    service_name: str,
    start_time_min: str | None = None,
    start_time_max: str | None = None,
    search_depth: int = 20,
    operation_name: str | None = None,
    ping_url: str = DEFAULT_URL,
) -> traces.GetTraceSummaries | str:
    """Get trace summaries for a service within a time range from Jaeger."""
    return tool_helper.get_trace_summaries(
        ping_url=ping_url,
        service_name=service_name,
        start_time_min=start_time_min,
        start_time_max=start_time_max,
        search_depth=search_depth,
        operation_name=operation_name,
    )