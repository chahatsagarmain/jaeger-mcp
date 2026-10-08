from mcp.server import MCPServer
from tools import tools

mcp = MCPServer("Demo")

mcp.tool()(tools.ping_jaeger)

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b


@mcp.resource("greeting://{name}")
def greeting(name: str) -> str:
    """Greet someone by name."""
    return f"Hello, {name}!"