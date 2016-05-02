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

x=sales15[u'sale_total_15q1'].reshape((len(sales15),1))
y=sales15[u'sale_total_15'].reshape((len(sales15),1))

plt.scatter(x, y)
plt.xlabel("Total Sales 2015 Q1")
plt.ylabel("Total Sales 2015")
plt.show()

model = lm.fit(x, y)
predictions = lm.predict(x)
print lm.score(x,y)
plt.scatter(y,predictions)
plt.xlabel("True Values")
plt.ylabel("Predicted Values")
plt.show()
