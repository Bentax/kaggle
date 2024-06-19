import geopandas as gpd

####### There are many, many different geospatial file formats, such as shapefile, GeoJSON, KML, and GPKG. 
####### We won't discuss their differences in this micro-course, but it's important to mention that:
####### shapefile is the most common file type that you'll encounter, and
####### all of these file types can be quickly loaded with the gpd.read_file() function.
####### The next code cell loads a shapefile containing information about forests, wilderness areas, and other lands under the care of the Department of 
####### Environmental Conservation in the state of New York.

full_data = gpd.read_file("../input/geospatial-learn-course-data/DEC_lands/DEC_lands/DEC_lands.shp")

type(full_data)
# geopandas.geodataframe.GeoDataFrame

data = full_data.loc[:, ["CLASS", "COUNTY", "geometry"]].copy()

data.CLASS.value_counts()
'''
WILD FOREST                   965
INTENSIVE USE                 108
PRIMITIVE                      60
WILDERNESS                     52
ADMINISTRATIVE                 17
UNCLASSIFIED                    7
HISTORIC                        5
PRIMITIVE BICYCLE CORRIDOR      4
CANOE AREA                      1
Name: CLASS, dtype: int64
'''

# Select lands that fall under the "WILD FOREST" or "WILDERNESS" category
wild_lands = data.loc[data.CLASS.isin(['WILD FOREST', 'WILDERNESS'])].copy()
wild_lands.head()
'''
	CLASS	COUNTY	geometry
0	WILD FOREST	DELAWARE	POLYGON ((486093.245 4635308.586, 486787.235 4...
1	WILD FOREST	DELAWARE	POLYGON ((491931.514 4637416.256, 491305.424 4...
2	WILD FOREST	DELAWARE	POLYGON ((486000.287 4635834.453, 485007.550 4...
3	WILD FOREST	GREENE	POLYGON ((541716.775 4675243.268, 541217.579 4...
4	WILD FOREST	ESSEX	POLYGON ((583896.043 4909643.187, 583891.200 4...
'''

######## Create your first map!
wild_lands.plot()

######## The "geometry" column in our dataset contains 2983 different Polygon objects, each corresponding to a different shape in the plot above.
######## In the code cell below, we create three more GeoDataFrames, containing campsite locations (Point), foot trails (LineString), and county boundaries (Polygon).
# Campsites in New York state (Point)
POI_data = gpd.read_file("../input/geospatial-learn-course-data/DEC_pointsinterest/DEC_pointsinterest/Decptsofinterest.shp")
campsites = POI_data.loc[POI_data.ASSET=='PRIMITIVE CAMPSITE'].copy()

# Foot trails in New York state (LineString)
roads_trails = gpd.read_file("../input/geospatial-learn-course-data/DEC_roadstrails/DEC_roadstrails/Decroadstrails.shp")
trails = roads_trails.loc[roads_trails.ASSET=='FOOT TRAIL'].copy()

# County boundaries in New York state (Polygon)
counties = gpd.read_file("../input/geospatial-learn-course-data/NY_county_boundaries/NY_county_boundaries/NY_county_boundaries.shp")

######### Next, we create a map from all four GeoDataFrames.
######### The plot() method takes as (optional) input several parameters that can be used to customize the appearance. Most importantly, setting a value for ax ensures that all of the information is plotted on the same map.
# Define a base map with county boundaries
ax = counties.plot(figsize=(10,10), color='none', edgecolor='gainsboro', zorder=3)

# Add wild lands, campsites, and foot trails to the base map
wild_lands.plot(color='lightgreen', ax=ax)
campsites.plot(color='maroon', markersize=2, ax=ax)
trails.plot(color='black', markersize=1, ax=ax)

