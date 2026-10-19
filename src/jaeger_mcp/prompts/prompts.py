from mcp.server import MCPServer


def register_prompts(mcp: MCPServer) -> None:
    """Register all Jaeger MCP prompts."""

    @mcp.prompt(
        name="triage-service-incident",
        title="Triage Service Incident",
        description="Guide an AI agent through the 5-stage progressive discovery funnel to diagnose an unhealthy microservice.",
    )
    def triage_service_incident(service_name: str, lookback_hours: str = "1") -> str:
        """Workflow prompt guiding systematic triage of service degradation or failure."""
        return (
            f"You are an SRE investigating performance issues or errors in service '{service_name}' "
            f"over the last {lookback_hours} hour(s).\n\n"
            "Follow the 5-Stage Progressive Discovery Funnel strictly to conserve context tokens:\n"
            f"1. Service & Operation Discovery: Call `get_operations_for_service(service_name='{service_name}')` to inspect registered operations.\n"
            f"2. Trace Discovery: Call `get_trace_summaries(service_name='{service_name}', search_depth=15)` to locate recent degraded or failing traces.\n"
            "3. High-Level Triage: For the most degraded or failing traces, call `get_trace_overview(trace_id=...)` to inspect total wall-clock duration and error counts.\n"
            "4. Bottleneck / Error Isolation:\n"
            "   - If latency is degraded: Call `get_slowest_spans(trace_id=..., limit=5)` to locate the slowest operations.\n"
            "   - If errors/exceptions occurred: Call `get_trace_errors(trace_id=...)` to retrieve only the failing spans.\n"
            "5. Deep-Dive Inspection: Call `get_span_details(trace_id=..., span_id=...)` ONLY on the 1-2 culprit span IDs identified above to inspect attributes, HTTP status codes, and exception logs.\n\n"
            "Synthesize your findings:\n"
            "- Root cause (culprit service, operation, and error message/exception)\n"
            "- Impact analysis (total latency vs component breakdown)\n"
            "- Actionable remediation steps"
        )
