import pandas as pd
import geopandas as gpd

from shapely.geometry import LineString

# Load the data and print the first 5 rows
birds_df = pd.read_csv("../input/geospatial-learn-course-data/purple_martin.csv", parse_dates=['timestamp'])
print("There are {} different birds in the dataset.".format(birds_df["tag-local-identifier"].nunique()))
birds_df.head()
'''
There are 11 different birds in the dataset.
timestamp	location-long	location-lat	tag-local-identifier
0	2014-08-15 05:56:00	-88.146014	17.513049	30448
1	2014-09-01 05:59:00	-85.243501	13.095782	30448
2	2014-10-30 23:58:00	-62.906089	-7.852436	30448
3	2014-11-15 04:59:00	-61.776826	-11.723898	30448
4	2014-11-30 09:59:00	-61.241538	-11.612237	30448
'''

# Your code here: Create the GeoDataFrame
birds = gpd.GeoDataFrame(birds_df,geometry=gpd.points_from_xy(birds_df['location-long'],birds_df['location-lat']))

# Your code here: Set the CRS to {'init': 'epsg:4326'}
birds.crs = {'init':'epsg:4326'}

### Plot the data.

## Next, we load in the 'naturalearth_lowres' dataset from GeoPandas, and set americas to a GeoDataFrame containing the boundaries of all countries in the Americas (both North and South America). Run the next code cell without changes.
# Load a GeoDataFrame with country boundaries in North/South America, print the first 5 rows
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
americas = world.loc[world['continent'].isin(['North America', 'South America'])]
americas.head()
'''
	pop_est	continent	name	iso_a3	gdp_md_est	geometry
3	37589262.0	North America	Canada	CAN	1736425	MULTIPOLYGON (((-122.84000 49.00000, -122.9742...
4	328239523.0	North America	United States of America	USA	21433226	MULTIPOLYGON (((-122.84000 49.00000, -120.0000...
9	44938712.0	South America	Argentina	ARG	445445	MULTIPOLYGON (((-68.63401 -52.63637, -68.25000...
10	18952038.0	South America	Chile	CHL	282318	MULTIPOLYGON (((-68.63401 -52.63637, -68.63335...
16	11263077.0	North America	Haiti	HTI	14332	POLYGON ((-71.71236 19.71446, -71.62487 19.169...
'''

# Your code here
ax = americas.plot(figsize=(10,10),color='white',linestyle=':',edgecolor='gray')
birds.plot(ax=ax,markersize=10)

### Where does each bird start and end its journey? (Part 1)
### Now, we're ready to look more closely at each bird's path. Run the next code cell to create two GeoDataFrames:
### path_gdf contains LineString objects that show the path of each bird. It uses the LineString() method to create a LineString object from a list of Point objects.
### start_gdf contains the starting points for each bird.

# GeoDataFrame showing path for each bird
path_df = birds.groupby("tag-local-identifier")['geometry'].apply(list).apply(lambda x: LineString(x)).reset_index()
path_gdf = gpd.GeoDataFrame(path_df, geometry=path_df.geometry)
path_gdf.crs = {'init' :'epsg:4326'}
​
# GeoDataFrame showing starting point for each bird
start_df = birds.groupby("tag-local-identifier")['geometry'].apply(list).apply(lambda x: x[0]).reset_index()
start_gdf = gpd.GeoDataFrame(start_df, geometry=start_df.geometry)
start_gdf.crs = {'init' :'epsg:4326'}
​
# Show first five rows of GeoDataFrame
start_gdf.head()
'''
	tag-local-identifier	geometry
0	30048	POINT (-90.12992 20.73242)
1	30054	POINT (-93.60861 46.50563)
2	30198	POINT (-80.31036 25.92545)
3	30263	POINT (-76.78146 42.99209)
4	30275	POINT (-76.78213 42.99207)
'''

### Use the next code cell to create a GeoDataFrame end_gdf containing the final location of each bird.
### The format should be identical to that of start_gdf, with two columns ("tag-local-identifier" and "geometry"), where the "geometry" column contains Point objects.
### Set the CRS of end_gdf to {'init': 'epsg:4326'}.
end_df = birds.groupby('tag-local-identifier')['geometry'].apply(list).apply(lambda x: x[-1]).reset_index()
end_gdf = gpd.GeoDataFrame(end_df,geometry=end_df.geometry)
end_gdf.crs = {'init':'epsg:4326'}

