from datetime import datetime, timedelta
from typing import List, Any, Optional

from pydantic import BaseModel, Field


class QueryRequest(BaseModel):

    since: datetime = Field(default=None, 
                            alias='from', 
                            description="The start timestamp to get data from. When omitted, all available data until the 'to' timestamp will be returned", 
                            example= str((datetime.now()- timedelta(days=1)).isoformat()).split('.')[0]+'Z')

    to: datetime = Field(default=None,
                         description="The timestamp until which to get data. When omitted, all available data starting from 'from' until the time of the request execution will be returned",
                         example=str(datetime.now().isoformat()).split('.')[0]+'Z')

    device_ids: List[str] = Field(...,
                                  description="List of device_ids to get aggregation data")

class QueryResponse(BaseModel):
    class AggregationResponse(BaseModel):
        device_id: str
        average: Optional[float] = None
        maximum: Optional[float] = None
        minimum: Optional[float] = None

        # def __init__(__pydantic_self__, aggregation_type) -> None:
        #     super().__init__(aggregation_type)
        #     __pydantic_self__.value = Field(default=None, alias=aggregation_type)
    
    since: datetime = Field(default=None,
                            alias='from',
                            description='The start timestamp to get data from.')
    to: datetime = Field(default=None,
                         description='The timestamp until which to get data.')
    data: List[AggregationResponse] = Field(default=None, description="List of aggregation values for each device")