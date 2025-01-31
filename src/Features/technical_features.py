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
                    "Linear_Regression", "Linear_Regression_Angle", "Linear_Regression_Intercept",\
                    "Rate_of_Change_Percentage", "Rate_of_Change_Ratio", "Rate_of_Change_Ratio_100","Relative_Strength_Index", "Parabolic_SAR", "Parabolic_SAR_Extended",\
                    "Simple_Moving_Average", "Standard_Deviation", "Linear_Regression_Slope", "All_Moving_Average", "Moving_Average_Convergence_Divergence",\
                    "MACD_with_controllable_MA_type","Moving_Average_Convergence/Divergence_Fix_12/26","MESA_Adaptive_Moving_Average","Highest_value_over_a_specified_period",\
                    "Index_of_highest_value_over_a_specified_period", "triangular_moving_average", "one_day_rate_of_change_of_a_triple_smooth_ema", "time_series_forecast",\
                    "typical_price", "ultimate_oscillator", "variance", "weighted_close_price", "williams_r", "weighted_moving_average"]
        
        ##Aroon and Aroon Oscillator, Moving_Average_Convergence_Divergence_Fix_12_26, have issues 

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
    
    def Two_Crows(self):
        self.technical_features["Two_Crows"] = talib.CDL2CROWS(
            self.stock["Open"], self.stock["High"], self.stock["Low"], self.stock["Close"]
        )

    def Three_Black_Crows(self):
        self.technical_features["Three_Black_Crows"] = talib.CDL3BLACKCROWS(
            self.stock["Open"], self.stock["High"], self.stock["Low"], self.stock["Close"]
        )

    def Three_Inside_Up_Down(self):
        self.technical_features["Three_Inside_Up"] = talib.CDL3INSIDE(
            self.stock["Open"], self.stock["High"], self.stock["Low"], self.stock["Close"]
        )

    def Three_Outside_Up_Down(self):
        self.technical_features["Three_Outside_Up"] = talib.CDL3OUTSIDE(
            self.stock["Open"], self.stock["High"], self.stock["Low"], self.stock["Close"]
        )

    def Three_Stars_In_The_South(self):
        self.technical_features["Three_Stars_In_The_South"] = talib.CDL3STARSINSOUTH(
            self.stock["Open"], self.stock["High"], self.stock["Low"], self.stock["Close"]
        )

    def Three_Advancing_White_Soldiers(self):
        self.technical_features["Three_Advancing_White_Soldiers"] = talib.CDL3WHITESOLDIERS(
            self.stock["Open"], self.stock["High"], self.stock["Low"], self.stock["Close"]
        )

    def Abandoned_Baby(self):
        self.technical_features["Abandoned_Baby"] = talib.CDLABANDONEDBABY(
            self.stock["Open"], self.stock["High"], self.stock["Low"], self.stock["Close"]
        )

    def Advance_Block(self):
        self.technical_features["Advance_Block"] = talib.CDLADVANCEBLOCK(
            self.stock["Open"], self.stock["High"], self.stock["Low"], self.stock["Close"]
        )

    def Belt_Hold(self):
        self.technical_features["Belt_Hold"] = talib.CDLBELTHOLD(
            self.stock["Open"], self.stock["High"], self.stock["Low"], self.stock["Close"]
        )

    def Breakaway(self):
        self.technical_features["Breakaway"] = talib.CDLBREAKAWAY(
            self.stock["Open"], self.stock["High"], self.stock["Low"], self.stock["Close"]
        )

    def Closing_Marubozu(self):
        self.technical_features["Closing_Marubozu"] = talib.CDLCLOSINGMARUBOZU(
            self.stock["Open"], self.stock["High"], self.stock["Low"], self.stock["Close"]
        )

    def Concealing_Baby_Swallow(self):
        self.technical_features["Concealing_Baby_Swallow"] = talib.CDLCONCEALBABYSWALL(
            self.stock["Open"], self.stock["High"], self.stock["Low"], self.stock["Close"]
        )

    def Counterattack(self):
        self.technical_features["Counterattack"] = talib.CDLCOUNTERATTACK(
            self.stock["Open"], self.stock["High"], self.stock["Low"], self.stock["Close"]
        )

    def Dark_Cloud_Cover(self):
        self.technical_features["Dark_Cloud_Cover"] = talib.CDLDARKCLOUDCOVER(
            self.stock["Open"], self.stock["High"], self.stock["Low"], self.stock["Close"], penetration=0
        )

    def Doji(self):
        self.technical_features["Doji"] = talib.CDLDOJI(
            self.stock["Open"], self.stock["High"], self.stock["Low"], self.stock["Close"]
        )
    
    def Rate_of_Change_Percentage(self):
        """Rate of Change Percentage: (price - prevPrice) / prevPrice"""
        self.technical_features["Rate_of_Change_Percentage"] = talib.ROCP(self.stock["Close"], timeperiod=10)  # You can adjust timeperiod as needed

    def Rate_of_Change_Ratio(self):
        """Rate of Change Ratio: (price / prevPrice)"""
        self.technical_features["Rate_of_Change_Ratio"] = talib.ROCR(self.stock["Close"], timeperiod=10)  # Adjust timeperiod as needed

    def Rate_of_Change_Ratio_100(self):
        """Rate of Change Ratio 100 Scale: (price / prevPrice) * 100"""
        self.technical_features["Rate_of_Change_Ratio_100"] = talib.ROCR100(self.stock["Close"], timeperiod=10)  # Adjust timeperiod as needed

    def Relative_Strength_Index(self):
        """Relative Strength Index"""
        self.technical_features["Relative_Strength_Index"] = talib.RSI(self.stock["Close"], timeperiod=14)  # Commonly 14

    def Parabolic_SAR(self):
        """Parabolic SAR"""
        self.technical_features["Parabolic_SAR"] = talib.SAR(
            self.stock["High"], self.stock["Low"], acceleration=0.02, maximum=0.2
        )  # Default parameters; adjust if needed

    def Parabolic_SAR_Extended(self):
        """Parabolic SAR - Extended"""
        sar_ext = talib.SAREXT(
            self.stock["High"], self.stock["Low"], 
            startvalue=0, offsetonreverse=0, 
            accelerationinitlong=0.02, 
            accelerationlong=0.02, accelerationmaxlong=0.2,
            accelerationinitshort=0.02, 
            accelerationshort=0.02, accelerationmaxshort=0.2
        )
        self.technical_features["Parabolic_SAR_Extended"] = sar_ext

    def Simple_Moving_Average(self):
        """Simple Moving Average"""
        self.technical_features["Simple_Moving_Average"] = talib.SMA(self.stock["Close"], timeperiod=30)  # Example with 30-day SMA

    def Standard_Deviation(self):
        """Standard Deviation"""
        self.technical_features["Standard_Deviation"] = talib.STDDEV(self.stock["Close"], timeperiod=30, nbdev=1)  # 30-day STDDEV

    def Stochastic(self):
        self.technical_features["Stochastic"] = talib.STOCH(self.stock["High"], self.stock["Low"], self.stock["Close"])

    def Stochastic_Fast(self):
        self.technical_features["Stochastic_Fast"] = talib.STOCHF(self.stock["High"], self.stock["Low"], self.stock["Close"])

    def Stochastic_RSI(self):
        self.technical_features["Stochastic_RSI"] = talib.STOCHRSI(self.stock["Close"])

    def Summation(self):
        self.technical_features["Summation"] = talib.SUM(self.stock["Close"], timeperiod = 30)
    
    def Triple_Exponential_Moving_Average(self):
        self.technical_features["Triple_Exponential_Moving_Average"] = talib.T3(self.stock["Close"], timeperiod = 5)

    def Triple_Exponential_Moving_Average_Oscillator(self):
        self.technical_features["Triple_Exponential_Moving_Average_Oscillator"] = talib.TEMA(self.stock["Close"], timeperiod = 30)

    def True_Range(self):
        self.technical_features["True_Range"] = talib.TRANGE(self.stock["High"], self.stock["Low"], self.stock["Close"])

    def Linear_Regression_Slope(self):
        self.technical_features["Linear_Regression_Slope"] = talib.LINEARREG_SLOPE(self.stock["Close"])

    def All_Moving_Average(self):
        self.technical_features["All_Moving_Average"] = talib.MA(self.stock["Close"])

    def Moving_Average_Convergence_Divergence(self):
        macd, signal, hist = talib.MACD(self.stock["Close"])
        self.technical_features["MACD"] = macd
        self.technical_features["MACD_Signal"] = signal
        self.technical_features["MACD_Histogram"] = hist

    def MACD_with_controllable_MA_type(self):
        macd, signal, hist = talib.MACDEXT(
            self.stock["Close"],
            fastperiod=12,
            slowperiod=26,
            signalperiod=9,
            fastmatype=talib.MA_Type.EMA,
            slowmatype=talib.MA_Type.EMA,
            signalmatype=talib.MA_Type.EMA
        )
        self.technical_features["MACD_EXT"] = macd
        self.technical_features["MACD_EXT_Signal"] = signal
        self.technical_features["MACD_EXT_Histogram"] = hist

    def Moving_Average_Convergence_Divergence_Fix_12_26(self):
        
        macd, signal, hist = talib.MACDFIX(
            self.stock["Close"],
            signalperiod=9
        )
        self.technical_features["MACDFIX"] = macd
        self.technical_features["MACDFIX_Signal"] = signal
        self.technical_features["MACDFIX_Histogram"] = hist
        

    def MESA_Adaptive_Moving_Average(self):
        mama, fama = talib.MAMA(
            self.stock["Close"],
            fastlimit=0.5,
            slowlimit=0.05
        )
        self.technical_features["MAMA"] = mama
        self.technical_features["FAMA"] = fama

    def Highest_value_over_a_specified_period(self):
        self.technical_features["Highest_value_over_a_specified_period"] = talib.MAX(self.stock["Close"], timeperiod=30)

    def Index_of_highest_value_over_a_specified_period(self):
        self.technical_features["Index_of_highest_value_over_a_specified_period"] = talib.MAXINDEX(self.stock["Close"], timeperiod=30)

    def triangular_moving_average(self):
        self.technical_features["triangular_moving_average"] = talib.TRIMA(self.stock["Close"], timeperiod=30)

    def one_day_rate_of_change_of_a_triple_smooth_ema(self):
        self.technical_features["one_day_rate_of_change_of_a_triple_smooth_ema"] = talib.TRIX(self.stock["Close"], timeperiod=30)

    def time_series_forecast(self):
        self.technical_features["Time_series_forecast"] = talib.TSF(self.stock["Close"], timeperiod=14)

    def typical_price(self):
        self.technical_features["Typical_Price"] = talib.TYPPRICE(self.stock["High"], self.stock["Low"], self.stock["Close"])

    def ultimate_oscillator(self):
        self.technical_features["Ultimate_Oscillator"] = talib.ULTOSC(self.stock["High"], self.stock["Low"], self.stock["Close"])

    def variance(self):
        self.technical_features["Variance"] = talib.VAR(self.stock["Close"], timeperiod=5, nbdev=1)

    def weighted_close_price(self):
        self.technical_features["Weighted_Close_Price"] = talib.WCLPRICE(self.stock["High"], self.stock["Low"], self.stock["Close"])

    def williams_r(self):
        self.technical_features["Williams_R"] = talib.WILLR(self.stock["High"], self.stock["Low"], self.stock["Close"])

    def weighted_moving_average(self):
        self.technical_features["Weighted_Moving_Average"] = talib.WMA(self.stock["Close"], timeperiod=30)