from helper import tool_helper


def ping_jaeger(ping_url: str = "http://localhost:16686"):
    return tool_helper.ping_jaeger(ping_url)
