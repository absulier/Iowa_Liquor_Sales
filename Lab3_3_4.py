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

x=sales15[u'sale_total_15q1']
y=sales15[u'sale_total_15']

model = lm.fit(x, y)
predictions = lm.predict(x)
