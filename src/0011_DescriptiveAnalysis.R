library(data.table)
library(tidyverse)

byState <- datasetCarsFinal[, .(N = .N,
                                averagePrice = mean(price),
                                sdPrice = sd(price)), 
                            by = state]
byState

ggplot(datasetCarsFinal,
       aes(x = factor(state),
           y = price)) +
  geom_boxplot()

byBrand <- datasetCarsFinal[, .(N = .N,
                                averagePrice = mean(price),
                                sdPrice = sd(price)), 
                            by = brand]
byBrand
ggplot(datasetCarsFinal,
       aes(x = factor(brand),
           y = price)) +
  geom_boxplot()

byFuelType <- datasetCarsFinal[, .(N = .N,
                                averagePrice = mean(price),
                                sdPrice = sd(price)), 
                            by = fuelType]
byFuelType
ggplot(datasetCarsFinal,
       aes(x = factor(fuelType),
           y = price)) +
  geom_boxplot()

ggplot(datasetCarsFinal,
       aes(x = yearOfRegistration,
           y = log(price))) +
  geom_point() +
  geom_smooth(method = 'lm') +
  facet_wrap(brand ~ .)
