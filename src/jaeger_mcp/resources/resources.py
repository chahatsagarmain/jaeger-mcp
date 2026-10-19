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
