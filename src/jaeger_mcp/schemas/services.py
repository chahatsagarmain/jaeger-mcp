from pydantic import BaseModel, Field


class GetAllServices(BaseModel):
    services: list[str] = Field(
        default=[], description="get all service names instrumented with jaeger"
    )


class Operation(BaseModel):
    name: str = Field(default="", description="name of the operation for the service")
    spanKind: str = Field(default="", description="span kind name")


class GetServiceOperations(BaseModel):
    operations: list[Operation] = Field(
        default=[], description="list of operations for the service"
    )
