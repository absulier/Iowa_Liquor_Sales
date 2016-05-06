import datetime
import numpy as np
import pandas as pd

#reads in data
df = pd.read_csv("Iowa_Liquor_Sales.csv", low_memory=False)

#Creates a county labels df
county=['County Number','County']
cn=df[county].dropna()
cn = cn.groupby(by=['County Number'], as_index=False)
cn = cn.agg({'County': lambda x: x.iloc[0]})
cn.to_csv('cn.csv')

#drops redundant columns
df=df.drop(['County','Category Name','Volume Sold (Gallons)'],axis=1)

#drops to $ from the pricing data
xdol = lambda x : x.replace('$','')
df['State Bottle Cost']=df['State Bottle Cost'].apply(xdol)
df['State Bottle Retail']=df['State Bottle Retail'].apply(xdol)
df['Sale (Dollars)']=df['Sale (Dollars)'].apply(xdol)

#Converts to date times
df["Date"] = pd.to_datetime(df["Date"], infer_datetime_format=True)

#Gets rid of rows with empty data
df = df.dropna(axis=0, how='any')

#Turns floats into integers
intconv= lambda x: int(x)
df['County Number']= df['County Number'].apply(intconv)
df['Category']= df['Category'].apply(intconv)

#Turns objects into floats
floatconv = lambda x: float(x)
df['Sale (Dollars)']= df['Sale (Dollars)'].apply(floatconv)
df['State Bottle Cost']= df['State Bottle Cost'].apply(floatconv)
df['State Bottle Retail']= df['State Bottle Retail'].apply(floatconv)

#Finds first and last dates of business
dfmax = pd.pivot_table(df, index='Store Number', values='Date', aggfunc='max')
dfmin = pd.pivot_table(df, index='Store Number', values='Date', aggfunc='min')

#puts first and last dates of business into two seperate lists
maximums = dfmax.index.values
minimums = dfmin.index.values

#Builds a database first row store id second row first sale date
dfopen = pd.DataFrame()
dfopen['Store Number'] = minimums
dfopen['First Date'] = dfmin.values

#Builds a database first row store id second row last sale date
dfclose = pd.DataFrame()
dfclose['Store Number'] = maximums
dfclose['Last Date'] = dfmax.values

#Joins databases togeter so that we have a DB with first and last sale date
dfdates = pd.merge(dfopen, dfclose, on='Store Number', how='outer')

#Creates an empty list to hold dummy variable if store is active
active = []

#Loops through dates DF, if the first sale takes place in Jan and store stays open till 2016,
#appends to active list saying store is active
#Otherwise appends to active list with empty values
for i in range(len(dfdates)):
    if dfdates['First Date'][i].month == 01 and dfdates['Last Date'][i].year==2016:
        active.append(1)
    else:
        active.append(np.nan)

#Adds new column to dates DB, dummy variable if store was open all year
dfdates['Active']=active

#Joins dates databases to original database, drops sales from stores that did not stay open all year
#Deletes extra columns used to determine if store was open
df = pd.merge(df, dfdates, on='Store Number', how='left').dropna()
df = df.drop(['First Date','Last Date','Active'],axis=1)


#Calculates margin and price per l and stores them in a list
margin=[]
perml=[]
for i in df.index:
    margin.append((df['State Bottle Retail'][i]-df['State Bottle Cost'][i])*df['Bottles Sold'][i])
    perml.append(df['State Bottle Retail'][i]/df['Bottle Volume (ml)'][i])

perl=[]
for item in perml:
    perl.append(item*1000)

#puts margin and price per liter in DF
df['Margin']=margin
df['Price per Liter']=perl

# Filter by our start and end dates Q1 2015
df.sort_values(by=["Store Number", "Date"], inplace=True)
start_date = pd.Timestamp("20150101")
end_date = pd.Timestamp("20150331")
mask = (df['Date'] >= start_date) & (df['Date'] <= end_date)
salesQ115 = df[mask]
salesQ115 = salesQ115.groupby(by=["Store Number"], as_index=False)
salesQ115 = salesQ115.agg({"Sale (Dollars)": [np.sum, np.mean],
                   "Volume Sold (Liters)": [np.sum, np.mean],
                   "Margin": [np.mean, np.sum],
                   "Price per Liter": np.mean,
                   "Zip Code": lambda x: x.iloc[0], # just extract once, should be the same
                   "City": lambda x: x.iloc[0],
                   "County Number": lambda x: x.iloc[0]})
salesQ115.columns=[' '.join(col).strip() for col in salesQ115.columns.values]
salesQ115.columns=['store_number','city','sale_total_15q1','sale_mean_15q1','county_number','price_per_liter_mean_15q1','zip','vol_sol_l_sum_15q1','vol_sold_l_mean_15q1','margin_mean_15q1','margin_sum_15q1']
salesQ115.to_csv('salesQ115.csv')

# Filter by our start and end dates Q1 2016
df.sort_values(by=["Store Number", "Date"], inplace=True)
start_date = pd.Timestamp("20160101")
end_date = pd.Timestamp("20160331")
mask = (df['Date'] >= start_date) & (df['Date'] <= end_date)
salesQ116 = df[mask]
salesQ116 = salesQ116.groupby(by=["Store Number"], as_index=False)
salesQ116 = salesQ116.agg({"Sale (Dollars)": [np.sum, np.mean],
                   "Volume Sold (Liters)": [np.sum, np.mean],
                   "Margin": [np.mean, np.sum],
                   "Price per Liter": np.mean,
                   "Zip Code": lambda x: x.iloc[0], # just extract once, should be the same
                   "City": lambda x: x.iloc[0],
                   "County Number": lambda x: x.iloc[0]})
salesQ116.columns=[' '.join(col).strip() for col in salesQ116.columns.values]
salesQ116.columns=['store_number','city','sale_total_16q1','sale_mean_16q1','county_number','price_per_liter_mean_16q1','zip','vol_sol_l_sum_16q1','vol_sold_l_mean_16q1','margin_mean_16q1','margin_sum_16q1']
salesQ116.to_csv('salesQ116.csv')

# Filter by our start and end dates for 2015
df.sort_values(by=["Store Number", "Date"], inplace=True)
start_date = pd.Timestamp("20150101")
end_date = pd.Timestamp("20151231")
mask = (df['Date'] >= start_date) & (df['Date'] <= end_date)
sales2015 = df[mask]
sales2015 = sales2015.groupby(by=["Store Number"], as_index=False)
sales2015 = sales2015.agg({"Sale (Dollars)": [np.sum, np.mean],
                   "Volume Sold (Liters)": [np.sum, np.mean],
                   "Margin": [np.mean, np.sum],
                   "Price per Liter": np.mean})
sales2015.columns = [' '.join(col).strip() for col in sales2015.columns.values]
sales2015.columns=['store_number','price_per_liter_mean_15','margin_mean_15','margin_sum_15','sale_total_15','sale_mean_15','vol_sol_l_sum_15','vol_sold_l_mean_15']
sales2015.to_csv('sales2015.csv')
