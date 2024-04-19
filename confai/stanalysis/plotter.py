import cufflinks as cf
import plotly.offline
import yfinance as yf
from datetime import datetime
cf.go_offline() # Required to use plotly offline (no account required).

def plot_data(indicator_data):
    plots = []
    for title, data in indicator_data.items():
        fig = data.iplot(asFigure=True, yTitle='Value')
        fig.update_layout(title={'text': title, 'x':0.5, 'xanchor': 'center'})
        plot_html = plotly.offline.plot(fig, output_type='div', include_plotlyjs=False)
        plots.append(plot_html)
    return plots

def generate_stock_chart(ticker_name, start_date='2007-01-01', end_date=datetime.now().strftime('%Y-%m-%d')):
    # Fetch the stock data
    df = yf.download(ticker_name, start=start_date, end=end_date)

    # Create a cufflinks plot
    fig = df[['Open', 'High', 'Low', 'Close']].iplot(asFigure=True)
    fig.update_layout(title={'text': ticker_name, 'x':0.5, 'xanchor': 'center'})

    # Convert the plot to HTML
    plot_html = plotly.offline.plot(fig, output_type='div', include_plotlyjs=False)

    return plot_html