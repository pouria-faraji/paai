from fastapi import APIRouter, HTTPException, Request, Response, status
from loguru import logger
from motor.motor_asyncio import AsyncIOMotorDatabase
from paai.db.db_settings import DBDependency
from paai.db.query_db import QueryDataBaseService
from paai.model.query_datamodels import QueryRequest, QueryResponse

api_router = APIRouter(tags=["Queries"])

@api_router.post("/average", response_model_exclude_none=True)
async def root(query_request: QueryRequest, db:AsyncIOMotorDatabase=DBDependency) -> QueryResponse:
    logger.debug(query_request)
    try:
        query_response = QueryResponse()
        query_response.since = query_request.since
        query_response.to = query_request.to
        query_response.data = []
        for device_id in query_request.device_ids:
            result = await QueryDataBaseService.get_average_by_device_id(db, device_id, query_request.since, query_request.to)
            for item in result:
                query_response.data.append(QueryResponse.AggregationResponse(**{'device_id': device_id, 'average': item['totalAverage']}))

        return query_response
        
    except Exception as ex:
        logger.error(ex)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(ex))

@api_router.post("/maximum", response_model_exclude_none=True)
async def root(query_request: QueryRequest, db:AsyncIOMotorDatabase=DBDependency) -> QueryResponse:
    logger.debug(query_request)
    try:
        query_response = QueryResponse()
        query_response.since = query_request.since
        query_response.to = query_request.to
        query_response.data = []
        for device_id in query_request.device_ids:
            result = await QueryDataBaseService.get_maximum_by_device_id(db, device_id, query_request.since, query_request.to)
            for item in result:
                query_response.data.append(QueryResponse.AggregationResponse(**{'device_id': device_id, 'maximum': item['totalMaximum']}))

        return query_response
        
    except Exception as ex:
        logger.error(ex)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(ex))

@api_router.post("/minimum", response_model_exclude_none=True)
async def root(query_request: QueryRequest, db:AsyncIOMotorDatabase=DBDependency) -> QueryResponse:
    logger.debug(query_request)
    try:
        query_response = QueryResponse()
        query_response.since = query_request.since
        query_response.to = query_request.to
        query_response.data = []
        for device_id in query_request.device_ids:
            result = await QueryDataBaseService.get_minimum_by_device_id(db, device_id, query_request.since, query_request.to)
            for item in result:
                query_response.data.append(QueryResponse.AggregationResponse(**{'device_id': device_id, 'minimum': item['totalMinimum']}))

        return query_response
        
    except Exception as ex:
        logger.error(ex)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(ex))