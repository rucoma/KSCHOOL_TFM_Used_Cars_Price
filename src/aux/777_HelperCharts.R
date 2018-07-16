library(data.table)
library(tidyverse)
library(ggmap)
library(plotly)
library(kableExtra)
library(scales)
library(corrplot)
library(gridExtra)
library(treemap)
library(RColorBrewer)
library(choroplethr)
library(choroplethrMaps)

load(file = './data/datasetCarsFinal')


themeCharts <- ggplot2::theme(
  axis.title = element_text(colour = '#2D4471', size = 14),
  axis.text.x = element_text(colour = '#2D4471', size = 12, angle = 90, vjust = .5),
  axis.text.y = element_text(colour = '#2D4471', size = 12),
  axis.ticks = element_line(colour = '#2D4471'),
  axis.line = element_line(colour = '#2D4471'),
  legend.text = element_text(colour = '#2D4471', size = 14),
  legend.title = element_text(colour = '#2D4471', size = 16),
  panel.grid.major = element_line(colour = 'gray95', linetype = 1), #'#2D4471'
  plot.title = element_text(colour = '#2D4471', size = 22, face = 'bold'),
  plot.subtitle = element_text(colour = '#2D4471', size = 16),
  panel.background = element_rect(fill = '#FFFFFF'),
  legend.box.background = element_blank(),
  legend.key = element_blank()
  )

## Numerical variables ---------------------------------------------------------

## Using data frame variables as arguments in custom function
plotNumerical <- function(df, xvar, yvar, xName, yName, tit, subtit = NULL) {
  ggplot(df,
         aes_string(x = xvar, 
                    y= yvar)) +
    geom_point(alpha = 0.2, color = '#D16666') +
    scale_x_continuous(name = xName) +
    scale_y_continuous(name = yName, labels = scales::dollar_format(prefix = '€')) +
    labs(title = tit, subtitle = subtit) +
    themeCharts
}

g1 <- plotNumerical(df = datasetCarsFinal, xvar = 'yearOfRegistration', yvar = 'price', xName = 'Year', yName = 'Price', tit = 'Price by Year')
g2 <- plotNumerical(df = datasetCarsFinal, xvar = 'powerPS', yvar = 'price', xName = 'Power PS', yName = 'Price', tit = 'Price by Power PS')
g3 <- plotNumerical(df = datasetCarsFinal, xvar = 'kilometer', yvar = 'price', xName = 'Kilometer', yName = 'Price', tit = 'Price by Kilometer')

grid.arrange(g1, g2, g3, nrow = 1)

gBoxplot1 <- ggplot(data = datasetCarsFinal,
                    mapping = aes(x = yearOfRegistration,
                                  y = price,
                                  group = yearOfRegistration)) +
  geom_boxplot(alpha = 0.1, color = '#D16666') +
  labs(title = 'Price boxplot by year', subtitle = NULL) +
  scale_x_continuous(name = 'Year', breaks = seq(1950, 2020, by = 10)) +
  scale_y_continuous(name = 'Price', labels = scales::dollar_format(prefix = '€')) +
  themeCharts
gBoxplot1

numericalCol <- c('yearOfRegistration', 'powerPS', 'kilometer', 'price')
datasetNumerical <- datasetCarsFinal[, ..numericalCol]

plot(datasetNumerical)

corrplot(cor(datasetNumerical), method = 'number', addCoef.col = T, type = 'lower', title = 'Correlation coefficients', outline = T, tl.pos = 'ld', number.cex = 1.25)

## Categorical variables
gBoxplot2 <- 
  ggplot(data = datasetCarsFinal,
                    mapping = aes(x = brand,
                                  y = price)) +
  geom_boxplot(alpha = 0.1, color = '#D16666') +
  geom_hline(yintercept = mean(datasetNumerical$price), linetype="dashed") +
  annotate(geom = 'text', x = 3, y = mean(datasetNumerical$price), label = paste0('Average price: ', sprintf('%4.0f €', round(mean(datasetNumerical$price), 0))), vjust = -.5) +
  labs(title = 'Price boxplot by brand', subtitle = NULL) +
  scale_x_discrete(name = 'Brand') +
  scale_y_log10(name = 'Price (log scale)', labels = scales::dollar_format(prefix = '€')) +
  
  themeCharts
