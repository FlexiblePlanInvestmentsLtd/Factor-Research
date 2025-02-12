#type: ignore
import pandas as pd
import sqlalchemy
import yfinance as yf

class BuildFeatures:
    def __init__(self, data, ticker):
        self.data = data
        self.ticker = ticker
        self.build_master_data()


    def build_master_data(self):
        # import yfinance as yf
        price = yf.Ticker(self.ticker)
        self.stock = price.history(period="max", interval="1d")
        self.stock.index = self.stock.index.tz_convert('US/Eastern')
        for i,j in self.data.items():
            self.data[i] = j[j['ticker'] == self.ticker]
            if 'per_type' in j.columns:
                self.data[i] = self.data[i][self.data[i]['per_type']=='Q']


    def process_financial_statements(self):
        dates = ['filing_date']
        indicator_features=["total revenue","ebitda","eps","Dividend Payout Ratio","total_current_assets"," "]
        ratio_features = self.data['zacks_fr'].columns.tolist()


        ### Indicators ###
        self.fundamental_features=pd.DataFrame(index=self.data['zacks_fc'].index, columns=(dates+indicator_features+ratio_features))
        self.fundamental_features.loc[:,"total revenue"] = self.data['zacks_fc'].loc[:,"tot_revnu"].values
        self.fundamental_features.loc[:,"ebitda"] = self.data['zacks_fc'].loc[:,"ebitda"].values
        self.fundamental_features.loc[:, "eps"] = self.data['zacks_fc'].loc[:,"diluted_net_eps"].values
        self.fundamental_features.loc[:, "eps"].fillna(self.data['zacks_fc'].loc[:, "basic_net_eps"], inplace=True)
        self.fundamental_features.loc[:, "total_current_assets"] = self.data['zacks_fc'].loc[:, "tot_curr_asset"].values

        ### Dates ###
        self.fundamental_features.loc[:, "filing_date"] = self.data['zacks_fc'].loc[:, "filing_date"]

        ### Ratios ###
        self.fundamental_features[ratio_features] = self.data['zacks_fr'][ratio_features]
        self.fundamental_features.set_index('filing_date', inplace=True)
        self.fundamental_features = self.fundamental_features[~self.fundamental_features.index.duplicated(keep='last')]
        # self.fundamental_features = pd.merge_asof(left=self.fundamental_features, right=self.stock['Close'], left_index=True, right_index=True)

    def extend_monthly(self):
        self.fundamental_features.index = self.fundamental_features.index.to_period('M').to_timestamp()
        all_months = pd.date_range(start=self.fundamental_features.index.min(), end=self.fundamental_features.index.max(), freq='MS')

        # Identify missing months
        existing_months = self.fundamental_features.index.to_period('M')
        missing_months = [date for date in all_months if date.to_period('M') not in existing_months]

        # Add missing months to the dataset with NaN values for other columns
        missing_data = pd.DataFrame({
            'filing_date': missing_months
        }).set_index('filing_date')

        # Combine the original and missing data, then sort by index
        self.fundamental_features = pd.concat([self.fundamental_features, missing_data]).sort_index()
        self.fundamental_features.index = self.fundamental_features.index.tz_localize('UTC').tz_convert('US/Eastern')
        self.fundamental_features.ffill(inplace=True)
        

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
    