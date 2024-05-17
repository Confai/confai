# Project Name

## Description

Scrape, Analyze, and Serve Earnings Call Transcripts with sentiment analysis and keyword extraction for investors to make informed decisions.

## Getting Started

### Prerequisites

- Python 3.8.10
- pip 24.0
- conda
- Django


### Installation

1. Clone the repository:
    
    ```bash
   git clone https://github.com/siddiki8/confai.git
   ```
2. Install the required packages:
    ```bash
   pip install -r requirements.txt
   ```
### Running the Application

1. Make and apply the migrations:
    ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
2. Start the server:
    ```bash
   python manage.py runserver
   ```
   
3. Select a cache directory 
    In ```confai.stanalysis.sentiment.py``` file, assign a cache directory where you want the model to be stored (about 400 MB)

4. Database management:
    To periodically update the database with the latest transcripts, run the following command: 
   ```bash
   python scheduletask.py
   ```
   To update the database with calls from a specific quarter, run the following command:
   ```bash
    python manage.py load_analysis <year> <quarter>
    ```
   Currently 2024 Q1 and 2023 Q4 have been added


5. Open the browser and go to http://localhost:8000

### API Documentation
    endpoints:
    -api/symbol/<path:symbol>/ - view the latest call of a symbol
    -api/ticker_list/ - view the list of tickers of today's calls
    -api/call_detail/<path:ticker_symbol>/<int:year>/<int:quarter>/ - view the analysis of a single call
    -api/prior_ticker_list/?count=count - view tickers starting from yesteday
    -api/all_calls/ - view all calls
