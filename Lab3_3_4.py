% matplotlib inline
from collections import defaultdict
import datetime
from matplotlib import pyplot as plt
plt.rcParams['figure.figsize'] = 10, 10
import seaborn as sns
import numpy as np
import pandas as pd
from sklearn import linear_model

q115 = pd.read_csv("salesq115.csv")
s15 = pd.read_csv("sales2015.csv")
del q115['Unnamed: 0']
del s15['Unnamed: 0']

lm = linear_model.LinearRegression()
sales15= pd.merge(s15,q115, how='outer')
sales15=sales15.dropna()

x=sales15['sale_total_15q1']
y=sales15['sale_total_15']
plt.scatter(x, y)
plt.xlabel("Total Sales 2015 Q1")
plt.ylabel("Total Sales 2015")
plt.show()

x=sales15['sale_mean_15q1']
y=sales15['sale_total_15']
plt.scatter(x, y)
plt.xlabel("Mean Sales 2015 Q1")
plt.ylabel("Total Sales 2015")
plt.show()

x=sales15['price_per_liter_mean_15q1']
y=sales15['sale_total_15']
plt.scatter(x, y)
plt.xlabel("Mean Price Per Liter 2015 Q1")
plt.ylabel("Total Sales 2015")
plt.show()

x=sales15['vol_sol_l_sum_15q1']
y=sales15['sale_total_15']
plt.scatter(x, y)
plt.xlabel("Total Liters Sold 2015 Q1")
plt.ylabel("Total Sales 2015")
plt.show()

x=sales15['vol_sold_l_mean_15q1']
y=sales15['sale_total_15']
plt.scatter(x, y)
plt.xlabel("Mean Liters Sold 2015 Q1")
plt.ylabel("Total Sales 2015")
plt.show()

x=sales15['margin_mean_15q1']
y=sales15['sale_total_15']
plt.scatter(x, y)
plt.xlabel("Mean Margin 2015 Q1")
plt.ylabel("Total Sales 2015")
plt.show()

x=sales15['margin_sum_15q1']
y=sales15['sale_total_15']
plt.scatter(x, y)
plt.xlabel("Total Margin 2015 Q1")
plt.ylabel("Total Sales 2015")
plt.show()


x=sales15[['sale_total_15q1','vol_sol_l_sum_15q1','margin_sum_15q1']]

lm = linear_model.LinearRegression()
model = lm.fit(x, y)
predictions = lm.predict(x)
print "Sample:", lm.score(x, y)

lm = linear_model.RidgeCV()
model = lm.fit(x, y)
predictions = lm.predict(x)
print "Sample with regularization:", lm.score(x, y)
