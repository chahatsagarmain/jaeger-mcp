from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

from mcp.server import MCPServer
from tools import tools

mcp = MCPServer("jaeger-mcp")

mcp.tool()(tools.ping_jaeger)
mcp.tool()(tools.get_all_services)
mcp.tool()(tools.get_operations_for_service)
mcp.tool()(tools.get_trace_summaries)
mcp.tool()(tools.get_trace_overview)
mcp.tool()(tools.get_slowest_spans)
mcp.tool()(tools.get_trace_errors)
mcp.tool()(tools.get_span_details)


if __name__ == "__main__":
    mcp.run()
