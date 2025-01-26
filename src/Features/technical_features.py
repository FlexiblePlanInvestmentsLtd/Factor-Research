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
                    "Average_True_Range", "Average_Price", "Bollinger_Bands", \
                    "Beta", "Balance_of_Power", "Commodity_Channel_Index", "Doji_Star", "Dragonfly_Doji", "Engulfing_Pattern", "Evening_Doji_Star",\
                    "Evening_Star", "Up_Down_gap_side_by_side_white_lines", "Gravestone_Doji", "Hammer", "Hanging_Man", "Harami_Pattern", "Harami_Cross_Pattern",\
                    "High_Wave_Candle", "Hikkake_Pattern", "Modified_Hikkake_Pattern", "Homing_Pigeon"]
        
        ##Aroon and Aroon Oscillator have issues 

        self.technical_features=pd.DataFrame(index=self.stock.index)

        #### Add Technical Features Here ####
        for feature in features:
            try:
                method_name = getattr(self, feature)  # Get the method from class
                method_name()
            except:
                print(f"Error: {feature}")

        
    
    def add_to_database(self, ticker):
        self.combined_fetures["ticker"]=ticker
        self.combined_fetures=self.combined_fetures.dropna()

        db_engine = sqlalchemy.create_engine("sqlite:///Technical.sqlite", echo=False)

        self.combined_fetures.to_sql('TechnicalTable', con=db_engine, if_exists='append')

    # Add Technical Features Here
    def SMA_50(self):
        self.technical_features["SMA_50"]=self.stock["Close"].rolling(window=50).mean()

    def SMA_200(self):
        self.technical_features["SMA_200"]=self.stock["Close"].rolling(window=200).mean()

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

    def Doji_Star(self):
        self.technical_features["Doji_Star"] = talib.CDLDOJISTAR(self.stock["Open"], self.stock["High"], self.stock["Low"], self.stock["Close"])

    def Dragonfly_Doji(self):
        self.technical_features["Dragonfly_Doji"] = talib.CDLDRAGONFLYDOJI(self.stock["Open"], self.stock["High"], self.stock["Low"], self.stock["Close"])

    def Engulfing_Pattern(self):
        self.technical_features["Engulfing_Pattern"] = talib.CDLENGULFING(self.stock["Open"], self.stock["High"], self.stock["Low"], self.stock["Close"])

    def Evening_Doji_Star(self):
        self.technical_features["Evening_Doji_Star"] = talib.CDLEVENINGDOJISTAR(self.stock["Open"], self.stock["High"], self.stock["Low"], self.stock["Close"])

    def Evening_Star(self):
        self.technical_features["Evening_Star"] = talib.CDLEVENINGSTAR(self.stock["Open"], self.stock["High"], self.stock["Low"], self.stock["Close"])

    def Up_Down_gap_side_by_side_white_lines(self):
        self.technical_features["Up_Down_gap_side_by_side_white_lines"] = talib.CDLGAPSIDESIDEWHITE(self.stock["Open"], self.stock["High"], self.stock["Low"], self.stock["Close"])

    def Gravestone_Doji(self):
        self.technical_features["Gravestone_Doji"] = talib.CDLGRAVESTONEDOJI(self.stock["Open"], self.stock["High"], self.stock["Low"], self.stock["Close"])

    def Hammer(self):
        self.technical_features["Hammer"] = talib.CDLHAMMER(self.stock["Open"], self.stock["High"], self.stock["Low"], self.stock["Close"])

    def Hanging_Man(self):
        self.technical_features["Hanging_Man"] = talib.CDLHANGINGMAN(self.stock["Open"], self.stock["High"], self.stock["Low"], self.stock["Close"])

    def Harami_Pattern(self):
        self.technical_features["Harami_Pattern"] = talib.CDLHARAMI(self.stock["Open"], self.stock["High"], self.stock["Low"], self.stock["Close"])

    def Harami_Cross_Pattern(self):
        self.technical_features["Harami_Cross_Pattern"] = talib.CDLHARAMICROSS(self.stock["Open"], self.stock["High"], self.stock["Low"], self.stock["Close"])

    def High_Wave_Candle(self):
        self.technical_features["High_Wave_Candle"] = talib.CDLHIGHWAVE(self.stock["Open"], self.stock["High"], self.stock["Low"], self.stock["Close"])

    def Hikkake_Pattern(self):
        self.technical_features["Hikkake_Pattern"] = talib.CDLHIKKAKE(self.stock["Open"], self.stock["High"], self.stock["Low"], self.stock["Close"])

    def Modified_Hikkake_Pattern(self):
        self.technical_features["Modified_Hikkake_Pattern"] = talib.CDLHIKKAKEMOD(self.stock["Open"], self.stock["High"], self.stock["Low"], self.stock["Close"])

    def Homing_Pigeon(self):
        self.technical_features["Homing_Pigeon"] = talib.CDLHOMINGPIGEON(self.stock["Open"], self.stock["High"], self.stock["Low"], self.stock["Close"])
