## Mapping data ---------------------------------------------------------------
## 2018-05-06
## https://gist.github.com/lmullen/8375785



# Required libraries
listPackages <- c('rgdal', 'ggplot2', 'ggmap', 'plotly', 'tidyverse')
newPackages <- listPackages[!(listPackages %in% installed.packages()[,'Package'])]
if(length(newPackages)) install.packages(newPackages)

rm(list = c('listPackages', 'newPackages'))


library(rgdal)
library(ggplot2)
library(ggmap)
library(plotly)
library(tidyverse)

# shapefile <- readOGR('~/Dropbox/MOOCs/KSCHOOL/DATA SCIENCE/TFM/plz-gebiete.shp/', 'plz-gebiete')
# 
# map <- ggplot() +
#   geom_path(data = shapefile,
#             mapping = aes(x = long, y = lat, group = group),
#             color = 'gray',
#             size = .1) +
#   theme_minimal()
# map
# 
# # xx <- fortify(shapefile)
# # write.csv2(xx, './shapefileCPlemania.csv', row.names = F)
# 
# lander <- readOGR(dsn = '../GermanyShapefile/', layer = 'VG250_Bundeslaender', encoding = 'ISO-8859-15')
# kreise <- readOGR(dsn = '../GermanyShapefile/', layer = 'VG250_Kreise', encoding = 'ISO-8859-15')
# gemeinen <- readOGR(dsn = '../GermanyShapefile/', layer = 'VG250_Gemeinden', encoding = 'ISO-8859-15')
# Verwaltungsgemeinschaften <- readOGR(dsn = '../GermanyShapefile/', layer = 'VG250_Verwaltungsgemeinschaften', encoding = 'ISO-8859-15')
# 
# map <- ggplot() +
#   geom_path(data = lander,
#             mapping = aes(x = long, y = lat, group = group),
#             color = 'gray',
#             size = .1) +
#   theme_minimal()
# map
# 
# ## New shapefiles --------------------------------------------------------------
# shapefiles <- list.files(path = '~/Dropbox/MOOCs/KSCHOOL/DATA SCIENCE/TFM/gadm36_DEU_shp/',
#                          pattern = '\\.shp') %>% 
#   str_sub(start = 1, end = -5)
# 
# # tst <- readOGR(dsn = '../gadm36_DEU_shp/', layer = shapefiles[1])
#   
# for (shapefile in shapefiles){
#   shape <- readOGR(dsn = '../gadm36_DEU_shp/',
#                    layer = shapefile)
#   mapa <- ggplot() +
#     geom_path(data = shape,
#               mapping = aes(x = long, y = lat, group = group))
#   print(mapa)
# }
# 
# shape <- readOGR(dsn = '../gadm36_DEU_shp/',
#                  layer = 'gadm36_DEU_2')




## Acquire datashape data ------------------------------------------------------
# Download dataset from Dropbox
download.file(url = 'https://www.dropbox.com/s/xuupzr8rfpeekyc/VG250_1Jan2011_WGS84.zip?dl=1',
              destfile = './data/VG250_1Jan2011_WGS84.zip')
unzip(zipfile = './data/VG250_1Jan2011_WGS84.zip', exdir = './data/Germany_shapefile/')
shapefile <- readOGR('./data/Germany_shapefile/', layer = 'VG250_Bundeslaender', encoding = 'ISO-8859-15')
load(file = './data/datasetCarsFinal')

map <- ggplot() +
  geom_path(data = shapefile,
            mapping = aes(x = long, y = lat, group = group),
            color = 'black',
            size = .1) +
  theme_minimal()
map

map_data_fortified <- fortify(shapefile) %>% 
  mutate(id = as.numeric(id) + 1)

dfDummy <- data.frame(state = shapefile@data$GEN,
                      id = as.integer(shapefile@data$GEN))

map_data_merged <- left_join(map_data_fortified, dfDummy, by = 'id')
