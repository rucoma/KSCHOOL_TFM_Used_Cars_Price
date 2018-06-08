## Data cleaning process -------------------------------------------------------
## 2018-04-23

# Required libraries
listPackages <- c('data.table', 'tidyverse', 'lubridate', 'funModeling', 'forcats')
newPackages <- listPackages[!(listPackages %in% installed.packages()[,'Package'])]
if(length(newPackages)) install.packages(newPackages)

rm(list = c('listPackages', 'newPackages'))

library(data.table)
library(tidyverse)
library(lubridate)
library(funModeling)
library(forcats)

## Acquire data ----------------------------------------------------------------
# Download dataset from Dropbox
download.file(url = "https://www.dropbox.com/s/3802ph0qspdgtao/autos.csv?dl=1",
              destfile = './data/autos.csv')
download.file(url = "https://www.dropbox.com/s/uzzhu05061xjm0z/zipcodes_de_completo.csv?dl=1",
              destfile = './data/zipcodes_de_completo.csv')

# Load dataset
filename <- './data/autos.csv'
datasetCars <- fread(input = filename, 
                     stringsAsFactors = TRUE, 
                     quote = "",
                     colClasses = c(rep(x = 'factor', 4),
                                    'numeric',
                                    rep(x = 'factor', 2),
                                    'numeric',
                                    'factor',
                                    'numeric',
                                    'factor',
                                    rep('numeric', 2),
                                    rep('factor', 7)))

# Data exploration -------------------------------------------------------------
head(datasetCars)
str(datasetCars)
df_status(datasetCars)
# describe(datasetCars)
summary(datasetCars)

# Some variables won't be necessary for the model:
# datasetCars[, dateCreated := str_sub(string = dateCreated, start = 1, end = 10)]
# datasetCars[, dateCreated := ymd(dateCreated)]  ## as.Date(dateCreated, format = '%Y-%m%d %H:%M:%S')
# hist(datasetCars$dateCreated, breaks = 'months')
# dateCreated could be removed from dataset as well
deleteCols <- c('dateCrawled', 'dateCreated', 'nrOfPictures', 'lastSeen', 'name', 'abtest')
datasetCars[, (deleteCols) := NULL]

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


# Distribution of categorical variables ----------------------------------------
categoricalCols <- c('seller', 'offerType', 'vehicleType', 'gearbox', 'fuelType', 'notRepairedDamage')
# lapply(datasetCars[, ..categoricalCols], table, useNA = 'always')
datasetCarsCategorical <- datasetCars[, ..categoricalCols ]
# Long Format to better visualization
datasetCarsCategorical <- datasetCarsCategorical %>% gather()
ggplot(datasetCarsCategorical, aes(value)) +
  geom_bar() +
  coord_flip() +
  facet_wrap(~ key, scales = 'free_y') +
  theme_light()
# We are going to remove all NA values unles from notRepairedDamage variable (NA will be converted to 'Not applicable')
# Brands chart
ggplot(datasetCars, aes(x = fct_infreq(brand))) +
  geom_bar() +
  coord_flip() + 
  theme_light() +
  xlab('Brand') +
  ylab('Count') +
  labs(title = 'Frequency ob brands in dataset')
# Models chart
# ggplot(datasetCars, aes(x = fct_infreq(model))) +
#   geom_bar() +
#   coord_flip() + 
#   theme_light() +
#   xlab('Model') +
#   ylab('Count') +
#   labs(title = 'Frequency ob models in dataset')


# Histograms of numeric variables ----------------------------------------------
numericalCols <- c('price', 'yearOfRegistration', 'powerPS', 'kilometer', 'monthOfRegistration')
datasetCarsNumerical <- datasetCars[, ..numericalCols]
# Long Format to better visualization
datasetCarsNumerical <- datasetCarsNumerical %>% gather()
# Charting
ggplot(datasetCarsNumerical, aes(x=value)) +
  geom_histogram(bins = 20) +
  facet_wrap(~key, scales = 'free') +
  theme_light()
# It seems kilometer is a categorical variable
# Month of registration = 0?? Quite strange
# Power PS, price and year of registration have a lot of outliers!!
rm(list = c('categoricalCols', 'datasetCarsCategorical', 'datasetCarsNumerical', 'numericalCols', 'deleteCols', 'filename'))

# Cleaning the dataset. Removing NA and invalid cases --------------------------
# Price
datasetCars[price == max(price)]
datasetCars[price == min(price)]
# Some prices will be dropped from dataset:
datasetCars <- datasetCars[price > 200 & price <= 200000]

# Year of registration
datasetCars[yearOfRegistration == max(yearOfRegistration)]
datasetCars[yearOfRegistration == min(yearOfRegistration)]
# Some years will be dropped from dataset as well
datasetCars <- datasetCars[yearOfRegistration > 1950 & yearOfRegistration < 2018]

# Kilometer
datasetCars[kilometer == max(kilometer)]
datasetCars[kilometer == min(kilometer)]

# kilometer variable: (seems to be categorical, could refactor)
datasetCars[, kilometerCategorical := cut(x = kilometer,
                                          breaks = c(0, 50000, 100000, 150000),
                                          labels = c('km<50000', '50000>km<100000', 'km>100000'))]

# Power PS
datasetCars[powerPS == max(powerPS)]
datasetCars[powerPS == min(powerPS)]
datasetCars <- datasetCars[powerPS > 0 & powerPS <= 500]

# Recodification no repaired damage
datasetCars[is.na(notRepairedDamage), notRepairedDamage := 'Not applicable']

# We are not interested in auctions, only in direct sales
datasetCars <- datasetCars[offerType != 'Gesuch']
# We want only privat sellers
datasetCars <- datasetCars[seller == 'privat']
# Removing model 'andere' = 'other'
datasetCars <- datasetCars[model != 'andere']

# Minimal dataset (removing samples with empty values and unused features)
datasetCarsFinal <- datasetCars[!is.na(vehicleType) &
                                    !is.na(gearbox) &
                                    !is.na(fuelType) &
                                    !is.na(brand) &
                                    !is.na(model) &
                                    !is.na(notRepairedDamage),
                                  c('price', 'vehicleType', 'yearOfRegistration',
                                    'gearbox', 'powerPS','kilometerCategorical', 
                                    'fuelType', 'brand', 'model', 'notRepairedDamage',
                                    'postalCode', 'kilometer')]

# Merge brand and model --------------------------------------------------------
datasetCarsFinal[, brandModel := paste(brand, model, sep = ' ')]

# Merge with postal Code Database ----------------------------------------------
zipcodes <- fread(input = './data/zipcodes_de_completo.csv',
                  select = c('zipcode', 'state', 'community'),
                  colClasses = c(rep('character', 11)))
zipcodes <- zipcodes[!duplicated(zipcodes)]
colnames(zipcodes)[1] <- 'postalCode'
datasetCarsFinal <- zipcodes[datasetCarsFinal, on = 'postalCode']
datasetCarsFinal <- datasetCarsFinal[!is.na(datasetCarsFinal$state),]

# Pretty Names -----------------------------------------------------------------
datasetCarsFinal[, `:=` (brand = toupper(brand),
                         model = toupper(model))]
datasetCarsFinal[, `:=` (brand = gsub(pattern = '_', replacement = ' ', x = brand))]
# Save dataset -----------------------------------------------------------------
save(datasetCars, file = './data/datasetCars')
save(datasetCarsFinal, file = './data/datasetCarsFinal')

fwrite(datasetCarsFinal, file = './data/autosFinal.csv', row.names = F)

# Delete unused objects
rm(list = ls())
