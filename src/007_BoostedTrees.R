## Boosted trees methodology
## 2018-06-23

# Required libraries
listPackages <- c('data.table', 'tidyverse', 'lubridate', 'forcats', 
                  'gbm', 'tree', 'gdata', 'ggpubr', 'caret')
newPackages <- listPackages[!(listPackages %in% installed.packages()[,'Package'])]
if(length(newPackages)) install.packages(newPackages)

rm(list = c('listPackages', 'newPackages'))


library(lubridate)
library(tidyverse)
library(data.table)
library(lubridate)
library(gbm)
library(tree)
library(gdata)
library(ggpubr)
library(caret)

# Loading the dataset ----------------------------------------------------------
load(file = './data/datasetCarsFinal')

datasetCarsFinal <- datasetCarsFinal[, c('state', 'vehicleType', 'yearOfRegistration', 
                                         'gearbox', 'powerPS', 'kilometerCategorical', 'fuelType', 
                                         'notRepairedDamage', 'brandModel','price')]

# Creating train and test datasets ---------------------------------------------
set.seed(123)
trainIdx <- sample(1:nrow(datasetCarsFinal), size = nrow(datasetCarsFinal) * 0.8)

train <- datasetCarsFinal[trainIdx,]
test <- datasetCarsFinal[-trainIdx,]

# Boosted ----------------------------------------------------------------------
system.time(
  {
    arbol_boosting <- gbm(price ~ ., data = train,
                          distribution = "gaussian",
                          n.trees = 1447,
                          interaction.depth = 5,
                          shrinkage = 0.01,
                          n.minobsinnode = 1,
                          bag.fraction = 0.5)
    
  }
)

test_prediction <- predict(object = arbol_boosting, newdata = test, n.trees = 1447)

Train_RSq <- (cor(arbol_boosting$fit, train$price))^2
Test_Rsq <- (cor(test_prediction, test$price))^2

Train_MSE <- mean((arbol_boosting$fit - train$price)^2)
Test_MSE <- mean((test_prediction - test$price)^2)

# Searching best hyperparameters with caret
set.seed(123)
validation <- trainControl(method = 'cv',
                           number = 10)
tuning_grid <- expand.grid(interaction.depth = 1,
                           n.trees = c(100, 1000),
                           shrinkage = c(.1, .01, .001),
                           n.minobsinnode = c(1, 10, 20))
system.time(
  best_model <- train(price ~  .,
                      data = train,
                      method = 'gbm',
                      trControl = validation,
                      verbose = T,
                      tuneGrid = tuning_grid)
  
)

## Function to predict new data from user --------------------------------------
asignaFactor <- function(
  state=NULL,
  vehicleType=NULL,
  yearOfRegistration=NULL,
  gearbox=NULL,                         
  powerPS=NULL,
  kilometerCategorical=NULL,
  fuelType=NULL,
  notRepairedDamage=NULL,
  brandModel=NULL
){
  prediction <- data.frame(
    state=factor(state, levels = levels(datasetCarsFinal$state)),
    vehicleType=factor(vehicleType, levels = levels(datasetCarsFinal$vehicleType)),
    yearOfRegistration=yearOfRegistration,
    gearbox=factor(gearbox, levels = levels(datasetCarsFinal$gearbox)),
    powerPS=powerPS,
    kilometerCategorical=factor(kilometerCategorical, levels = levels(datasetCarsFinal$kilometerCategorical)),
    fuelType=factor(fuelType, levels = levels(datasetCarsFinal$fuelType)),
    notRepairedDamage=factor(notRepairedDamage, levels = levels(datasetCarsFinal$notRepairedDamage)),
    brandModel=factor(brandModel, levels = levels(datasetCarsFinal$brandModel))
  )
  return(prediction)
}

prediccion <- asignaFactor(state = "Bayern",
                           vehicleType = "coupe",
                           yearOfRegistration = 2016,
                           gearbox = "automatik",
                           powerPS = 90,
                           kilometerCategorical = "km<50000",
                           fuelType = "benzin",
                           notRepairedDamage = "nein",
                           brandModel = "mercedes_benz s_klasse")

predict(object = arbol_boosting,
        newdata = prediccion,
        n.trees = 1447)#,
# type = 'response')
