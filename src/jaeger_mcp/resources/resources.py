import json

from mcp.server import MCPServer

from jaeger_mcp.config import get_base_url, settings
from jaeger_mcp.helper import tool_helper


def register_resources(mcp: MCPServer) -> None:
    """Register all Jaeger MCP resources."""

    @mcp.resource(
        "jaeger://status",
        name="jaeger_status",
        title="Jaeger Connectivity Status",
        description="Health check and accessibility status of the configured Jaeger Query endpoint.",
        mime_type="application/json",
    )
    def jaeger_status() -> str:
        """Get reachability status and configuration details for the Jaeger endpoint."""
        url = get_base_url()
        status = tool_helper.ping_jaeger(url)
        return json.dumps(
            {
                "url": url,
                "serviceApiVersion": settings.service_api_version,
                "timeoutSeconds": settings.request_timeout_seconds,
                "status": status,
            },
            indent=2,
        )

    @mcp.resource(
        "jaeger://services",
        name="jaeger_services",
        title="Instrumented Services List",
        description="List of all active service names currently registered in Jaeger.",
        mime_type="application/json",
    )
    def jaeger_services() -> str:
        """Retrieve all active service names registered in Jaeger."""
        url = get_base_url()
        result = tool_helper.get_all_services(url)
        if hasattr(result, "model_dump_json"):
            return result.model_dump_json(indent=2)
        return json.dumps({"error": str(result)}, indent=2)
