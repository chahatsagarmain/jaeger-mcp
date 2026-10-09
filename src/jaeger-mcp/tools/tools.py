from typing import Annotated

from helper import tool_helper
from pydantic import Field
from schemas import services, traces

DEFAULT_URL = "http://localhost:16686"


def ping_jaeger(
    ping_url: Annotated[str, Field(description="Base URL of the Jaeger UI / Query service")] = DEFAULT_URL,
) -> str:
    """Check connectivity to the Jaeger query service. Verifies whether the Jaeger UI / HTTP API is reachable and responding."""
    return tool_helper.ping_jaeger(ping_url)


def get_all_services(
    ping_url: Annotated[str, Field(description="Base URL of the Jaeger UI / Query service")] = DEFAULT_URL,
) -> services.GetAllServices | str:
    """Retrieve the list of all instrumented service names available in Jaeger. Use this as the first step to discover active microservices."""
    return tool_helper.get_all_services(ping_url)


def get_operations_for_service(
    service_name: Annotated[str, Field(description="Name of the service to retrieve operations for (e.g. 'frontend')")],
    ping_url: Annotated[str, Field(description="Base URL of the Jaeger UI / Query service")] = DEFAULT_URL,
) -> services.GetServiceOperations | str:
    """Retrieve all operations, endpoints, and span kinds (e.g., server, client, internal) registered for a specific service in Jaeger."""
    return tool_helper.get_service_operations(ping_url, service_name)


def get_trace_summaries(
    service_name: Annotated[str, Field(description="Name of the service to query traces for")],
    start_time_min: Annotated[str | None, Field(description="Earliest start time in ISO-8601 format (e.g. '2026-10-08T12:00:00Z'). Defaults to 1 hour ago.")] = None,
    start_time_max: Annotated[str | None, Field(description="Latest start time in ISO-8601 format (e.g. '2026-10-08T13:00:00Z'). Defaults to current time.")] = None,
    search_depth: Annotated[int, Field(description="Maximum number of trace summaries to return")] = 20,
    operation_name: Annotated[str | None, Field(description="Optional operation name to filter traces within the service")] = None,
    ping_url: Annotated[str, Field(description="Base URL of the Jaeger UI / Query service")] = DEFAULT_URL,
) -> traces.GetTraceSummaries | str:
    """Search and retrieve high-level trace summaries for a service within a time range from Jaeger."""
    return tool_helper.get_trace_summaries(
        ping_url=ping_url,
        service_name=service_name,
        start_time_min=start_time_min,
        start_time_max=start_time_max,
        search_depth=search_depth,
        operation_name=operation_name,
    )


def get_trace_overview(
    trace_id: Annotated[str, Field(description="Unique identifier of the trace to inspect")],
    ping_url: Annotated[str, Field(description="Base URL of the Jaeger UI / Query service")] = DEFAULT_URL,
) -> traces.TraceOverview | str:
    """Get high-level overview and metrics for a specific trace, including wall-clock duration, span count, and service breakdown."""
    return tool_helper.get_trace_overview(ping_url=ping_url, trace_id=trace_id)


def get_slowest_spans(
    trace_id: Annotated[str, Field(description="Unique identifier of the trace")],
    limit: Annotated[int, Field(description="Maximum number of slow spans to return per page")] = 10,
    offset: Annotated[int, Field(description="Pagination offset")] = 0,
    ping_url: Annotated[str, Field(description="Base URL of the Jaeger UI / Query service")] = DEFAULT_URL,
) -> traces.GetSlowestSpans | str:
    """Identify latency bottlenecks by retrieving the slowest spans within a specific trace, sorted by duration descending with pagination."""
    return tool_helper.get_slowest_spans(
        ping_url=ping_url,
        trace_id=trace_id,
        limit=limit,
        offset=offset,
    )


def get_trace_errors(
    trace_id: Annotated[str, Field(description="Unique identifier of the trace to inspect for errors")],
    ping_url: Annotated[str, Field(description="Base URL of the Jaeger UI / Query service")] = DEFAULT_URL,
) -> traces.TraceErrors | str:
    """Isolate and retrieve only the failing spans and exceptions/errors within a specific trace for rapid root-cause analysis."""
    return tool_helper.get_trace_errors(ping_url=ping_url, trace_id=trace_id)


def get_span_details(
    trace_id: Annotated[str, Field(description="Unique identifier of the trace containing the span")],
    span_id: Annotated[str, Field(description="Unique identifier of the specific span to inspect")],
    ping_url: Annotated[str, Field(description="Base URL of the Jaeger UI / Query service")] = DEFAULT_URL,
) -> traces.SpanDetails | str:
    """Get granular details of a specific span within a trace, including exact timestamps, duration, attributes, events/logs, and child spans."""
    return tool_helper.get_span_details(ping_url=ping_url, trace_id=trace_id, span_id=span_id)