import logging
import os
import requests
from schemas import services

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