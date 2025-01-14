#type: ignore
import pandas as pd
import sqlalchemy

class BuildFeatures:
    def __init__(self, data):
        self.data=data
        self.build_master_index()


        
    def build_master_index(self):
        self.balance_sheet=(pd.DataFrame(self.data['Financials']['Balance_Sheet']['quarterly']).T).set_index("filing_date").iloc[:,2:].astype(float)
        self.balance_sheet.index=pd.to_datetime(self.balance_sheet.index)
        self.balance_sheet=self.balance_sheet.reset_index().drop_duplicates(subset="filing_date", keep="last").set_index("filing_date")

        self.income_statement=(pd.DataFrame(self.data['Financials']['Income_Statement']['quarterly']).T).set_index("filing_date").iloc[:,2:].astype(float)
        self.income_statement.index=pd.to_datetime(self.income_statement.index)
        self.income_statement=self.income_statement.reset_index().drop_duplicates(subset="filing_date", keep="last").set_index("filing_date")
        self.cash_flow_staement=(pd.DataFrame(self.data['Financials']['Cash_Flow']['quarterly']).T).set_index("filing_date").iloc[:,2:].astype(float)
        self.cash_flow_staement.index=pd.to_datetime(self.cash_flow_staement.index)
        self.cash_flow_staement=self.cash_flow_staement.reset_index().drop_duplicates(subset="filing_date", keep="last").set_index("filing_date")

        self.master_index=pd.concat([self.balance_sheet, self.income_statement,self.cash_flow_staement], axis=1, join="inner").index
        self.master_index=self.master_index.dropna()
        self.income_statement=self.income_statement.loc[self.master_index]
        self.cash_flow_staement=self.cash_flow_staement.loc[self.master_index]
        self.balance_sheet=self.balance_sheet.loc[self.master_index]
    def process_financial_statements(self):
        features=["netIncome","totalRevenue","EPS","Free Cash Flow to Firm","ROE","EBITDA","Dividend Payout Ratio","Buybacks","retention ratio","sustainable growth ratio","ROA"]

        self.fundamental_features=pd.DataFrame(index=self.master_index, columns=features)

        self.fundamental_features.loc[:,"netIncome"]=self.income_statement.loc[:,"netIncome"].values
        self.fundamental_features.loc[:,"totalRevenue"]=self.income_statement.loc[:,"totalRevenue"]
        self.fundamental_features.loc[:, "EPS"]=self.income_statement.loc[:,"netIncome"]/self.balance_sheet.loc[:,"commonStockSharesOutstanding"]
        self.fundamental_features.loc[:, "Free Cash Flow to Firm"]=self.income_statement.loc[:,"ebitda"]-self.income_statement.loc[:,"incomeTaxExpense"]-self.cash_flow_staement["capitalExpenditures"]-self.cash_flow_staement["changeInWorkingCapital"]
        
        self.fundamental_features.loc[:,"ROE"]=self.income_statement.loc[:,"netIncome"]/self.balance_sheet.loc[:, "totalStockholderEquity"]
        self.fundamental_features.loc[:,"EBITDA"]=self.income_statement.loc[:, "ebitda"]
        self.fundamental_features.loc[:, "Dividend Payout Ratio"]=self.cash_flow_staement.loc[:, "dividendsPaid"].fillna(0)/self.income_statement.loc[:,"netIncome"]

        self.fundamental_features.loc[:, "Buybacks"]=-self.cash_flow_staement.loc[:, "salePurchaseOfStock"].fillna(0)


        self.fundamental_features.loc[:, "retention ratio"]=1-(self.fundamental_features.loc[:, "Dividend Payout Ratio"])

        self.fundamental_features.loc[:,"sustainable growth ratio"]=self.fundamental_features.loc[:, "retention ratio"]*self.fundamental_features.loc[:,"ROE"]

        self.fundamental_features.loc[:, "ROA"]=self.income_statement.loc[:,"netIncome"]/self.balance_sheet.loc[:,"totalAssets"]
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
    