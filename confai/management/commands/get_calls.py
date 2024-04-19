import requests

class APIWrapper:
    def __init__(self):
        self.base_url = "http://discountingcashflows.com/api"

    def get_transcript(self, ticker, quarter, year):
        endpoint = f"{self.base_url}/transcript/{ticker}/{quarter}/{year}/"
        response = requests.get(endpoint)

        if response.status_code == 200:
            try:
                return response.json()
            except json.JSONDecodeError:
                print("Warning: Response is not a valid JSON.")
                return None
        else:
            print(f"Warning: HTTP status code {response.status_code} when trying to get transcript.")
            return None

        response.json()

        if len(response) > 0:
            return response[0]
        else:
            print("Warning: No transcript available for the given parameters.")
            return None