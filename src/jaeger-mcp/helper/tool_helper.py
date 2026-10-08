import requests
import logging

logger = logging.getLogger(__name__)

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