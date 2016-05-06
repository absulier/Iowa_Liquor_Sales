#Project Description:
This project analyzed the liquor sales in the state of Iowa. This analysis focused
on finding the total sales for the state of Iowa. The tax board is interested in
seeing how much money they can expect to collect in tax revenue from liquor sales.
This prediction was completed by building a linear regression model to predict the
sales of each store. The model was first trained using data from 2015. The sales
from Q1 of 2015 were used as features to predict the total yearly sales as the target.
After the model was created with the test data from 2015, the model was fed Q1 sales
data for each store to predict their overall sales for the year. The precent difference
from 2015 to 2016 was calculated overall and per county and plotted on a map of
Iowa by color. You can see this map in the "Sales Mapped.jpg" file or access an
interactive version with in the tableau "Sales Mapped.twb" file. You can access
the code for the data cleaning in the "Lab3_3_3.py" file and the code for the analysis
and prediction modeling in the "Lab3_3_4.py" file.

####Note:
While this folder contains cleaned datasets for sales by store and county,
it does not contain the original dataset as it was too large to push to Github.

##Possible Effects of tax increase
The primary stake holder for this project is the Iowa State Tax Board. Secondary
stake holders include the owners of the liquor stores, these stores' consumers,
and every organization that receives money from Iowa state liquor taxes.

The Iowa State Tax Board should be made aware that liquor sales this year are predicted  
to be on the decline. Therefore, they can not expect to create a significant amount
of extra revenue for the state by increasing the liquor tax. Secondary stake holders
like consumers and business owners might react poorly to this increase in tax as
it will inevitably drive sales even lower. If sales continue to drop, it could result
in even lower overall revenue than if they kept the same tax rate.

#Critiques
I did have one major critique on the methodology used for this project. Right now,
our model does a pretty good job of predicting how much a single store will make
assuming it stays open all year, but can not accurately give total counts for the
state.

Early on, we were told to drop stores that opened or closed through out the year.
This is problematic because the state is still collecting tax revenue on these stores
even if they were not open for the whole year. Also, since some stores will probably
close during 2016 as well, it does not make really make sense to use a model that
was just trained on stores that stayed open all year. This prediction effectively
does not control for stores opening or closing and will create substantial error
when we aggregate total sales for the year. What I would have done differently from
the beginning of this lab would have been to separate the data sets into 3 different
sets. Sales for 2015 Q1, Total Sales for 2015, and Sales for 2016 Q1. I then would
have grouped the total sales by either county, zip code, or city. The model would
then be trained on this data to predict total sales for that county, zip, or city.
This model would factor in the money made from stores opening and closing throughout
the time and would also require the deletion of far less data.
