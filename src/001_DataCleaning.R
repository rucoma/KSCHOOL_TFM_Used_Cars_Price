## Data cleaning ---------------------------------------------------------------
## 2018-04-23

# Required libraries
listPackages <- c('data.table', 'tidyverse', 'lubridate', 'funModeling')
newPackages <- listPackages[!(listPackages %in% installed.packages()[,'Package'])]
if(length(newPackages)) install.packages(newPackages)

rm(list = c('listPackages', 'newPackages'))

library(data.table)
library(tidyverse)
library(lubridate)
library(funModeling)

# Load dataset
filename <- './data/autos.csv'
datasetCars <- fread(input = filename, stringsAsFactors = TRUE)

# Data check
head(datasetCars)
str(datasetCars)

# Data exploration
df_status(datasetCars)
# describe(datasetCars)
summary(datasetCars)

# Missing values exploration
any(!complete.cases(datasetCars))
map_dbl(.x = datasetCars, .f = function(x){sum(is.na(x))})

# It seems there is not NA vaues in the dataset, let's try to detect '' values
map_lgl(.x = datasetCars, .f = function(x){any(is.na(x) | x == '')})
# There are some variables with '' values, so it is necessary to detect and evaluate
# if we will remove them or assign another value

# Whe have to converto to character prior to asign NA. We create a function to do so
assignNA <- function(column){
  column <- as.character(column)
  column[column == ''] <- NA
  column <- as.factor(column)
}

datasetCars$vehicleType <- assignNA(datasetCars$vehicleType)
datasetCars$gearbox <- assignNA(datasetCars$gearbox)
datasetCars$model <- assignNA(datasetCars$model)
datasetCars$fuelType <- assignNA(datasetCars$fuelType)
datasetCars$notRepairedDamage <- assignNA(datasetCars$notRepairedDamage)

map_dbl(.x = datasetCars, .f = function(x){sum(is.na(x))})
# Aha! a lot of NA have appeared!! Let's remove them later

# Some variables won't be necessary for the model:
datasetCars[, dateCreated := str_sub(string = dateCreated, start = 1, end = 10)]
datasetCars[, dateCreated := ymd(dateCreated)]  ## as.Date(dateCreated, format = '%Y-%m%d %H:%M:%S')
hist(datasetCars$dateCreated, breaks = 'months')
# dateCreated could be removed from dataset as well
deleteCols <- c('dateCrawled', 'dateCreated', 'monthOfRegistration', 'nrOfPictures', 'lastSeen')
datasetCars[, (deleteCols) := NULL]

# We are not interested in auctions, only in direct sales
datasetCars <- datasetCars[offerType != 'Gesuch']

# Let's visualize NA values
# datasetCarsLong <- datasetCars %>%
#   mutate(pos = 1:n()) %>%
#   gather(key = "variable", value = "value", -pos) %>%
#   mutate(absent = is.na(value)) %>%
#   setDT()
# 
# chartNA <-
#   ggplot(data = datasetCarsLong[variable %in% c('vehicleType', 'gearbox', 'model', 'fuelType', 'notRepairedDamage')],
#        mapping = aes(x = variable, y = pos, col = absent)) +
#   geom_point() +
#   scale_fill_manual(values = c("gray60", "orangered2")) +
#   theme_bw()
# 
# chartNA

# Price will be dependent variable. Some exploration first:
par(mfrow=c(3,1))
hist(datasetCars$price, breaks = 50)
hist(datasetCars$yearOfRegistration, breaks = 50)
hist(datasetCars$kilometer, breaks = 50)

datasetCars[price == max(price)]
datasetCars[price == min(price)]

datasetCars[yearOfRegistration == max(yearOfRegistration)]
datasetCars[yearOfRegistration == min(yearOfRegistration)]

datasetCars[kilometer == max(kilometer)]
datasetCars[kilometer == min(kilometer)]

# Some prices will be dropped from dataset:
datasetCars <- datasetCars[price > 0 & price <= 50000]

# Some years will be dropped from dataset as well
datasetCars <- datasetCars[yearOfRegistration > 1950 & yearOfRegistration < 2018]

# Now it looks better
par(mfrow=c(3,1))
hist(datasetCars$price)
hist(datasetCars$yearOfRegistration)
hist(datasetCars$kilometer)

## Some feature engineering here
# powerPS variable: (transform with log)
par(mfrow=c(2,1))
hist(datasetCars$powerPS, breaks = 100)
hist(log(datasetCars$powerPS), breaks = 100)
datasetCars$powerPSLog <- log(datasetCars$powerPS)
# with log transformation, powerPS = 0 should be removed
datasetCars <- datasetCars[powerPS > 0]


# kilometer variable: (seems to be categorical, could refactor)
datasetCars[, kilometerCategorical := cut(x = kilometer,
                                          breaks = c(0, 50000, 100000, 150000),
                                          labels = c('km<50000', '50000>km<100000', 'km>100000'))]

# Alternative dataset; Minimal (removing samples with empty values and unused features)
datasetCarsMinimal <- datasetCars[!is.na(vehicleType) &
                                    !is.na(gearbox) &
                                    !is.na(fuelType) &
                                    !is.na(brand) &
                                    !is.na(model) &
                                    !is.na(notRepairedDamage),
                                  c('price', 'vehicleType', 'yearOfRegistration',
                                    'gearbox', 'powerPSLog','kilometerCategorical', 'fuelType',
                                    'brand', 'notRepairedDamage')]

# Save dataset
save(datasetCars, file = './data/datasetCars')
save(datasetCarsMinimal, file = './data/datasetCarsMinimal')

fwrite(datasetCarsMinimal, file = './data/autosMinimal.csv', row.names = F)

# Delete unused objects
rm(list = ls())
