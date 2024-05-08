import requests
from xml.etree import ElementTree as ET
import re
import logging

logger = logging.getLogger(__name__)

def fetch_symbols():
    # URL of the XML file
    url = "https://seekingalpha.com/sector/transcripts.xml"

    # Send a GET request to the URL
    logger.info(f"Sending request to {url}")
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
            logger.info(f"Added symbol: {symbol.text} for Q{quarter} {year}")
        else:
            logger.error(f"Failed to add symbol for title: {title}")

    logger.info(f"Successfully fetched symbols.")
    return symbols_quarters_years