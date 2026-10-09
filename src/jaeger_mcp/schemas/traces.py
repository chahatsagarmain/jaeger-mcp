from typing import Any

from pydantic import BaseModel, Field


class ServiceSummary(BaseModel):
    name: str = Field(default="", description="Name of the service")
    spanCount: int = Field(
        default=0, description="Number of spans for this service in the trace"
    )


class TraceSummary(BaseModel):
    traceId: str = Field(default="", description="Unique identifier of the trace")
    rootServiceName: str = Field(
        default="", description="Root service name of the trace"
    )
    rootOperationName: str = Field(
        default="", description="Root operation name of the trace"
    )
    minStartTimeUnixNano: str = Field(
        default="", description="Earliest start time in Unix nanoseconds"
    )
    maxEndTimeUnixNano: str = Field(
        default="", description="Latest end time in Unix nanoseconds"
    )
    spanCount: int = Field(default=0, description="Total number of spans in the trace")
    services: list[ServiceSummary] = Field(
        default_factory=list, description="Services involved in the trace"
    )


class GetTraceSummaries(BaseModel):
    summaries: list[TraceSummary] = Field(
        default_factory=list, description="List of trace summaries"
    )


class ServiceMetrics(BaseModel):
    serviceName: str = Field(default="", description="Name of the service")
    spanCount: int = Field(
        default=0, description="Number of spans belonging to this service"
    )
    cumulativeDurationMs: float = Field(
        default=0.0, description="Sum of span durations in milliseconds"
    )
    errorCount: int = Field(
        default=0, description="Number of error spans in this service"
    )


class TraceOverview(BaseModel):
    traceId: str = Field(default="", description="Unique identifier of the trace")
    rootServiceName: str = Field(default="", description="Root service name")
    rootOperationName: str = Field(default="", description="Root operation name")
    totalDurationMs: float = Field(
        default=0.0,
        description="Total wall-clock duration of the trace in milliseconds",
    )
    spanCount: int = Field(default=0, description="Total number of spans in the trace")
    errorCount: int = Field(default=0, description="Total number of error spans")
    hasErrors: bool = Field(
        default=False, description="Whether any span in the trace encountered an error"
    )
    services: list[ServiceMetrics] = Field(
        default_factory=list, description="Metrics grouped by service"
    )


class SlowestSpan(BaseModel):
    spanId: str = Field(default="", description="Span ID")
    parentSpanId: str | None = Field(
        default=None, description="Parent span ID if not root"
    )
    serviceName: str = Field(default="", description="Service name")
    operationName: str = Field(default="", description="Operation name")
    durationMs: float = Field(default=0.0, description="Duration in milliseconds")
    statusCode: str = Field(
        default="UNSET", description="Status code (UNSET, OK, ERROR)"
    )
    isError: bool = Field(
        default=False, description="Whether this span encountered an error"
    )


class GetSlowestSpans(BaseModel):
    traceId: str = Field(default="", description="Unique identifier of the trace")
    totalSpans: int = Field(default=0, description="Total number of spans in the trace")
    limit: int = Field(default=10, description="Number of spans requested per page")
    offset: int = Field(default=0, description="Offset for pagination")
    hasMore: bool = Field(
        default=False, description="Whether there are more spans after this page"
    )
    spans: list[SlowestSpan] = Field(
        default_factory=list,
        description="List of slowest spans sorted by duration descending",
    )


class TraceErrorSpan(BaseModel):
    spanId: str = Field(default="", description="Span ID")
    serviceName: str = Field(default="", description="Service name")
    operationName: str = Field(default="", description="Operation name")
    durationMs: float = Field(default=0.0, description="Duration in milliseconds")
    statusCode: str = Field(default="ERROR", description="Status code")
    statusMessage: str = Field(default="", description="Error status message")
    errorAttributes: dict[str, Any] = Field(
        default_factory=dict, description="Attributes related to the error"
    )
    events: list[dict[str, Any]] = Field(
        default_factory=list, description="Log events or exceptions on the span"
    )


class TraceErrors(BaseModel):
    traceId: str = Field(default="", description="Unique identifier of the trace")
    totalErrors: int = Field(default=0, description="Count of error spans")
    errors: list[TraceErrorSpan] = Field(
        default_factory=list,
        description="List of failing spans and their error context",
    )


class SpanDetails(BaseModel):
    traceId: str = Field(default="", description="Unique identifier of the trace")
    spanId: str = Field(default="", description="Span ID")
    parentSpanId: str | None = Field(
        default=None, description="Parent span ID if not root"
    )
    serviceName: str = Field(default="", description="Service name")
    operationName: str = Field(default="", description="Operation name")
    startTimeUnixNano: str = Field(
        default="", description="Start time in Unix nanoseconds"
    )
    endTimeUnixNano: str = Field(default="", description="End time in Unix nanoseconds")
    durationMs: float = Field(default=0.0, description="Duration in milliseconds")
    statusCode: str = Field(
        default="UNSET", description="Status code (UNSET, OK, ERROR)"
    )
    statusMessage: str = Field(default="", description="Status message")
    isError: bool = Field(default=False, description="Whether the span failed")
    attributes: dict[str, Any] = Field(
        default_factory=dict, description="Flattened span attributes"
    )
    events: list[dict[str, Any]] = Field(
        default_factory=list, description="Events and logs associated with the span"
    )
    childSpanIds: list[str] = Field(
        default_factory=list, description="List of direct child span IDs"
    )
