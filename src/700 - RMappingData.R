## Mapping data ---------------------------------------------------------------
## 2018-05-06
## https://gist.github.com/lmullen/8375785



# Required libraries
listPackages <- c('rgdal', 'ggplot2', 'ggmap', 'plotly')
newPackages <- listPackages[!(listPackages %in% installed.packages()[,'Package'])]
if(length(newPackages)) install.packages(newPackages)

rm(list = c('listPackages', 'newPackages'))


library(rgdal)
library(ggplot2)
library(ggmap)
library(plotly)

shapefile <- readOGR('~/Dropbox/MOOCs/KSCHOOL/DATA SCIENCE/TFM/plz-gebiete.shp/', 'plz-gebiete')

map <- ggplot() +
  geom_path(data = shapefile,
            mapping = aes(x = long, y = lat, group = group),
            color = 'gray',
            size = .1) +
  theme_minimal()
map

# xx <- fortify(shapefile)
# write.csv2(xx, './shapefileCPlemania.csv', row.names = F)

lander <- readOGR(dsn = '../GermanyShapefile/', layer = 'VG250_Bundeslaender', encoding = 'ISO-8859-15')
kreise <- readOGR(dsn = '../GermanyShapefile/', layer = 'VG250_Kreise', encoding = 'ISO-8859-15')
gemeinen <- readOGR(dsn = '../GermanyShapefile/', layer = 'VG250_Gemeinden', encoding = 'ISO-8859-15')
Verwaltungsgemeinschaften <- readOGR(dsn = '../GermanyShapefile/', layer = 'VG250_Verwaltungsgemeinschaften', encoding = 'ISO-8859-15')

map <- ggplot() +
  geom_path(data = kreise,
            mapping = aes(x = long, y = lat, group = group),
            color = 'gray',
            size = .1) +
  theme_minimal()
map
