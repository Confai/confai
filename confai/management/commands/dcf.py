import requests
import json
import logging

logger = logging.getLogger(__name__)

class DCF:
    def __init__(self):
        self.base_url = "http://discountingcashflows.com/api"

    def get_transcript(self, ticker, quarter, year):
        endpoint = f"{self.base_url}/transcript/{ticker}/{quarter}/{year}/"
        logger.info(f"Sending request to {endpoint}")
        response = requests.get(endpoint)

        if response.status_code == 200 and response.content:
            try:
                response_json = response.json()
                logger.info(f"Received response: {response.status_code}")
                if len(response_json) > 0:
                    return response_json[0]
                else:
                    logger.error("No transcript available for the given parameters: {ticker}, {quarter}, {year}")
                    return None
            except json.JSONDecodeError:
                logger.error("Response is not a valid JSON.")
                return None
        else:
            logger.error(f"HTTP status code {response.status_code} when trying to get transcript.")
            return None

    def get_news(self, ticker, limit=5):
        endpoint = f"{self.base_url}/news/{ticker}/{limit}"
        logger.info(f"Sending request to {endpoint}")
        response = requests.get(endpoint)

        if response.status_code == 200 and response.content:
            try:
                response_json = response.json()
                logger.info(f"Received response: {response.status_code}")
                return response_json
            except json.JSONDecodeError:
                logger.error("Response is not a valid JSON.")
                return None
        else:
            logger.error(f"HTTP status code {response.status_code} when trying to get news.")
            return None