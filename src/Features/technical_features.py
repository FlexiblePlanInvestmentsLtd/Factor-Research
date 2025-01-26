import pandas as pd
import yfinance as yf
import sqlalchemy
import talib

class BuildFeatures:
    def __init__(self, ticker):
        self.ticker = ticker
        self.get_stock()

        
    def get_stock(self):
        data = yf.Ticker(self.ticker)
        self.stock = data.history(period="max", interval="1d")

    def build_technical_features(self):
        # Add Feature Names here
        features = ["SMA_50", "SMA_200", "Chaikin_ADI_Line", "Chaikin_ADI_Oscillator", "ADM_Index", "ADM_Index_Rating", "Absolute_Price_Oscillator", \
                    "Aroon", "Aroon_Oscillator", "Average_True_Range", "Average_Price", "Bollinger_Band_Upper", "Bollinger_Band_Middle", "Bollinger_Band_Lower", \
                        "Beta", "Balance_of_Power", "Commodity_Channel_Index"]
        self.technical_features=pd.DataFrame(index=self.stock.index, columns=features)

        #### Add Technical Features Here ####
        self.technical_features["SMA_50"]=self.stock["Close"].rolling(window=50).mean()
        self.technical_features["SMA_200"]=self.stock["Close"].rolling(window=200).mean()
        for feature in features[2:]:
            self.f"{feature}()"


    def Chaikin_ADI_Line(self):
        self.technical_features["Chaikin_ADI_Line"] = talib.AD(self.stock["High"], self.stock["Low"], self.stock["Close"], self.stock["Volume"])

    def Chaikin_ADI_Oscillator(self):
        self.technical_features["Chaikin_ADI_Oscillator"] = talib.ADOSC(self.stock["High"], self.stock["Low"], self.stock["Close"], self.stock["Volume"])

    def ADM_Index(self):
        self.technical_features["ADM_Index"] = talib.ADX(self.stock["High"], self.stock["Low"], self.stock["Close"])

    def ADM_Index_Rating(self):
        self.technical_features["ADM_Index_Rating"] = talib.ADXR(self.stock["High"], self.stock["Low"], self.stock["Close"])

    def Absolute_Price_Oscillator(self):
        self.technical_features["Absolute_Price_Oscillator"] = talib.APO(self.stock["Close"])

    def Aroon(self):
        self.technical_features["Aroon"] = talib.AROON(self.stock["High"], self.stock["Low"])

    def Aroon_Oscillator(self):
        self.technical_features["Aroon_Oscillator"] = talib.AROONOSC(self.stock["High"], self.stock["Low"])

    def Average_True_Range(self):
        self.technical_features["Average_True_Range"] = talib.ATR(self.stock["High"], self.stock["Low"], self.stock["Close"])

    def Average_Price(self):
        self.technical_features["Average_Price"] = talib.AVGPRICE(self.stock["Open"], self.stock["High"], self.stock["Low"], self.stock["Close"])

    def Bollinger_Bands(self):
        self.technical_features["Bollinger_Band_Upper"], self.technical_features["Bollinger_Band_Middle"], self.technical_features["Bollinger_Band_Lower"] = talib.BBANDS(self.stock["Close"])

    def Beta(self):
        self.technical_features["Beta"] = talib.BETA(self.stock["High"], self.stock["Low"])
    
    def Balance_of_Power(self):
        self.technical_features["Balance_of_Power"] = talib.BOP(self.stock["Open"], self.stock["High"], self.stock["Low"], self.stock["Close"])
    
    def Commodity_Channel_Index(self):
        self.technical_features["Commodity_Channel_Index"] = talib.CCI(self.stock["High"], self.stock["Low"], self.stock["Close"])

    def add_to_database(self, ticker):
        self.combined_fetures["ticker"]=ticker
        self.combined_fetures=self.combined_fetures.dropna()

        db_engine = sqlalchemy.create_engine("sqlite:///Technical.sqlite", echo=False)

        self.combined_fetures.to_sql('TechnicalTable', con=db_engine, if_exists='append')
        