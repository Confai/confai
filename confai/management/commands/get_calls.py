import requests
import json

class DCF:
    def __init__(self):
        self.base_url = "http://discountingcashflows.com/api"

    def get_transcript(self, ticker, quarter, year):
        endpoint = f"{self.base_url}/transcript/{ticker}/{quarter}/{year}/"
        response = requests.get(endpoint)

        #print(response.status_code)

        if response.status_code == 200 and response.content:
            try:
                response_json = response.json()
                if len(response_json) > 0:
                    return response_json[0]
                else:
                    print("Warning: No transcript available for the given parameters.")
                    return None
            except json.JSONDecodeError:
                print("Warning: Response is not a valid JSON.")
                return None
        else:
            print(f"Warning: HTTP status code {response.status_code} when trying to get transcript.")
            return None