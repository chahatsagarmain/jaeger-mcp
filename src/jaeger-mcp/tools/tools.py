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

def get_trace_overview(trace_id: str, ping_url: str = DEFAULT_URL) -> traces.TraceOverview | str:
    """Get high-level overview and metrics for a specific trace, including duration, span count, and service breakdown."""
    return tool_helper.get_trace_overview(ping_url=ping_url, trace_id=trace_id)

def get_slowest_spans(
    trace_id: str,
    limit: int = 10,
    offset: int = 0,
    ping_url: str = DEFAULT_URL,
) -> traces.GetSlowestSpans | str:
    """Get the slowest spans within a specific trace, sorted by duration descending with pagination and limit."""
    return tool_helper.get_slowest_spans(
        ping_url=ping_url,
        trace_id=trace_id,
        limit=limit,
        offset=offset,
    )

def get_trace_errors(trace_id: str, ping_url: str = DEFAULT_URL) -> traces.TraceErrors | str:
    """Isolate and retrieve only the failing spans and exceptions/errors within a specific trace."""
    return tool_helper.get_trace_errors(ping_url=ping_url, trace_id=trace_id)

def get_span_details(trace_id: str, span_id: str, ping_url: str = DEFAULT_URL) -> traces.SpanDetails | str:
    """Get granular details of a specific span within a trace, including all attributes, events/logs, and child spans."""
    return tool_helper.get_span_details(ping_url=ping_url, trace_id=trace_id, span_id=span_id)