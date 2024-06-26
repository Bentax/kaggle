import pandas as pd
reviews = pd.read_csv("../input/wine-reviews/winemag-data-130k-v2.csv", index_col=0)
pd.set_option('display.max_rows', 5)

reviews['country'][0]
#'Italy'

reviews.iloc[0]
'''
country                                                    Italy
description    Aromas include tropical fruit, broom, brimston...
                                     ...                        
variety                                              White Blend
winery                                                   Nicosia
Name: 0, Length: 13, dtype: object
'''
reviews.iloc[:, 0]
'''
0            Italy
1         Portugal
            ...   
129969      France
129970      France
Name: country, Length: 129971, dtype: object
'''
reviews.iloc[:3, 0]
'''
0       Italy
1    Portugal
2          US
Name: country, dtype: object
'''
reviews.iloc[1:3, 0]
'''
1    Portugal
2          US
Name: country, dtype: object
'''
reviews.iloc[[0, 1, 2], 0]
'''
0       Italy
1    Portugal
2          US
Name: country, dtype: object
'''
reviews.iloc[-5:]
reviews.loc[0, 'country']
# 'Italy'

reviews.loc[:, ['taster_name', 'taster_twitter_handle', 'points']]

reviews.set_index("title")

reviews.country == 'Italy'
'''
0          True
1         False
          ...  
129969    False
129970    False
Name: country, Length: 129971, dtype: bool
'''

reviews.loc[reviews.country == 'Italy']

reviews.loc[(reviews.country == 'Italy') & (reviews.points >= 90)]

reviews.loc[(reviews.country == 'Italy') | (reviews.points >= 90)]

reviews.loc[reviews.country.isin(['Italy', 'France'])]

reviews.loc[reviews.price.notnull()]

reviews['critic'] = 'everyone'
reviews['critic']
'''
0         everyone
1         everyone
            ...   
129969    everyone
129970    everyone
Name: critic, Length: 129971, dtype: object
'''

reviews['index_backwards'] = range(len(reviews), 0, -1)
reviews['index_backwards']
'''
0         129971
1         129970
           ...  
129969         2
129970         1
Name: index_backwards, Length: 129971, dtype: int64
'''

### I'm an economical wine buyer. Which wine is the "best bargain"? Create a variable bargain_wine with the title of the wine with the highest points-to-price ratio in the dataset.
bargain_idx = (reviews.points / reviews.price).idxmax()
bargain_wine = reviews.loc[bargain_idx, 'title']

### Create a Series descriptor_counts counting how many times each of these two words appears in the description column in the dataset. (For simplicity, let's ignore the capitalized versions of these words.)
n_trop = reviews.description.map(lambda desc: "tropical" in desc).sum()
n_fruity = reviews.description.map(lambda desc: "fruity" in desc).sum()
descriptor_counts = pd.Series([n_trop, n_fruity], index=['tropical', 'fruity'])

### There are only so many words you can use when describing a bottle of wine. Is a wine more likely to be "tropical" or "fruity"? Create a Series descriptor_counts counting how many times each of these two words appears in the description column in the dataset. (For simplicity, let's ignore the capitalized versions of these words.)
n_trop = reviews.description.map(lambda desc: 'tropical' in desc).sum()
n_fruity = reviews.description.map(lambda desc: 'fruity' in desc).sum()
descriptor_counts = pd.Series([n_trop,n_fruity],index=['tropical','fruity'])

### We'd like to host these wine reviews on our website, but a rating system ranging from 80 to 100 points is too hard to understand - we'd like to translate them into simple star ratings. A score of 95 or higher counts as 3 stars, a score of at least 85 but less than 95 is 2 stars. Any other score is 1 star.
### Also, the Canadian Vintners Association bought a lot of ads on the site, so any wines from Canada should automatically get 3 stars, regardless of points.
### Create a series star_ratings with the number of stars corresponding to each review in the dataset.
def stars(row):
    if row.country == 'Canada':
        return 3
    elif row.points >= 95:
        return 3
    elif row.points >= 85:
        return 2
    else:
        return 1
star_ratings = reviews.apply(stars,axis='columns')
