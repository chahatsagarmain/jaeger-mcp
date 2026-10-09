from dotenv import find_dotenv, load_dotenv
from mcp.server import CacheHint

load_dotenv(find_dotenv())

from mcp.server import MCPServer
from tools import tools

mcp = MCPServer("jaeger-mcp",
        cache_hints={
        "tools/list": CacheHint(ttl_ms=60_000, scope="public"),
        "resources/read": CacheHint(ttl_ms=5_000),
})

mcp.tool(
    description="Check connectivity to the Jaeger query service. Verifies whether the Jaeger UI / HTTP API is reachable and responding."
)(tools.ping_jaeger)

mcp.tool(
    description="Retrieve the list of all instrumented service names available in Jaeger. Use this as the first step to discover active microservices."
)(tools.get_all_services)

mcp.tool(
    description="Retrieve all operations, endpoints, and span kinds (e.g., server, client, internal) registered for a specific service in Jaeger."
)(tools.get_operations_for_service)

mcp.tool(
    description="Search and retrieve high-level trace summaries for a service within a time range from Jaeger."
)(tools.get_trace_summaries)

mcp.tool(
    description="Get high-level overview and metrics for a specific trace, including wall-clock duration, span count, and service breakdown."
)(tools.get_trace_overview)

mcp.tool(
    description="Identify latency bottlenecks by retrieving the slowest spans within a specific trace, sorted by duration descending with pagination."
)(tools.get_slowest_spans)

mcp.tool(
    description="Isolate and retrieve only the failing spans and exceptions/errors within a specific trace for rapid root-cause analysis."
)(tools.get_trace_errors)

mcp.tool(
    description="Get granular details of a specific span within a trace, including exact timestamps, duration, attributes, events/logs, and child spans."
)(tools.get_span_details)


if __name__ == "__main__":
    mcp.run()
