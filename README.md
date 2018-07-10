# KSchool I Data Science Master

## Final project: Price prediction model of used cars

From a dataset from [Kaggle](https://www.kaggle.com/orgesleka/used-cars-database), consisting in 370k samples of used cars on sale on [eBay Classifieds Germany](https://www.ebay-kleinanzeigen.de/) we will try to build a predictive model that gives us information about the approximate sales price at which users should put their cars on the website.

### Dataset description:  
Dataset contains different descriptive features of the vehicles like brand, model, vehicle type, year of registration, kilometers, etc. These are the features of the original dataset:
* dateCrawled : when this ad was first crawled, all field-values are taken from this date. Won't be used in the project.
* name : "name" of the ad. Won't be used in the project.
* seller : private or dealer
* offerType: Angebot (offer) or Gesuch (petition)
* price : the price on the ad in Euros
* abtest: eBay internal data. Won't be used in the project.
* vehicleType: coupe, SUV, cabrio, limousine, etc
* yearOfRegistration : at which year the car was first registered
* gearbox: Type of transmission
* powerPS : power of the car in PS
* model
* kilometer : how many kilometers the car has driven
* monthOfRegistration : at which month the car was first registered
* fuelType: benzin, diesel, elektro, etc
* brand
* notRepairedDamage : if the car has a damage which is not repaired yet
* dateCreated : the date for which the ad at ebay was created. Won't be used in the project.
* nrOfPictures : number of pictures in the ad (this field contains only 0, won't use)
* postalCode
* lastSeenOnline : when the crawler saw this ad last online. Won't be used in the project.

### Project setup  
After cloning the repository it's necessary to install the Anaconda environment found in `./data/rucoma.yml`.  
Project is based on Jupyter notebooks. Both R and Python kernels are used, so it's important to activate the provided environment because R kernel is not included by default in Anaconda installation.

### Project steps:
* Data exploration and cleaning:
* Data visualization
* Modeling
* Prediction of price using new data.
