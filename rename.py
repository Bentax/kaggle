import pandas as pd
pd.set_option('display.max_rows', 5)
reviews = pd.read_csv("../input/wine-reviews/winemag-data-130k-v2.csv", index_col=0)

reviews.rename(columns={'points': 'score'})

reviews.rename(index={0: 'firstEntry', 1: 'secondEntry'})

####### You'll probably rename columns very often, but rename index values very rarely. For that, set_index() is usually more convenient.
####### Both the row index and the column index can have their own name attribute. The complimentary rename_axis() method may be used to change these names. For example:
reviews.rename_axis("wines", axis='rows').rename_axis("fields", axis='columns')

####### Combining
canadian_youtube = pd.read_csv("../input/youtube-new/CAvideos.csv")
british_youtube = pd.read_csv("../input/youtube-new/GBvideos.csv")
pd.concat([canadian_youtube, british_youtube])

####### to pull down videos that happened to be trending on the same day in both Canada and the UK, we could do the following:
left = canadian_youtube.set_index(['title', 'trending_date'])
right = british_youtube.set_index(['title', 'trending_date'])
left.join(right, lsuffix='_CAN', rsuffix='_UK')
'''
		video_id_CAN	channel_title_CAN	category_id_CAN	publish_time_CAN	tags_CAN	views_CAN	likes_CAN	dislikes_CAN	comment_count_CAN	thumbnail_link_CAN	...	tags_UK	views_UK	likes_UK	dislikes_UK	comment_count_UK	thumbnail_link_UK	comments_disabled_UK	ratings_disabled_UK	video_error_or_removed_UK	description_UK
title	trending_date																					
!! THIS VIDEO IS NOTHING BUT PAIN !! | Getting Over It - Part 7	18.04.01	PNn8sECd7io	Markiplier	20	2018-01-03T19:33:53.000Z	getting over it|"markiplier"|"funny moments"|"...	835930	47058	1023	8250	https://i.ytimg.com/vi/PNn8sECd7io/default.jpg	...	NaN	NaN	NaN	NaN	NaN	NaN	NaN	NaN	NaN	NaN
'''

