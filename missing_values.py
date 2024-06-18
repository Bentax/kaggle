import pandas as pd
reviews = pd.read_csv("../input/wine-reviews/winemag-data-130k-v2.csv", index_col=0)
pd.set_option('display.max_rows', 5)

reviews.price.dtype
# dtype('float64')

reviews.dtypes
'''
country        object
description    object
                ...  
variety        object
winery         object
Length: 13, dtype: object
'''

reviews.points.astype('float64')
'''
0         87.0
1         87.0
          ... 
129969    90.0
129970    90.0
Name: points, Length: 129971, dtype: float64
'''

reviews.index.dtype
# dtype('int64')

## Missing data

reviews[pd.isnull(reviews.country)]

reviews.region_2.fillna("Unknown")
'''
0         Unknown
1         Unknown
           ...   
129969    Unknown
129970    Unknown
Name: region_2, Length: 129971, dtype: object
'''

reviews.taster_twitter_handle.replace("@kerinokeefe", "@kerino")
'''
0            @kerino
1         @vossroger
             ...    
129969    @vossroger
129970    @vossroger
Name: taster_twitter_handle, Length: 129971, dtype: object
'''

# Sometimes the price column is null. How many reviews in the dataset are missing a price?
missing_price_reviews = reviews[reviews.price.isnull()]
n_missing_prices = len(missing_price_reviews)
# Cute alternative solution: if we sum a boolean series, True is treated as 1 and False as 0
n_missing_prices = reviews.price.isnull().sum()
# or equivalently:
n_missing_prices = pd.isnull(reviews.price).sum()

# What are the most common wine-producing regions? Create a Series counting the number of times each value occurs in the region_1 field. This field is often missing data, so replace missing values with Unknown. Sort in descending order. Your output should look something like this:
reviews_per_region = reviews.region_1.fillna('Unknown').value_counts().sort_values(ascending=False)
'''
Unknown                    21247
Napa Valley                 4480
                           ...  
Bardolino Superiore            1
Primitivo del Tarantino        1
Name: region_1, Length: 1230, dtype: int64
'''
