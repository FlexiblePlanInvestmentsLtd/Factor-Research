#type: ignore
import pandas as pd
import sqlalchemy

class BuildFeatures:
    def __init__(self, data, ticker):
        self.data = data
        self.ticker = ticker
        self.build_master_data()


    def build_master_data(self):
        import yfinance as yf
        price = yf.Ticker(self.ticker)
        self.stock = price.history(period="max", interval="1d")
        for i,j in self.data.items():
            self.data[i] = j[j['ticker'] == self.ticker]


    def process_financial_statements(self):
        dates = ['filing_date']
        indicator_features=["total revenue","ebitda","eps","Dividend Payout Ratio","total_current_assets"]
        ratio_features = self.data['zacks_fr'].columns.tolist()


        ### Indicators ###
        self.fundamental_features=pd.DataFrame(index=self.data['zacks_fc'].index, columns=(dates+indicator_features+ratio_features))
        self.fundamental_features.loc[:,"total revenue"] = self.data['zacks_fc'].loc[:,"tot_revnu"].values
        self.fundamental_features.loc[:,"ebitda"] = self.data['zacks_fc'].loc[:,"ebitda"].values
        self.fundamental_features.loc[:, "eps"] = self.data['zacks_fc'].loc[:,"diluted_net_eps"].values
        self.fundamental_features.loc[:, "eps"].fillna(self.data['zacks_fc'].loc[:, "basic_net_eps"], inplace=True)
        self.fundamental_features.loc[:, "total_current_assets"] = self.data['zacks_fc'].loc[:, "tot_curr_asset"].values

        ### Dates ###
        self.fundamental_features.loc[:, "filing_date"] = self.data['zacks_fc'].loc[:, "filing_date"].values

        ### Ratios ###
        self.fundamental_features[ratio_features] = self.data['zacks_fr'][ratio_features]
        self.fundamental_features = self.fundamental_features.merge(self.stock["Close"], left_index=True, right_index=True)


    def build_growth_rates(self, lookbacks):
        growth_features=[]
        for i_feature in self.fundamental_features.columns:
            for i_lookback in lookbacks:
                
                if i_feature != "Dividend Payout Ratio" and i_feature != "Buybacks":

                    self.fundamental_features[f"{i_feature}_{i_lookback}"]=(self.fundamental_features[i_feature].astype(float)/self.fundamental_features[i_feature].astype(float).shift(-i_lookback))-1
    def add_to_database(self, ticker):
        self.combined_fetures["ticker"]=ticker
        self.combined_fetures=self.combined_fetures.dropna()

        db_engine = sqlalchemy.create_engine("sqlite:///Fundamental.sqlite", echo=False)

        self.combined_fetures.to_sql('FundamentalTable', con=db_engine, if_exists='append')
    