### Where does each bird start and end its journey? (Part 2)
### Use the GeoDataFrames from the question above (path_gdf, start_gdf, and end_gdf) to visualize the paths of all birds on a single map. You may also want to use the americas GeoDataFrame.

ax = americas.plot(figsize=(10, 10), color='white', linestyle=':', edgecolor='gray')
​
start_gdf.plot(ax=ax, color='red',  markersize=30)
path_gdf.plot(ax=ax, cmap='tab20b', linestyle='-', linewidth=1, zorder=1)
end_gdf.plot(ax=ax, color='black', markersize=30)

### Where are the protected areas in South America? (Part 1)
### It looks like all of the birds end up somewhere in South America. But are they going to protected areas?
### In the next code cell, you'll create a GeoDataFrame protected_areas containing the locations of all of the protected areas in South America. The corresponding shapefile is located at filepath protected_filepath.
# Path of the shapefile to load
protected_filepath = "../input/geospatial-learn-course-data/SAPA_Aug2019-shapefile/SAPA_Aug2019-shapefile/SAPA_Aug2019-shapefile-polygons.shp"
protected_areas = gpd.read_file(protected_filepath)

### Where are the protected areas in South America? (Part 2)
### Create a plot that uses the protected_areas GeoDataFrame to show the locations of the protected areas in South America. (You'll notice that some protected areas are on land, while others are in marine waters.)
# Country boundaries in South America
south_america = americas.loc[americas['continent']=='South America']

# Your code here: plot protected areas in South America
ax = south_america.plot(figsize=(10,10), color='white', edgecolor='gray')
protected_areas.plot(ax=ax, alpha=0.4)

### What percentage of South America is protected?
### You're interested in determining what percentage of South America is protected, so that you know how much of South America is suitable for the birds.
### As a first step, you calculate the total area of all protected lands in South America (not including marine area). To do this, you use the "REP_AREA" and "REP_M_AREA" columns, which contain the total area and total marine area, respectively, in square kilometers.
P_Area = sum(protected_areas['REP_AREA']-protected_areas['REP_M_AREA'])
print("South America has {} square kilometers of protected areas.".format(P_Area))
# South America has 5396761.9116883585 square kilometers of protected areas.

south_america.head()
'''
	pop_est	continent	name	iso_a3	gdp_md_est	geometry
9	44938712.0	South America	Argentina	ARG	445445	MULTIPOLYGON (((-68.63401 -52.63637, -68.25000...
10	18952038.0	South America	Chile	CHL	282318	MULTIPOLYGON (((-68.63401 -52.63637, -68.63335...
20	3398.0	South America	Falkland Is.	FLK	282	POLYGON ((-61.20000 -51.85000, -60.00000 -51.2...
28	3461734.0	South America	Uruguay	URY	56045	POLYGON ((-57.62513 -30.21629, -56.97603 -30.1...
29	211049527.0	South America	Brazil	BRA	1839758	POLYGON ((-53.37366 -33.76838, -53.65054 -33.2...
'''

### Calculate the total area of South America by following these steps:
### Calculate the area of each country using the area attribute of each polygon (with EPSG 3035 as the CRS), and add up the results. The calculated area will be in units of square meters.
### Convert your answer to have units of square kilometeters.
# Your code here: Calculate the total area of South America (in square kilometers)
totalArea = sum(south_america.geometry.to_crs(epsg=3035).area) / 10**6
# What percentage of South America is protected?
percentage_protected = P_Area/totalArea
print('Approximately {}% of South America is protected.'.format(round(percentage_protected*100, 2)))
# Approximately 30.39% of South America is protected.

### Where are the birds in South America?
### So, are the birds in protected areas?
### Create a plot that shows for all birds, all of the locations where they were discovered in South America. Also plot the locations of all protected areas in South America.
### To exclude protected areas that are purely marine areas (with no land component), you can use the "MARINE" column (and plot only the rows in protected_areas[protected_areas['MARINE']!='2'], instead of every row in the protected_areas GeoDataFrame).
ax = south_america.plot(figsize=(10,10), color='white', edgecolor='gray')
protected_areas[protected_areas['MARINE']!='2'].plot(ax=ax, alpha=0.4, zorder=1)
birds[birds.geometry.y < 0].plot(ax=ax, color='red', alpha=0.6, markersize=10, zorder=2)

