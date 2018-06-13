TFM: Used Cars Price Prediction
========================================================
author: Rubén Coca
date: June 15th, 2018
autosize: true

Introduction
========================================================

The main objective of the project is to create a prediction model for the price of used cars in a internet portal.  

The data has been downloaded from <https://www.kaggle.com>, and originally comes from <https://www.ebay.de>.

<center>
![car](../data/used_cars.jpg)
</center>

The dataset (I)
========================================================

Original dataset will be composed of:  

```
[1] "280602 samples and 15 features."
```

Features like brand, model, type of vehicle, type of fuel, number of kilometers, age, power or location will help to create a prediction model.  


The dataset (II)
========================================================

And this is the type of the features:  

```
          dateCrawled                 name seller offerType price abtest
1 2016-03-24 11:52:17           Golf_3_1.6 privat   Angebot   480   test
2 2016-03-24 10:58:45 A5_Sportback_2.7_Tdi privat   Angebot 18300   test
  vehicleType yearOfRegistration gearbox powerPS model kilometer
1                           1993 manuell       0  golf    150000
2       coupe               2011 manuell     190          125000
  monthOfRegistration fuelType      brand notRepairedDamage
1                   0   benzin volkswagen                  
2                   5   diesel       audi                ja
          dateCreated nrOfPictures postalCode            lastSeen
1 2016-03-24 00:00:00            0      70435 2016-04-07 03:16:57
2 2016-03-24 00:00:00            0      66954 2016-04-07 01:46:50
```


The target
========================================================

Price will be the target variable



Methodology
========================================================


The repository
========================================================

All the code and necessary data is available at this GitHub repository:  
<https://github.com/rucoma/KSCHOOL_TFM_Used_Cars_Price>
