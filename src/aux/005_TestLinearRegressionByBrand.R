library(data.table)
library(tidyverse)
autosFinal <- fread('./data/autosFinal.csv')


brands <- unique(autosFinal$brand)
dtResults <- data.table()

for (i in brands){
  print(i)
  model <- lm(formula = price ~ yearOfRegistration, data = autosFinal[brand == i])
  temp <- data.table(brand = i, alpha = model$coefficients[2])
  dtResults <- rbind(dtResults, temp)
}


