import requests
from xml.etree import ElementTree as ET
import re

def fetch_symbols():
    # URL of the XML file
    url = "https://seekingalpha.com/sector/transcripts.xml"

    # Send a GET request to the URL
    response = requests.get(url)

    # Parse the XML content of the response
    root = ET.fromstring(response.content)

    # Find all the 'item' elements in the XML
    items = root.findall('.//item')

    # Initialize a list to store the symbols, quarters, and years
    symbols_quarters_years = []

    # For each 'item', find the 'category' with type 'symbol' and add its text to the symbols list
    for item in items:
        symbol = next((category for category in item.findall('.//category') if category.get('type') == 'symbol'), None)
        title = item.find('title').text if item.find('title') is not None else ''

        # Use a regular expression to find the quarter and year in the title
        match = re.search(r'(Q\d) (\d{4})', title)
        if match and symbol is not None:
            quarter, year = match.groups()
            symbols_quarters_years.append((symbol.text, quarter, year))

    return symbols_quarters_years

# Example usage
calls = fetch_symbols()
