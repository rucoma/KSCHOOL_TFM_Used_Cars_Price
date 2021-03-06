## Mapping data ---------------------------------------------------------------
## 2018-05-06
## https://gist.github.com/lmullen/8375785



# Required libraries
listPackages <- c('rgdal', 'ggplot2', 'ggmap', 'plotly', 'tidyverse', 'data.table')
newPackages <- listPackages[!(listPackages %in% installed.packages()[,'Package'])]
if(length(newPackages)) install.packages(newPackages)

rm(list = c('listPackages', 'newPackages'))


library(rgdal)
library(ggplot2)
library(ggmap)
library(plotly)
library(tidyverse)
library(data.table)

# shapefile2 <- readOGR('~/Dropbox/MOOCs/KSCHOOL/DATA SCIENCE/TFM/plz-gebiete.shp/', 'plz-gebiete')
# 
map <- ggplot() +
  geom_path(data = shapefile2,
            mapping = aes(x = long, y = lat, group = group),
            color = 'gray',
            size = .1) +
  theme_minimal()
map

# xx <- fortify(shapefile2)
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



# Theme for maps ---------------------------------------------------------------
themeMaps <- theme(
  axis.title = element_blank(),
  axis.text.x = element_blank(),
  axis.text.y = element_blank(),
  axis.ticks = element_blank(),
  axis.line = element_blank(),
  legend.text = element_text(colour = '#2D4471', size = 10),
  legend.title = element_text(colour = '#2D4471', size = 12),
  plot.title = element_text(colour = '#2D4471', size = 18, face = 'bold'),
  plot.subtitle = element_text(colour = '#2D4471', size = 14),
  panel.background = element_rect(fill = '#FFFFFF'),
  legend.box.background = element_blank(),
  legend.key = element_blank(),
  panel.grid.major = element_blank(), 
  panel.grid.minor = element_blank()
)



## Acquire datashape data ------------------------------------------------------
# Download dataset from Dropbox
download.file(url = 'https://www.dropbox.com/s/xuupzr8rfpeekyc/VG250_1Jan2011_WGS84.zip?dl=1',
              destfile = './data/VG250_1Jan2011_WGS84.zip')
unzip(zipfile = './data/VG250_1Jan2011_WGS84.zip', exdir = './data/Germany_shapefile/')
shapefileLander <- readOGR('./data/Germany_shapefile/', layer = 'VG250_Bundeslaender', encoding = 'ISO-8859-15')
# shapefilePostal <- readOGR('~/Dropbox/MOOCs/KSCHOOL/DATA SCIENCE/TFM/plz-gebiete.shp/', layer = 'plz-gebiete', encoding = 'ISO-8859-15')
load(file = './data/datasetCarsFinal')

# Data for filling maps --------------------------------------------------------
avPriceLander <- datasetCarsFinal[, .(avPrice = mean(price)), by = state]
nCarsLander <- datasetCarsFinal[, .(N = .N), by = state]

# avPricePostal <- datasetCarsFinal[, .(avPrice = mean(price)), by = postalCode]
# nCarsPostal <- datasetCarsFinal[, .(N = .N), by = postalCode]

# Manipulate shapefile to create a data frame with all necessary data ----------
mapDataFortifiedLander <- fortify(shapefileLander) %>% 
  mutate(id = as.numeric(id)) %>% 
  setDT()

# mapDataFortifiedPostal <- fortify(shapefilePostal) %>% 
#   mutate(id = as.numeric(id)) %>% 
#   setDT()

dfLander <- data.frame(state = shapefileLander@data$GEN,
                      id = 0:20)

# dfPostal <- data.frame(postalCode = shapefilePostal@data$plz,
#                        id = )

centroids <- as.data.frame(coordinates(shapefileLander)) %>% 
  rename(long = V1, lat = V2) %>% 
  mutate(id = seq(0, nrow(.) - 1)) %>% 
  left_join(., dfLander, by ='id') %>% 
  setDT()

mapDataMergedLander <- left_join(mapDataFortifiedLander, dfLander, by = 'id') %>% 
  left_join(., avPriceLander, by = 'state') %>% 
  left_join(., nCarsLander, by = 'state') %>%
  setDT()

notNecessaryIds <- c(14, 4, 11, 6, 13)

# mapDataMergedPostal <- left_join(mapDataFortifiedPostal, avPricePostal, by = c('id' = '')) %>% 
#   setDT()

## Maps ------------------------------------------------------------------------
ggplot() +
  geom_path(data = mapDataMergedLander,
            mapping = aes(x = long, y = lat, group = group),
            color = 'black',
            size = .1) +
  geom_polygon(data = mapDataMergedLander,
               mapping = aes(x = long, y = lat, group = group, fill = avPrice)) +
  scale_fill_gradient(low = "white",
                      high = "#ff702f",
                      na.value = "grey",
                      space = "Lab",
                      name = 'Average \nprice') +
  geom_point(data = centroids[!(id %in% notNecessaryIds)],
             mapping = aes(x = long,
                           y = lat),
             colour ='#2D4471') +
  coord_map(projection = 'mercator') +
  geom_text(data = centroids[!(id %in% notNecessaryIds)],
            mapping = aes(x = long,
                          y = lat,
                          label = as.character(state)),
            size = 3,
            colour ='#2D4471',
            nudge_y = -0.15) +
  labs(title = 'Average price of cars on sale', subtitle = 'By Lander') +
  themeMaps

ggplot() +
  geom_path(data = mapDataMergedLander,
            mapping = aes(x = long, y = lat, group = group),
            color = 'black',
            size = .1) +
  geom_polygon(data = mapDataMergedLander,
               mapping = aes(x = long, y = lat, group = group, fill = N)) +
  scale_fill_gradient(low = "white",
                      high = "#ff702f",
                      na.value = "grey",
                      space = "Lab",
                      name = 'Number \nof cars') +
  geom_point(data = centroids[!(id %in% notNecessaryIds)],
             mapping = aes(x = long,
                           y = lat),
             colour ='#2D4471') +
  coord_map(projection = 'mercator') +
  geom_text(data = centroids[!(id %in% notNecessaryIds)],
            mapping = aes(x = long,
                          y = lat,
                          label = as.character(state)),
            size = 3,
            colour ='#2D4471',
            nudge_y = -0.15) +
  labs(title = 'Number of cars on sale', subtitle = 'By Lander') +
  themeMaps
