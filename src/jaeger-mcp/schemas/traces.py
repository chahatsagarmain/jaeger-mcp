from typing import List
from pydantic import BaseModel, Field

class ServiceSummary(BaseModel):
    name: str = Field(default="", description="Name of the service")
    spanCount: int = Field(default=0, description="Number of spans for this service in the trace")

class TraceSummary(BaseModel):
    traceId: str = Field(default="", description="Unique identifier of the trace")
    rootServiceName: str = Field(default="", description="Root service name of the trace")
    rootOperationName: str = Field(default="", description="Root operation name of the trace")
    minStartTimeUnixNano: str = Field(default="", description="Earliest start time in Unix nanoseconds")
    maxEndTimeUnixNano: str = Field(default="", description="Latest end time in Unix nanoseconds")
    spanCount: int = Field(default=0, description="Total number of spans in the trace")
    services: List[ServiceSummary] = Field(default_factory=list, description="Services involved in the trace")

class GetTraceSummaries(BaseModel):
    summaries: List[TraceSummary] = Field(default_factory=list, description="List of trace summaries")
