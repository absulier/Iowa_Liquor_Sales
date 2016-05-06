#sets up environement
% matplotlib inline
from collections import defaultdict
import datetime
from matplotlib import pyplot as plt
plt.rcParams['figure.figsize'] = 10, 10
import seaborn as sns
import numpy as np
import pandas as pd
from sklearn import linear_model
from sklearn.cross_validation import train_test_split as tts

#reads in data, deletes unnecessary row
q115 = pd.read_csv("salesq115.csv")
s15 = pd.read_csv("sales2015.csv")
del q115['Unnamed: 0']
del s15['Unnamed: 0']

#aligns stores Q1 sales with their 2015 sales
sales15=pd.merge(s15,q115, how='outer')
sales15=sales15.dropna()

# #sets up lm for exploratory analysis
# lm = linear_model.LinearRegression()

## looks at different correlations
##sees which variables do the best to predict total sales for the year
# x=sales15['sale_total_15q1']
# y=sales15['sale_total_15']
# plt.scatter(x, y)
# plt.xlabel("Total Sales 2015 Q1")
# plt.ylabel("Total Sales 2015")
# plt.show()
#
# x=sales15['sale_mean_15q1']
# y=sales15['sale_total_15']
# plt.scatter(x, y)
# plt.xlabel("Mean Sales 2015 Q1")
# plt.ylabel("Total Sales 2015")
# plt.show()
#
# x=sales15['price_per_liter_mean_15q1']
# y=sales15['sale_total_15']
# plt.scatter(x, y)
# plt.xlabel("Mean Price Per Liter 2015 Q1")
# plt.ylabel("Total Sales 2015")
# plt.show()
#
# x=sales15['vol_sol_l_sum_15q1']
# y=sales15['sale_total_15']
# plt.scatter(x, y)
# plt.xlabel("Total Liters Sold 2015 Q1")
# plt.ylabel("Total Sales 2015")
# plt.show()
#
# x=sales15['vol_sold_l_mean_15q1']
# y=sales15['sale_total_15']
# plt.scatter(x, y)
# plt.xlabel("Mean Liters Sold 2015 Q1")
# plt.ylabel("Total Sales 2015")
# plt.show()
#
# x=sales15['margin_mean_15q1']
# y=sales15['sale_total_15']
# plt.scatter(x, y)
# plt.xlabel("Mean Margin 2015 Q1")
# plt.ylabel("Total Sales 2015")
# plt.show()
#
# x=sales15['margin_sum_15q1']
# y=sales15['sale_total_15']
# plt.scatter(x, y)
# plt.xlabel("Total Margin 2015 Q1")
# plt.ylabel("Total Sales 2015")
# plt.show()

#These variables from Q1 were all highly correlated with sales for the year,
#use them to predict.
#these variables are also correlated with each other, so it is redundant to use all
#However, for the sake of practicing a multvariable linear regression, well use them all
x=['sale_total_15q1','vol_sol_l_sum_15q1','margin_sum_15q1']

#Split data into test and train
train, test = tts(sales15, train_size=.85)
train_x=train[x]
train_y=train['sale_total_15']
test_x=test[x]
test_y=test['sale_total_15']

#Builds the model using the train data.
lm = linear_model.LinearRegression()
model = lm.fit(train_x, train_y)
predictions = lm.predict(test_x)
print "Sample:", lm.score(test_x, test_y)

#Builds the model with a Ridge Regularization
lm = linear_model.RidgeCV()
model = lm.fit(train_x, train_y)
predictions = lm.predict(test_x)
print "Sample with regularization:", lm.score(test_x, test_y)

#Reads in data for Q1 2016 and drops odd column
sales16=pd.read_csv("salesq116.csv")
del sales16['Unnamed: 0']

#Builds a DataFrame of features from Q1 2016 used to predict total 16 sales
x=['sale_total_16q1','vol_sol_l_sum_16q1','margin_sum_16q1']
sales16_model=sales16[x]

#Predicts total 2016 sales for each store and feeds that back into the sales 2016 database
pred16=lm.predict(sales16_model)
sales16['sale_total_16_pred']=pred16

#Sums up total sales for both years
t15= sales15['sale_total_15'].sum()
t15
t16= sales16['sale_total_16_pred'].sum()
t16
#sums up total sales for q1 both years
tq15= sales15['sale_total_15q1'].sum()
tq16= sales16['sale_total_16q1'].sum()

#calculates percent difference
#Note: q1 of 2015 seems artificially low becasue we didnt include sales from stores
#that closed later on in the year. All stores are included for 2016 Q1 at this time,
#as none have closed yet. The raises questions on the choice to exclude sales from stores that closed
#through out the year, since we have to assume some of the stores will close in 2016
#as well and that will effect our total numbers. Also, the tax board still recieves
#revenue from stores that close for sales made when still open.
rev_inc_q1=100*(tq16-tq15)/tq15
rev_inc_pred=100*(t16-t15)/t15

#cuts down the dataframes to the infomation we are interested in
keep=['store_number','sale_total_15','county_number','sale_total_15q1']
sales15=sales15[keep]
keep=['store_number','sale_total_16_pred','county_number','sale_total_16q1']
sales16=sales16[keep]

#combines the years into single dataframe and sorts by county
total=pd.merge(sales15,sales16, on=['store_number','county_number'], how='outer')
total = total.groupby(by=["county_number"], as_index=False)
total = total.agg({"sale_total_15": [np.sum], "sale_total_16_pred": [np.sum],"sale_total_16_pred": [np.sum]})
total.columns = [' '.join(col).strip() for col in total.columns.values]

#read in County IDs
dfid=pd.read_csv('cn.csv')

#cleaning the id df
dfid=dfid.drop(['Unnamed: 0'], axis=1)
dfid.columns=['county_number','county']
counties=pd.merge(total,dfid, on=['county_number','county'])

#Adding state name so that tableau can map counties
state=[]
for i in range(len(counties)):
    state.append('iowa')

counties['state']=state

#Calculating differences in sales per county
preddiff=[]
for i in counties.index:
    preddiff.append(counties['sale_total_15 sum'][i]-counties['sale_total_16_pred sum'][i])
counties['predicted_difference']=preddiff

#exporting to csv to visualize
counties.to_csv('counties.csv')
