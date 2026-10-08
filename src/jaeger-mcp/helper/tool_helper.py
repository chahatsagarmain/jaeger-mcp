import logging
import os
from datetime import datetime, timedelta, timezone
from dotenv import find_dotenv, load_dotenv
import requests
from schemas import services, traces

load_dotenv(find_dotenv())

logger = logging.getLogger(__name__)

SERVICE_API_VERSION = os.getenv("SERVICE_API_VERSION", "v3")

def ping_jaeger(ping_url : str) -> str:
    try:
        logger.info(f"testing {ping_url}")
        response = requests.get(ping_url)
        if response.status_code == 200:
            logger.info(f"{ping_url} is active")
            return f"jaeger accessible on {ping_url}"
        else:
            logger.warning(f"{ping_url} is down")
            return f"cannot connect to jaeger on {ping_url}"
    except Exception as e:
        logger.error(f"raised exception here for {ping_url} : {str(e)}")
        return f"cannot connect to jaeger on {ping_url} , maybe jaeger is not deployed"

def get_all_services(ping_url: str) -> services.GetAllServices | str:
    try:
        service_url = f"{ping_url}/api/{SERVICE_API_VERSION}/services"
        logger.info(f"getting services for {service_url}")
        response = requests.get(service_url)
        logging.info(f"{response.json()}")
        if response.status_code == 200:
            logger.info(f"{service_url} is active")
            body = response.json()
            return services.GetAllServices(services=body.get("services" , []))
        else:
            logger.warning(f"{service_url} is down")
            return f"cannot connect to jaeger on {service_url}"
    except Exception as e:
            logger.error(f"raised exception here for {service_url} : {str(e)}")
            return f"cannot connect to jaeger on {service_url} , maybe jaeger is not deployed"

def get_service_operations(ping_url: str , service_name: str) -> services.GetServiceOperations | str:
    try:
        service_url = f"{ping_url}/api/{SERVICE_API_VERSION}/operations?service={service_name}"
        logger.info(f"getting services for {service_url}")
        response = requests.get(service_url)
        logging.info(f"{response.json()}")
        if response.status_code == 200:
            logger.info(f"{service_url} is active")
            body = response.json()
            operations = []
            for itr in body.get("operations" , {}):
                operations.append(services.Operation(name=itr.get("name","") , spanKind=itr.get("spanKind","")))
            return services.GetServiceOperations(operations=operations)
        else:
            logger.warning(f"{service_url} is down")
            return f"cannot connect to jaeger on {service_url}"
    except Exception as e:
            logger.error(f"raised exception here for {service_url} : {str(e)}")
            return f"cannot connect to jaeger on {service_url} , maybe jaeger is not deployed"

def get_trace_summaries(
    ping_url: str,
    service_name: str,
    start_time_min: str | None = None,
    start_time_max: str | None = None,
    search_depth: int = 20,
    operation_name: str | None = None,
) -> traces.GetTraceSummaries | str:
    try:
        service_url = f"{ping_url}/api/{SERVICE_API_VERSION}/trace-summaries"

        if not start_time_max:
            start_time_max = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        if not start_time_min:
            start_time_min = (datetime.now(timezone.utc) - timedelta(hours=1)).strftime("%Y-%m-%dT%H:%M:%S.%fZ")

        params = {
            "query.serviceName": service_name,
            "query.startTimeMin": start_time_min,
            "query.startTimeMax": start_time_max,
            "query.searchDepth": search_depth,
        }
        if operation_name:
            params["query.operationName"] = operation_name

        logger.info(f"getting trace summaries for {service_url} with params {params}")
        response = requests.get(service_url, params=params)
        logger.info(f"{response.status_code}")
        if response.status_code == 200:
            logger.info(f"{service_url} is active")
            body = response.json()
            summaries = []
            for item in body.get("summaries", []):
                svc_list = [
                    traces.ServiceSummary(name=s.get("name", ""), spanCount=s.get("spanCount", 0))
                    for s in item.get("services", [])
                ]
                summaries.append(
                    traces.TraceSummary(
                        traceId=item.get("traceId", ""),
                        rootServiceName=item.get("rootServiceName", ""),
                        rootOperationName=item.get("rootOperationName", ""),
                        minStartTimeUnixNano=str(item.get("minStartTimeUnixNano", "")),
                        maxEndTimeUnixNano=str(item.get("maxEndTimeUnixNano", "")),
                        spanCount=item.get("spanCount", 0),
                        services=svc_list,
                    )
                )
            return traces.GetTraceSummaries(summaries=summaries)
        else:
            logger.warning(f"{service_url} is down")
            return f"cannot connect to jaeger on {service_url}"
    except Exception as e:
        logger.error(f"raised exception here for {service_url} : {str(e)}")
        return f"cannot connect to jaeger on {service_url} , maybe jaeger is not deployed"