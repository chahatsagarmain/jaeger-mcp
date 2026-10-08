from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

from mcp.server import MCPServer
from tools import tools

mcp = MCPServer("Demo")

mcp.tool()(tools.ping_jaeger)
mcp.tool()(tools.get_all_services)
mcp.tool()(tools.get_operations_for_service)
mcp.tool()(tools.get_trace_summaries)
