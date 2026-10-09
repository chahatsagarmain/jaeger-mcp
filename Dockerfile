FROM python:3.11-slim-bookworm

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    SERVICE_API_VERSION=v3

WORKDIR /app

# Install uv for fast dependency installation
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy project manifests and source
COPY pyproject.toml uv.lock README.md LICENSE ./
COPY src ./src

# Install package and dependencies globally into container python environment
RUN uv pip install --system --no-cache "."

# MCP operates over stdio by default
ENTRYPOINT ["mcp-server-jaeger"]
