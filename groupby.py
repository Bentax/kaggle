import pandas as pd
reviews = pd.read_csv("../input/wine-reviews/winemag-data-130k-v2.csv", index_col=0)
pd.set_option("display.max_rows", 5)

reviews.groupby('points').points.count()
'''
points
80     397
81     692
      ... 
99      33
100     19
Name: points, Length: 21, dtype: int64
'''

reviews.groupby('points').price.min()
'''
points
80      5.0
81      5.0
       ... 
99     44.0
100    80.0
Name: price, Length: 21, dtype: float64
'''

reviews.groupby('winery').apply(lambda df: df.title.iloc[0])
'''
winery
1+1=3                          1+1=3 NV Rosé Sparkling (Cava)
10 Knots                 10 Knots 2010 Viognier (Paso Robles)
                                  ...                        
àMaurice    àMaurice 2013 Fred Estate Syrah (Walla Walla V...
Štoka                         Štoka 2009 Izbrani Teran (Kras)
Length: 16757, dtype: object
'''

# For even more fine-grained control, you can also group by more than one column. For an example, here's how we would pick out the best wine by country and province:
reviews.groupby(['country', 'province']).apply(lambda df: df.loc[df.points.idxmax()])

# Another groupby() method worth mentioning is agg(), which lets you run a bunch of different functions on your DataFrame simultaneously. For example, we can generate a simple statistical summary of the dataset as follows:
reviews.groupby(['country']).price.agg([len, min, max])

# A multi-index differs from a regular index in that it has multiple levels. For example:
countries_reviewed = reviews.groupby(['country', 'province']).description.agg([len])
countries_reviewed
'''
len
country	province	
Argentina	Mendoza Province	3264
Other	536
...	...	...
Uruguay	San Jose	3
Uruguay	24
425 rows × 1 columns
'''

mi = countries_reviewed.index
type(mi)
## pandas.core.indexes.multi.MultiIndex

# The multi-index method you will use most often is the one for converting back to a regular index, the reset_index() method:
countries_reviewed.reset_index()
'''
country	province	len
0	Argentina	Mendoza Province	3264
1	Argentina	Other	536
...	...	...	...
423	Uruguay	San Jose	3
424	Uruguay	Uruguay	24
425 rows × 3 columns
'''

# Sorting
# Looking again at countries_reviewed we can see that grouping returns data in index order, not in value order. That is to say, when outputting the result of a groupby, the order of the rows is dependent on the values in the index, not in the data.
# To get data in the order want it in we can sort it ourselves. The sort_values() method is handy for this.
countries_reviewed = countries_reviewed.reset_index()
countries_reviewed.sort_values(by='len')
'''
country	province	len
179	Greece	Muscat of Kefallonian	1
192	Greece	Sterea Ellada	1
...	...	...	...
415	US	Washington	8639
392	US	California	36247
425 rows × 3 columns
'''

# sort_values() defaults to an ascending sort, where the lowest values go first. However, most of the time we want a descending sort, where the higher numbers go first. That goes thusly:
countries_reviewed.sort_values(by='len', ascending=False)
'''
country	province	len
392	US	California	36247
415	US	Washington	8639
...	...	...	...
63	Chile	Coelemu	1
149	Greece	Beotia	1
425 rows × 3 columns
'''

# To sort by index values, use the companion method sort_index(). This method has the same arguments and default order:
countries_reviewed.sort_index()
'''
country	province	len
0	Argentina	Mendoza Province	3264
1	Argentina	Other	536
...	...	...	...
423	Uruguay	San Jose	3
424	Uruguay	Uruguay	24
425 rows × 3 columns
'''

# you can sort by more than one column at a time:
countries_reviewed.sort_values(by=['country', 'len'])
'''
country	province	len
1	Argentina	Other	536
0	Argentina	Mendoza Province	3264
...	...	...	...
424	Uruguay	Uruguay	24
419	Uruguay	Canelones	43
425 rows × 3 columns
'''

# What are the minimum and maximum prices for each variety of wine? Create a DataFrame whose index is the variety category from the dataset and whose values are the min and max values thereof.
price_extremes = reviews.groupby(['variety']).price.agg([min,max])
'''
              min   max
variety                
Abouriou     15.0  75.0
Agiorgitiko  10.0  66.0
...           ...   ...
Çalkarası    19.0  19.0
Žilavka      15.0  15.0
[707 rows x 2 columns]
'''

# What are the most expensive wine varieties? Create a variable sorted_varieties containing a copy of the dataframe from the previous question where varieties are sorted in descending order based on minimum price, then on maximum price (to break ties).
sorted_varieties = price_extremes.sort_values(by=['min','max'],ascending=False)
'''
             min    max
variety                
Ramisco    495.0  495.0
Terrantez  236.0  236.0
...          ...    ...
Vital        NaN    NaN
Zelen        NaN    NaN
[707 rows x 2 columns]
'''

# Create a Series whose index is reviewers and whose values is the average review score given out by that reviewer. Hint: you will need the taster_name and points columns.
