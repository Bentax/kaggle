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
