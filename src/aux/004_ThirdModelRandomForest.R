## Random Forest with dummy variables ------------------------------------------
## 2018-04-28

# Required libraries
listPackages <- c('caret', 'corrplot', 'dummies', 'recipes', 'data.table', 
                  'tidyverse', 'lubridate', 'doMC', 'tree')
newPackages <- listPackages[!(listPackages %in% installed.packages()[,'Package'])]
if(length(newPackages)) install.packages(newPackages)

rm(list = c('listPackages', 'newPackages'))

library(data.table)
library(tidyverse)
library(lubridate)
library(caret)    # For modelization
library(corrplot) # For creating correlation charts
library(dummies)  # For creating dummy variables
library(recipes)  # For feature transformation
library(doMC)     # For paralelization
registerDoMC(cores = 8)
library(tree)

# Load dataset
load(file = './data/datasetCarsMinimal')

# Select interesting variables (we remove model because of it has a lot of levels, > 32)
datasetCarsMinimal <- datasetCarsMinimal[, c('price', 'vehicleType', 'yearOfRegistration',
                                             'gearbox', 'powerPSLog','kilometerCategorical', 'fuelType',
                                             'brand', 'notRepairedDamage')]

# Remove rands with few observations in order to get only 32 factors
brands <- datasetCarsMinimal %>% 
  group_by(brand) %>% 
  summarise(N =n()) %>% 
  arrange(desc(N)) %>% 
  head(32)
brands <- as.vector(brands$brand)

#Filtering by these 32 brands and refactor
datasetCarsMinimal <- datasetCarsMinimal[brand %in% brands]
datasetCarsMinimal$brand <- as.character(datasetCarsMinimal$brand)
datasetCarsMinimal$brand <- as.factor(datasetCarsMinimal$brand)

# Creation of train and test datasets
set.seed(42)
indexMinimal <- createDataPartition(y = datasetCarsMinimal$price, p = 0.8, list = F)
trainMinimal <- datasetCarsMinimal[indexMinimal,]
testMinimal <- datasetCarsMinimal[-indexMinimal,]


##### ALL THIS SECTION COULD BE COMMENTED ##### --------------------------------
# # Checking if predictors have 0 variance
# datasetCarsMinimal %>% select(-price) %>% nearZeroVar(saveMetrics = T)
# # Perfect, we can use all predictors!
# 
# # Creation of a recipe object
# recipeObject <- recipe(price ~ .,
#                        data = trainMinimal)
# 
# recipeObject <- recipeObject %>% step_nzv(all_predictors())
# recipeObject <- recipeObject %>% step_center(all_numeric())
# recipeObject <- recipeObject %>% step_scale(all_numeric())
# 
# # Creation of dummy vriables
# recipeObject <- recipeObject %>% step_dummy(all_nominal(), -all_outcomes())
# 
# # Applying recipe to train data
# trainedRecipe <- prep(recipeObject, training = trainMinimal)
# trainedRecipe
# 
# # Generation of dummied data frames
# trainMinimalPrep <- bake(trainedRecipe, newdata = trainMinimal)
# testMinimalPrep <- bake(trainedRecipe, newdata = testMinimal)
# 
# ## Recursive feature deletion
# subsets <- c(3:51308)
# repetitions <- 10
# 
# set.seed(42)
# seeds <- vector(mode = 'list', length = repetitions + 1)
# for (i in 1:repetitions){
#   seeds[[i]] <- sample.int(100000, length(subsets))
# }
# 
# seeds[[repetitions + 1]] <- sample.int(1000, 1)
# 
# # Se crea un control de entrenamiento donde se define el tipo de modelo empleado
# # para la selección de variables, en este caso random forest, la estrategia de
# # resampling, en este caso bootstrapping con 30 repeticiones, y las semillas para
# # cada repetición. Con el argumento returnResamp = "all" se especifica que se
# # almacene la información de todos los modelos generados en todas las repeticiones.
# 
# ctrlRfe <- rfeControl(functions = rfFuncs, method = 'boot', number = repetitions,
#                       returnResamp = 'all', allowParallel = T, verbose = T, seeds = seeds)
# 
# # Se ejecuta la eliminación recursiva de predictores
# set.seed(42)
# rf_rfe <- rfe(price ~ ., data = trainMinimalPrep, size = subsets, metric = 'Accuracy',
#               ntree = 500)

# Random forest using 'tree' library -------------------------------------------
set.seed(42)
train <- sample(1:nrow(datasetCarsMinimal), size = nrow(datasetCarsMinimal)/2)
regressTree <- tree(formula = price ~ ., 
                    data = datasetCarsMinimal, 
                    subset = train, 
                    split = 'deviance')
summary(regressTree)
regressTree
plot(regressTree, type = 'proportional')
text(regressTree, splits = T, pretty = 0, cex = .8, col = 'red')

# Pruning the tree
set.seed(42)
cvRegresTree <- cv.tree(regressTree, K = 10)
cvRegresTree

# Plot results
resultsCV <- data.table(nNodes = cvRegresTree$size,
                        deviance = cvRegresTree$dev,
                        alpha = cvRegresTree$k)
ggplot(data = resultsCV,
       mapping = aes(x = nNodes, y = deviance)) +
  geom_line() + 
  geom_point() +
  labs(title = 'Error vs tree size')

ggplot(data = resultsCV,
       mapping = aes(x = alpha, y = deviance)) +
  geom_line() + 
  geom_point() +
  labs(title = 'Error vs alpha')

# The lowest error is 10 nodes, so we should accept the first model

# Let's go to predict
predictions <- predict(regressTree, newdata = datasetCarsMinimal[-train,])
test_mse <- mean((predictions - datasetCarsMinimal[-train, 'price'])^2)
test_squaed_mse <- sqrt(test_mse)
# The prediction is not very good

# Comparing predictions with test data
comparison <- data.table(pred = predictions, 
                         obs = datasetCarsMinimal[-train, 'price'])
comparison[, diff := pred - obs.price]
