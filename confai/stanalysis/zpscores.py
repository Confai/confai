import yfinance as yf
import pandas as pd
import numpy as np

class StockAnalysis:
    def __init__(self, symbol):
        self.ticker = yf.Ticker(symbol)

    def ratio_x_1(self):
        df = self.ticker.balance_sheet
        working_capital = df.loc['Current Assets'].iloc[0] - df.loc['Current Liabilities'].iloc[0]
        total_assets = df.loc['Total Assets'].iloc[0]
        return working_capital/total_assets

    def ratio_x_2(self):
        df = self.ticker.balance_sheet
        retained_earnings = df.loc['Retained Earnings'].iloc[0]
        total_assets = df.loc['Total Assets'].iloc[0]
        return retained_earnings/total_assets

    def ratio_x_3(self):
        df = self.ticker.income_stmt
        ebit = df.loc['EBIT'].iloc[0]
        total_assets = self.ticker.balance_sheet.loc['Total Assets'].iloc[0]
        return ebit/total_assets

    def ratio_x_4(self):
        equity_market_value = self.ticker.info['sharesOutstanding'] * self.ticker.info['currentPrice']
        total_liabilities = self.ticker.balance_sheet.loc['Total Liabilities Net Minority Interest'].iloc[0]
        return equity_market_value/total_liabilities

    def ratio_x_5(self):
        df = self.ticker.income_stmt
        sales = df.loc['Total Revenue'].iloc[0]
        total_assets = self.ticker.balance_sheet.loc['Total Assets'].iloc[0]
        return sales/total_assets

    def z_score(self):
        ratio_1 = self.ratio_x_1()
        ratio_2 = self.ratio_x_2()
        ratio_3 = self.ratio_x_3()
        ratio_4 = self.ratio_x_4()
        ratio_5 = self.ratio_x_5()
        zscore = 1.2*ratio_1 + 1.4*ratio_2 + 3.3*ratio_3 + 0.6*ratio_4 + 1.0*ratio_5
        return zscore

    def net_income(self):
        df = self.ticker.income_stmt
        return df.loc['Net Income'].iloc[0]

    def roa(self):
        df = self.ticker.balance_sheet
        avg_assets = (df.loc['Total Assets'].iloc[0] + df.loc['Total Assets'].iloc[1]) / 2
        return round(self.net_income() / avg_assets, 2)

    def ocf(self):
        df = self.ticker.cash_flow
        if 'Operating Cash Flow' in df.index:
            return df.loc['Operating Cash Flow'].iloc[0]
        else:
            return df.loc['Free Cash Flow'].iloc[0] + abs(df.loc['Capital Expenditure']).iloc[0]

    def ltdebt(self):
        df = self.ticker.balance_sheet
        return (df.loc['Long Term Debt'].iloc[1] - df.loc['Long Term Debt'].iloc[0])

    def current_ratio(self):
        df = self.ticker.balance_sheet
        current_ratio_current = df.loc['Total Assets'].iloc[0] / df.loc['Total Liabilities Net Minority Interest'].iloc[0]
        current_ratio_prev = df.loc['Total Assets'].iloc[1] / df.loc['Total Liabilities Net Minority Interest'].iloc[1]
        return round((current_ratio_current - current_ratio_prev), 2)

    def new_shares(self):
        df = self.ticker.balance_sheet
        return (df.loc['Common Stock'].iloc[1] - df.loc['Common Stock'].iloc[0])

    def gross_margin(self):
        df = self.ticker.income_stmt
        gross_margin_current = df.loc['Gross Profit'].iloc[0] / df.loc['Total Revenue'].iloc[0]
        gross_margin_prev = df.loc['Gross Profit'].iloc[1] / df.loc['Total Revenue'].iloc[1]
        return (gross_margin_current - gross_margin_prev)

    def asset_turnover_ratio(self):
        df_bs = self.ticker.balance_sheet
        y0, y1, y2 = df_bs.loc['Total Assets'].iloc[0], df_bs.loc['Total Assets'].iloc[1], df_bs.loc['Total Assets'].iloc[2]
        avg_asset_y0 = (y0 + y1) / 2
        avg_asset_y1 = (y1 + y2) / 2

        df_is = self.ticker.income_stmt
        tot_rvn_y0 = df_is.loc['Total Revenue'].iloc[0] / avg_asset_y0
        tot_rvn_y1 = df_is.loc['Total Revenue'].iloc[1] / avg_asset_y1

        return round((tot_rvn_y0 - tot_rvn_y1), 2)

    def calculate_piotroski_score(self):
        criteria_dict = {
            'CR1': self.net_income,
            'CR2': self.roa,
            'CR3': self.ocf,
            'CR5': self.ltdebt,
            'CR6': self.current_ratio,
            'CR7': self.new_shares,
            'CR8': self.gross_margin,
            'CR9': self.asset_turnover_ratio
        }

        ps_criteria = {
            'Symbol': self.ticker.info['symbol'],
            'Name': self.ticker.info['longName'],
            'CR1': 0,
            'CR2': 0,
            'CR3': 0,
            'CR4': 0,
            'CR5': 0,
            'CR6': 0,
            'CR7': 0,
            'CR8': 0,
            'CR9': 0
        }

        ps_criteria_data = {
            'Symbol': self.ticker.info['symbol'],
            'Name': self.ticker.info['longName'],
            'CR1': np.nan,
            'CR2': np.nan,
            'CR3': np.nan,
            'CR4': np.nan,
            'CR5': np.nan,
            'CR6': np.nan,
            'CR7': np.nan,
            'CR8': np.nan,
            'CR9': np.nan
        }

        for key, value in criteria_dict.items():
            try:
                result = value()
                ps_criteria_data[key] = result
                if key == 'CR7':
                    ps_criteria[key] = 1 if result >= 0 else 0
                else:
                    ps_criteria[key] = 1 if result > 0 else 0
            except (KeyError, IndexError) as err:
                print(err)
                ps_criteria[key] = 0
                ps_criteria_data[key] = np.nan

        if ps_criteria_data['CR3'] > ps_criteria_data['CR1']:
            ps_criteria['CR4'] = 1
            ps_criteria_data['CR4'] = 1
        else:
            ps_criteria['CR4'] = 0
            ps_criteria_data['CR4'] = 0

        return ps_criteria, ps_criteria_data