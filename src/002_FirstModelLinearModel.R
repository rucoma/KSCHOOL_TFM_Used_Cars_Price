## Linear Model ----------------------------------------------------------------
## 2018-04-24

# Required libraries
listPackages <- c('caret', 'corrplot', 'data.table', 'tidyverse', 'lubridate')
newPackages <- listPackages[!(listPackages %in% installed.packages()[,'Package'])]
if(length(newPackages)) install.packages(newPackages)

rm(list = c('listPackages', 'newPackages'))

library(data.table)
library(tidyverse)
library(lubridate)
library(caret)
library(corrplot)

# Load dataset
load(file = './data/datasetCarsMinimal')

# Check correlation between variables
par(mfrow = c(1, 1))
corrplot::corrplot(cor(datasetCarsMinimal[, c('price', 'yearOfRegistration', 'powerPSLog')]), 
                   method = 'number', 
                   type = 'lower')

# Plot variables against price
# plot(datasetCarsMinimal$yearOfRegistration, datasetCarsMinimal$price)
# Year of registration doesn't seem to be a valid variable to predict price
# plot(datasetCarsMinimal$kilometer, datasetCarsMinimal$price)

## Some feature engineering ----------------------------------------------------
# Scalate variables
# datasetCarsMinimal[, `:=` (priceScalated = scale(price),
#                     kilometerScaled = scale(kilometer),
#                     yearOfRegistrationScalated = scale(yearOfRegistration))]

# Split dataset in train and test
set.seed(42)
index <- createDataPartition(y = datasetCarsMinimal$price, p = 0.8, list = F)
train <- datasetCarsMinimal[index,]
test <- datasetCarsMinimal[-index,]

# Regression with R stats ------------------------------------------------------
# model <- lm(formula = price ~ yearOfRegistration, data = train)
# summary(model)
# 
# plot(datasetCarsMinimal$yearOfRegistration, datasetCarsMinimal$price)
# abline(model, col = 'red')

# Some feature engineering
# datasetCarsMinimal[, yearSqrt := sqrt(yearOfRegistration)]
# index <- createDataPartition(y = datasetCarsMinimal$price, p = 0.8, list = F)
# train <- datasetCarsMinimal[index,]
# test <- datasetCarsMinimal[-index,]
# # Did not work!!
# 
# model2 <- lm(formula = price ~ yearSqrt, data = train)
# summary(model2)
# plot(datasetCarsMinimal$yearSqrt, datasetCarsMinimal$price)
# abline(model2, col = 'red')
# plot(model)

## Regression with caret -------------------------------------------------------
# https://www.analyticsvidhya.com/blog/2014/12/caret-package-stop-solution-building-predictive-models/
set.seed(42)
# Linear regression
modelLM <- train(price ~ yearOfRegistration + powerPSLog, data = train, method = 'lm')
# modelLM <- train(priceScalated ~ yearOfRegistrationScalated, data = train, method = 'lm') # No mejora la prediccion con las variables escaladas
# modelLM <- train(priceScalated ~ yearOfRegistrationScalated + kilometerScaled, data = train, method = 'lm') # Anyadiendo los kilometros mejora algo
# modelLM <- train(price ~ yearOfRegistration, data = trainMinimal, method = 'lm')
summary(modelLM)
# Coefficients
coefIcept <- coef(modelLM$finalModel)
coefIcept

# Predicted
predictLM <- predict(modelLM)
RMSE(pred = predictLM, train$price, na.rm = T)

# Cross Validation
ctrl <- trainControl(method = 'cv', number = 10)
modelLMCV <- train(price ~ yearOfRegistration, 
                   data = train, 
                   method = 'lm', 
                   trControl = ctrl, 
                   metric = "Rsquared")
summary(modelLMCV)

# Predicted
predictLMCV <- predict(modelLMCV)
residuals <- resid(modelLMCV)
RMSE(pred = predictLMCV, train$price, na.rm = T)
plot(train$price, predictLMCV)
# varImp(modelLMCV) # Para mas de una variable

# Test
predictedTest <- predict(modelLMCV, test)
modelValues <- data.frame(obs = test$price, pred = predictedTest)
defaultSummary(modelValues)
summary(modelLMCV)
RMSE(pred = predictedTest, obs = test$price)

## Conclussion: This methodology does not work very well.
## Move on with another methodology