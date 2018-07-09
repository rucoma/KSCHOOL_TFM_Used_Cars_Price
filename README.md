# KSchool I Data Science Master

## Final project: Price prediction model of used cars

From a dataset from [Kaggle](https://www.kaggle.com/orgesleka/used-cars-database), consisting in 370k samples of used cars on sale on [eBay Classifieds Germany](https://www.ebay-kleinanzeigen.de/) we will try to build a predictive model that gives us information about the approximate sales price at which users should put their cars on the website.

### Dataset description:  
Dataset contains different descriptive features of the vehicles like brand, model, vehicle type, year of registration, kilometers, etc. These are the features of the original dataset:
* dateCrawled : when this ad was first crawled, all field-values are taken from this date
* name : "name" of the ad
* seller : private or dealer
* offerType: Angebot (offer) or Gesuch (petition)
* price : the price on the ad in Euros
* abtest:
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
* dateCreated : the date for which the ad at ebay was created
* nrOfPictures : number of pictures in the ad (this field contains only 0, won't use)
* postalCode
* lastSeenOnline : when the crawler saw this ad last online

### Project setup  
After cloning repository it's necessary to install the Anaconda environment found in `./data/rucoma.yml` 

### Project steps:
* Data exploration and cleaning
* Data visualization
* Modeling

A partir de un dataset alojado en [Kaggle](https://www.kaggle.com/orgesleka/used-cars-database) consistente en una tabla de aproximadamente 370k registros de coches usados a la venta en [eBay Classifieds Germany](https://www.ebay-kleinanzeigen.de/) intentaremos crear un modelo predictivo que nos dé información acerca del precio de venta aproximado al que los usuarios deberían poner sus coches en el portal.  

El dataset contiene diferentes variables descriptivas de los vehículos como la marca, el modelo, el tipo de vehículo, la antigüedad, los kilómetros, potencia, la ubicación, etc. que nos permitirán crear el modelo predictivo.  

Las etapas del proyecto, idealmente serían las siguientes:  

* *Obtención del dataset*: En este caso, no habrá un proceso de extracción del dato, ya que partiremos de un dataset ya dado.  
* *Limpieza del dataset*: Selección de las variables, a priori, relevantes para el estudio. Limpieza o imputación de valores perdidos.  
* *Exploración del dataset*: Descripción de las distribuciones de las variables y de las relaciones entre ellas.  
* *Transformación de las variables predictoras*: Si fuese necesario, aplicaríamos *feature engineering* para encontrar un mejor ajuste a los datos.  
* *Proceso de modelización*: Aplicaciónn de diferentes algoritmos de regresión para encontrar la metodología que consigue mejores resultados predictivos.  
* *Creación de un simulador interactivo*: A partir de los resultados, creación de un entorno en el cual el usuario pueda introducir los parámetros de su vehículo para obtener un precio de tasación.  
