import pandas as pd
import yfinance as yf
import sqlalchemy

class BuildFeatures:
    def __init__(self, ticker):
        self.ticker = ticker
        self.get_stock()

        
    def get_stock(self):
        data = yf.Ticker(self.ticker)
        historical_data = data.history(period="max", interval="1d")
        self.stock = pd.DataFrame(historical_data['Close'], columns=['MSFT'])

    def build_technical_features(self):
        features = ["SMA_50", "SMA_200"] # Add Feature Names here
        self.technical_features=pd.DataFrame(index=self.stock.index, columns=features)

        #### Add Technical Features Here ####
        self.technical_features["SMA_50"]=self.stock["MSFT"].rolling(window=50).mean()
        self.technical_features["SMA_200"]=self.stock["MSFT"].rolling(window=200).mean()

    def add_to_database(self, ticker):
        self.combined_fetures["ticker"]=ticker
        self.combined_fetures=self.combined_fetures.dropna()

        db_engine = sqlalchemy.create_engine("sqlite:///Technical.sqlite", echo=False)

        self.combined_fetures.to_sql('TechnicalTable', con=db_engine, if_exists='append')
        