from typing import List
from pydantic import BaseModel , Field

class GetAllServices(BaseModel):
    services : List[str] = Field(default=[] , description="get all service names instrumented with jaeger")