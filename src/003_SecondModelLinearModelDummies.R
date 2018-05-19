## Linear Model with dummy variables -------------------------------------------
## 2018-04-26

# Required libraries
listPackages <- c('caret', 'corrplot', 'dummies', 'data.table', 'tidyverse', 'lubridate')
newPackages <- listPackages[!(listPackages %in% installed.packages()[,'Package'])]
if(length(newPackages)) install.packages(newPackages)

rm(list = c('listPackages', 'newPackages'))

library(data.table)
library(tidyverse)
library(lubridate)
library(caret)
library(corrplot)
library(dummies)

# Load dataset
load(file = './data/datasetCarsMinimal')

# Select interesting variables and get dummies
datasetCarsMinimal <- datasetCarsMinimal[, c('price', 'vehicleType', 'yearOfRegistration',
                                             'gearbox', 'powerPS','kilometer', 'fuelType',
                                             'brand', 'model', 'notRepairedDamage')]
set.seed(42)
indexMinimal <- createDataPartition(y = datasetCarsMinimal$price, p = 0.8, list = F)
trainMinimal <- datasetCarsMinimal[indexMinimal,]
testMinimal <- datasetCarsMinimal[-indexMinimal,]

## Regression with R stats -----------------------------------------------------
modelDummyLM <- lm(price ~ ., data = trainMinimal, method = 'lm')
summary(modelDummyLM)
predictDummyLM <- predict(modelDummyLM)
RMSE(pred = predictDummyLM, obs = trainMinimal$price, na.rm = T)
# Not bad!!

## Regression with caret -------------------------------------------------------
set.seed(42)
# ctrl <- trainControl(method = 'cv', number = 2)
modelDummyCVLM <- train(price ~ .,
                      data = trainMinimal,
                      method = 'lm') #,
                      # trControl = ctrl,
                      #metric = "Rsquared")
summary(modelDummyCVLM)
