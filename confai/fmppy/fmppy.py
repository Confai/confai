import requests
import time
from requests.exceptions import HTTPError, ConnectionError
from ratelimiter import RateLimiter

API_KEY = 'c127V2ohM7E4V6ctj6aaNwbDfOCPOT5Y'

class FinancialModelingPrepAPI:
    def __init__(self, api_key, max_requests_per_second=5):
        self.api_key = api_key
        self.base_url = "https://financialmodelingprep.com/api/v4/"
        self.rate_limiter = RateLimiter(max_calls=max_requests_per_second, period=1)

    def _request(self, endpoint, params=None):
        url = self.base_url + endpoint
        if params:
            params['apikey'] = self.api_key
        else:
            params = {'apikey': self.api_key}

        with self.rate_limiter:
            try:
                response = requests.get(url, params=params)
                response.raise_for_status()
                return response.json()
            except HTTPError as http_err:
                print(f'HTTP error occurred: {http_err}')
                return None
            except ConnectionError as conn_err:
                print(f'Connection error occurred: {conn_err}')
                return None
            except Exception as err:
                print(f'Other error occurred: {err}')
                return None

    # Define a method for each endpoint
    def profile(self, symbol):
        return self._request(f'profile/{symbol}')

    def quote(self, symbol):
        return self._request(f'quote/{symbol}')

    def historical_price_full(self, symbol, params=None):
        return self._request(f'historical-price-full/{symbol}', params)

    def income_statement(self, symbol, params=None):
        return self._request(f'income-statement/{symbol}', params)

    def balance_sheet_statement(self, symbol, params=None):
        return self._request(f'balance-sheet-statement/{symbol}', params)

    def cash_flow_statement(self, symbol, params=None):
        return self._request(f'cash-flow-statement/{symbol}', params)

    def enterprise_value(self, symbol, params=None):
        return self._request(f'enterprise-value/{symbol}', params)

    def company_key_metrics(self, symbol, params=None):
        return self._request(f'company-key-metrics/{symbol}', params)

    def financial_ratios(self, symbol, params=None):
        return self._request(f'financial-ratios/{symbol}', params)

    def company_rating(self, symbol, params=None):
        return self._request(f'company-rating/{symbol}', params)

    def conference_call_transcript(self, symbol, year, quarter):
        params = {'year': year, 'quarter': quarter}
        return self._request(f'earning_call_transcript/{symbol}', params)

    def batch_earning_call_transcript(self, symbol, year):
        params = {'year': year}
        return self._request(f'earning_call_transcript/{symbol}', params)

# Usage
api = FinancialModelingPrepAPI(api_key=API_KEY, max_requests_per_second=5)
#print(api.profile("AAPL"))
#print(api.quote("AAPL"))
#print(api.historical_price_full("AAPL"))
#print(api.income_statement("AAPL"))
#print(api.balance_sheet_statement("AAPL"))
#print(api.cash_flow_statement("AAPL"))
#print(api.enterprise_value("AAPL"))
#print(api.company_key_metrics("AAPL"))
#print(api.financial_ratios("AAPL"))
#print(api.company_rating("AAPL"))
#print(api.conference_call_transcript("AAPL",2020,3))
print(api.batch_earning_call_transcript("AAPL",2020))