gBoxplot2

gCountBrand <- 
  ggplot(data = datasetCarsFinal[, .(N = .N), by = brand][order(-N)],
       mapping = aes(x = reorder(brand, N),
                     y = N)) +
  geom_col(fill = '#D16666') +
  coord_flip() +
  labs(title = 'Brand count', subtitle = NULL) +
  scale_x_discrete(name = 'Brand') +
  scale_y_continuous(name = 'Count', labels = comma) +
  themeCharts
gCountBrand

vehicleTypeEvol <- 
  ggplot(datasetCarsFinal[yearOfRegistration > 1980 & yearOfRegistration < 2016, .(N = .N), by =.(yearOfRegistration, vehicleType)],
         aes(x = yearOfRegistration,
             y = N,
             color = vehicleType)) +
  geom_line(size = 1) +
  scale_color_brewer(palette = 'Set1', name = 'Vehicle type') +
  scale_x_continuous(name = 'Year', breaks = seq(1980, 2020, by = 10)) +
  scale_y_continuous(name = 'Count', labels = comma) +
  labs(title = 'Vehicle type evolution', subtitle = NULL) +
  themeCharts
vehicleTypeEvol

gearboxEvol <- 
  ggplot(datasetCarsFinal[yearOfRegistration > 1980 & yearOfRegistration < 2016, .(N = .N), by =.(yearOfRegistration, gearbox)],
         aes(x = yearOfRegistration,
             y = N,
             color = gearbox)) +
  geom_line(size = 1) +
  scale_color_brewer(palette = 'Set1', name = 'Gearbox') +
  scale_x_continuous(name = 'Year', breaks = seq(1980, 2020, by = 10)) +
  scale_y_continuous(name = 'Count', labels = comma) +
  labs(title = 'Gearbox type evolution', subtitle = NULL) +
  themeCharts
gearboxEvol

fuelTypeEvol <- 
  ggplot(datasetCarsFinal[yearOfRegistration > 1980 & yearOfRegistration < 2016, .(N = .N), by =.(yearOfRegistration, fuelType)],
         aes(x = yearOfRegistration,
             y = N,
             color = fuelType)) +
  geom_line(size = 1) +
  scale_color_brewer(palette = 'Set1', name = 'Fuel type') +
  scale_x_continuous(name = 'Year', breaks = seq(1980, 2020, by = 10)) +
  scale_y_continuous(name = 'Count', labels = comma) +
  labs(title = 'Fuel type evolution', subtitle = NULL) +
  themeCharts
fuelTypeEvol

grid.arrange(vehicleTypeEvol, gearboxEvol, fuelTypeEvol, nrow = 1)

# Treemap
brandPrice <- datasetCarsFinal[, .(N = .N, meanPrice = mean(price)), by = brand]
brandPrice$label <- paste(brandPrice$brand, format(round(brandPrice$meanPrice, 0), big.mark = '.', decimal.mark = ','), sep = ':')
treeMapBrands <- 
  treemap(dtf = brandPrice,
        index = c('label'),
        vSize = 'N',
        vColor = 'meanPrice',
        type = 'value',
        fontsize.title = 10,
        fontsize.labels = 10,
        title = 'Brands distribution \n Square size: number of cars \n Value: average price',
        border.lwds = 1,
        aspRatio = 3)


# portfolio::map.market(id = brandPrice$brand,
#                       area = brandPrice$N,
#                       color = brandPrice$meanPrice,
#                       group = brandPrice$brand,
#                       scale = 25000,
#                       main = "Size of the market")


## Geo data
# geoData <- datasetCarsFinal[, .(N = .N, averagePric = mean(price)), by = state]
