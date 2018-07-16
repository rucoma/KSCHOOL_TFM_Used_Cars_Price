## Trees methodology
## 2018-06-23

# Required libraries
listPackages <- c('data.table', 'tidyverse', 'lubridate', 'forcats', 'gbm', 'tree', 'gdata', 'ggpubr')
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

# Loading the dataset ----------------------------------------------------------
load(file = './data/datasetCarsFinal')

datasetCarsFinal <- datasetCarsFinal[, c('state', 'vehicleType', 'yearOfRegistration', 
                                  'gearbox', 'powerPS', 'kilometerCategorical', 'fuelType', 
                                  'notRepairedDamage', 'price')]


# Creating train and test datasets ---------------------------------------------
set.seed(123)
trainIdx <- sample(1:nrow(datasetCarsFinal), size = nrow(datasetCarsFinal) * 0.8)

train <- datasetCarsFinal[trainIdx,]
test <- datasetCarsFinal[-trainIdx,]

# Tree -------------------------------------------------------------------------
tree <- tree(price ~ .,
             data = train,
             split = 'deviance')
plot(tree, type = 'proportional')
text(tree, splits = T, pretty = 0, cex = .8, col = 'red')

# Pruning the tree
cv_tree <- cv.tree(tree, K = 10)
cv_tree

# Plotting results
results_cv <- data.frame(n_nodes = cv_tree$size,
                         dev = cv_tree$dev,
                         alpha = cv_tree$k)
g1 <- 
  ggplot(results_cv, aes(x = n_nodes, y = dev)) +
  geom_line() + 
  geom_point() +
  scale_x_continuous(breaks = 0:max(results_cv$n_nodes)) +
  labs(title = 'Error vs tree size') +
  theme_bw()
g2 <- 
  ggplot(results_cv, aes(x = alpha, y = dev)) +
  geom_line() + 
  geom_point() +
  labs(title = 'Error vs alpha') +
  theme_bw()

ggarrange(g1, g2)

# Tree pruning
tree_pruning <- prune.tree(tree = tree,
                           best = 12)
plot(tree_pruning, type = 'proportional')
text(tree_pruning, splits = T, pretty = 0, cex = .8, col = 'red')

# Tree evaluation
prediction_train <- predict(tree_pruning, newdata = datasetCarsFinal[trainIdx,])
prediction_test <- predict(tree_pruning, newdata = datasetCarsFinal[-trainIdx,])
train_mse <- mean((prediction_train - datasetCarsFinal[trainIdx, 'price'])^2)
test_mse <- mean((prediction_test - datasetCarsFinal[-trainIdx, 'price'])^2)

