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
                    "High_Wave_Candle", "Hikkake_Pattern", "Modified_Hikkake_Pattern", "Homing_Pigeon", "Identical_Three_Crows", "In_Neck_Pattern",\
                    "Inverted_Hammer","Kicking","Kicking_by_Length", "Ladder_Bottom", "Long_Legged_Doji", "Long_Line_Candle", "Marubozu", "Matching_Low",\
                    "Mat_Hold", "Morning_Doji_Star", "Morning_Star", "On_Neck_Pattern", "Piercing_Pattern",\
                    "Rising_Falling_Three_Methods", "Separating_Lines", "Shooting_Star", "Short_Line_Candle", "Spinning_Top", "Stalled_Pattern", "Stick_Sandwich",\
                    "Takuri", "Tasuki_Gap", "Thrusting_Pattern", "Tristar_Pattern", "Unique_3_River", "Upside_Gap_Two_Crows", "Upside_Downside_Gap_Three_Methods",\
                    "Chande_Momentum_Oscillator", "Pearson_Correlation_Coefficient", "Double_Exponential_Moving_Average", "Directional_Movement_Index",\
                    "Exponential_Moving_Average", "Hilbert_Transform_Dominant_Cycle_Period", "Hilbert_Transform_Dominant_Cycle_Phase", "Hilbert_Transform_Phasor_Components",\
                    "Hilbert_Transform_SineWave", "Hilbert_Transform_Instantaneous_Trendline", "Hilbert_Transform_Trend_vs_Cycle_Mode", "Kaufman_Adaptive_Moving_Average",\
                    "Linear_Regression", "Linear_Regression_Angle", "Linear_Regression_Intercept"]
        
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

    def Identical_Three_Crows(self):
        self.technical_features["Identical_Three_Crows"] = talib.CDLIDENTICAL3CROWS(self.stock["Open"], self.stock["High"], self.stock["Low"], self.stock["Close"])

    def In_Neck_Pattern(self):
        self.technical_features["In_Neck_Pattern"] = talib.CDLINNECK(self.stock["Open"], self.stock["High"], self.stock["Low"], self.stock["Close"])

    def Inverted_Hammer(self):
        self.technical_features["Inverted_Hammer"] = talib.CDLINVERTEDHAMMER(self.stock["Open"], self.stock["High"], self.stock["Low"], self.stock["Close"])

    def Kicking(self):
        self.technical_features["Kicking"] = talib.CDLKICKING(self.stock["Open"], self.stock["High"], self.stock["Low"], self.stock["Close"])

    def Kicking_by_Length(self):
        self.technical_features["Kicking_by_Length"] = talib.CDLKICKINGBYLENGTH(self.stock["Open"], self.stock["High"], self.stock["Low"], self.stock["Close"])

    def Ladder_Bottom(self):
        self.technical_features["Ladder_Bottom"] = talib.CDLLADDERBOTTOM(self.stock["Open"], self.stock["High"], self.stock["Low"], self.stock["Close"])

    def Long_Legged_Doji(self):
        self.technical_features["Long_Legged_Doji"] = talib.CDLLONGLEGGEDDOJI(self.stock["Open"], self.stock["High"], self.stock["Low"], self.stock["Close"])

    def Long_Line_Candle(self):
        self.technical_features["Long_Line_Candle"] = talib.CDLLONGLINE(self.stock["Open"], self.stock["High"], self.stock["Low"], self.stock["Close"])

    def Marubozu(self):
        self.technical_features["Marubozu"] = talib.CDLMARUBOZU(self.stock["Open"], self.stock["High"], self.stock["Low"], self.stock["Close"])

    def Matching_Low(self):
        self.technical_features["Matching_Low"] = talib.CDLMATCHINGLOW(self.stock["Open"], self.stock["High"], self.stock["Low"], self.stock["Close"])

    def Mat_Hold(self):
        self.technical_features["Mat_Hold"] = talib.CDLMATHOLD(self.stock["Open"], self.stock["High"], self.stock["Low"], self.stock["Close"])

    def Morning_Doji_Star(self):
        self.technical_features["Morning_Star"] = talib.CDLMORNINGDOJISTAR(self.stock["Open"], self.stock["High"], self.stock["Low"], self.stock["Close"])

    def Morning_Star(self):
        self.technical_features["Morning_Star"] = talib.CDLMORNINGSTAR(self.stock["Open"], self.stock["High"], self.stock["Low"], self.stock["Close"])

    def On_Neck_Pattern(self):
        self.technical_features["On_Neck_Pattern"] = talib.CDLONNECK(self.stock["Open"], self.stock["High"], self.stock["Low"], self.stock["Close"])

    def Piercing_Pattern(self):
        self.technical_features["Piercing_Pattern"] = talib.CDLPIERCING(self.stock["Open"], self.stock["High"], self.stock["Low"], self.stock["Close"])

    def Rising_Falling_Three_Methods(self):
        self.technical_features["Rising_Falling_Three_Methods"] = talib.CDLRISEFALL3METHODS(self.stock["Open"], self.stock["High"], self.stock["Low"], self.stock["Close"])

    def Separating_Lines(self):
        self.technical_features["Separating_Lines"] = talib.CDLSEPARATINGLINES(self.stock["Open"], self.stock["High"], self.stock["Low"], self.stock["Close"])

    def Shooting_Star(self):
        self.technical_features["Shooting_Star"] = talib.CDLSHOOTINGSTAR(self.stock["Open"], self.stock["High"], self.stock["Low"], self.stock["Close"])

    def Short_Line_Candle(self):
        self.technical_features["Short_Line_Candle"] = talib.CDLSHORTLINE(self.stock["Open"], self.stock["High"], self.stock["Low"], self.stock["Close"])

    def Spinning_Top(self):
        self.technical_features["Spinning_Top"] = talib.CDLSPINNINGTOP(self.stock["Open"], self.stock["High"], self.stock["Low"], self.stock["Close"])

    def Stalled_Pattern(self):
        self.technical_features["Stalled_Pattern"] = talib.CDLSTALLEDPATTERN(self.stock["Open"], self.stock["High"], self.stock["Low"], self.stock["Close"])

    def Stick_Sandwich(self):
        self.technical_features["Stick_Sandwich"] = talib.CDLSTICKSANDWICH(self.stock["Open"], self.stock["High"], self.stock["Low"], self.stock["Close"])

    def Takuri(self):
        self.technical_features["Takuri"] = talib.CDLTAKURI(self.stock["Open"], self.stock["High"], self.stock["Low"], self.stock["Close"])

    def Tasuki_Gap(self):
        self.technical_features["Tasuki_Gap"] = talib.CDLTASUKIGAP(self.stock["Open"], self.stock["High"], self.stock["Low"], self.stock["Close"])

    def Thrusting_Pattern(self):
        self.technical_features["Thrusting_Pattern"] = talib.CDLTHRUSTING(self.stock["Open"], self.stock["High"], self.stock["Low"], self.stock["Close"])

    def Tristar_Pattern(self):
        self.technical_features["Tristar_Pattern"] = talib.CDLTRISTAR(self.stock["Open"], self.stock["High"], self.stock["Low"], self.stock["Close"])

    def Unique_3_River(self):
        self.technical_features["Unique_3_River"] = talib.CDLUNIQUE3RIVER(self.stock["Open"], self.stock["High"], self.stock["Low"], self.stock["Close"])

    def Upside_Gap_Two_Crows(self):
        self.technical_features["Upside_Gap_Two_Crows"] = talib.CDLUPSIDEGAP2CROWS(self.stock["Open"], self.stock["High"], self.stock["Low"], self.stock["Close"])

    def Upside_Downside_Gap_Three_Methods(self):
        self.technical_features["Upside_Downside_Gap_Three_Methods"] = talib.CDLXSIDEGAP3METHODS(self.stock["Open"], self.stock["High"], self.stock["Low"], self.stock["Close"])

    def Chande_Momentum_Oscillator(self):
        self.technical_features["Chande_Momentum_Oscillator"] = talib.CMO(self.stock["Close"])
        
    def Pearson_Correlation_Coefficient(self):
        self.technical_features["Pearson_Correlation_Coefficient"] = talib.CORREL(self.stock["Close"],self.stock["Volume"])
        
    def Double_Exponential_Moving_Average(self):
        self.technical_features["Double_Exponential_Moving_Average"] = talib.DEMA(self.stock["Close"])
        
    def Directional_Movement_Index(self):
        self.technical_features["Directional_Movement_Index"] = talib.DX(self.stock["High"], self.stock["Low"], self.stock["Close"])
        
    def Exponential_Moving_Average(self):
        self.technical_features["Exponential_Moving_Average"] = talib.EMA(self.stock["Close"])
        
    def Hilbert_Transform_Dominant_Cycle_Period(self):
        self.technical_features["Hilbert_Transform_Dominant_Cycle_Period"] = talib.HT_DCPERIOD(self.stock["Close"])
        
    def Hilbert_Transform_Dominant_Cycle_Phase(self):
        self.technical_features["Hilbert_Transform_Dominant_Cycle_Phase"] = talib.HT_DCPHASE(self.stock["Close"])
        
    def Hilbert_Transform_Phasor_Components(self):
        inphase, quadrature = talib.HT_PHASOR(self.stock["Close"])
        self.technical_features["Hilbert_Transform_Phasor_Components_inphase"] = inphase
        self.technical_features["Hilbert_Transform_Phasor_Components_quadrature"] = quadrature
    
    def Hilbert_Transform_SineWave(self):
        sine, leadsine = talib.HT_SINE(self.stock["Close"]) 
        self.technical_features["Hilbert_Transform_SineWave_sine"] = sine
        self.technical_features["Hilbert_Transform_SineWave_leadsine"] = leadsine
        
    def Hilbert_Transform_Instantaneous_Trendline(self):
        self.technical_features["Hilbert_Transform_Instantaneous_Trendline"] = talib.HT_TRENDLINE(self.stock["Close"]) 
        
    def Hilbert_Transform_Trend_vs_Cycle_Mode(self):
        self.technical_features["Hilbert_Transform_Trend_vs_Cycle_Mode"] = talib.HT_TRENDMODE(self.stock["Close"])    
        
    def Kaufman_Adaptive_Moving_Average(self):
        self.technical_features["Kaufman_Adaptive_Moving_Average"] = talib.KAMA(self.stock["Close"])   
        
    def Linear_Regression(self):
        self.technical_features["Linear_Regression"] = talib.LINEARREG(self.stock["Close"]) 
        
    def Linear_Regression_Angle(self):
        self.technical_features["Linear_Regression_Angle"] = talib.LINEARREG_ANGLE(self.stock["Close"])   

    def Linear_Regression_Intercept(self):
        self.technical_features["Linear_Regression_Intercept"] = talib.LINEARREG_INTERCEPT(self.stock["Close"])   
        