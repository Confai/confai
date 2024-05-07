# Project Name

## Description

Provide a brief description of what your project does and the problem it solves.

## Getting Started

### Prerequisites

- Python 3.8 or higher
- pip
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
   Or use conda
    ```bash
   conda env create -f environment.yml
    conda activate confai
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

4. Start the scheduled task:
    ```bash
   python scheduletask.py
   ```
5. Open the browser and go to http://localhost:8000

### API Documentation
    endpoints:
    -api/symbol/<path:symbol>/ - view the latest call of a symbol
    -api/ticker_list/ - view the list of tickers of today's calls
    -api/call_detail/<path:ticker_symbol>/<int:year>/<int:quarter>/ - view the analysis of a single call
    -api/prior_ticker_list/ - view tickers starting from yesteday
    -api/all_calls/ - view all calls