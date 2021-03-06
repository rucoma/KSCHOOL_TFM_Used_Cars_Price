# KSchool: I Data Science Master

## Final project: Predictive model of the price of used cars

From a dataset from [Kaggle](https://www.kaggle.com/orgesleka/used-cars-database), consisting in 370k samples of used cars on sale on [eBay Classifieds Germany](https://www.ebay-kleinanzeigen.de/) we will try to build a predictive model that gives us information about the approximate sales price at which users should put their cars on the website.

### Dataset description:  
Dataset contains different descriptive features of the vehicles like brand, model, vehicle type, year of registration, kilometers, etc. These are the features of the original dataset:
* dateCrawled: when this ad was first crawled, all field-values are taken from this date. Won't be used in the project.
* name: "name" of the ad. Won't be used in the project.
* seller: private or dealer
* offerType: Angebot (offer) or Gesuch (petition)
* price: the price on the ad in Euros
* abtest: eBay internal data. Won't be used in the project.
* vehicleType: coupe, SUV, cabrio, limousine, etc
* yearOfRegistration: at which year the car was first registered
* gearbox: Type of transmission
* powerPS: power of the car in PS (Horse Power)
* model
* kilometer: how many kilometers the car has driven
* monthOfRegistration: at which month the car was first registered
* fuelType: benzin, diesel, elektro, etc
* brand
* notRepairedDamage: if the car has a damage which is not repaired yet
* dateCreated: the date for which the ad at ebay was created. Won't be used in the project.
* nrOfPictures: number of pictures in the ad (this field contains only 0, won't use)
* postalCode
* lastSeenOnline: when the crawler saw this ad last online. Won't be used in the project.

## Project manual  

### Required hardware  
Project has been developed on an Intel Core i7 PC with 4 cores and 16Gb RAM. It should not be a problem not to have that hardware settings, but some scripts use a lot of resources.  

### Required software  
OS used in the project has been Linux, so it's the recommended system to run it. R and Python has been used to create the scripts, so it will be necessary to install both to run the scripts:  
* [Anaconda](https://www.anaconda.com/download/#linux)  
* [R](https://cran.r-project.org/)  
* [R Studio](https://www.rstudio.com/products/rstudio/download/)  

### Project setup  
After cloning the repository it's necessary to install the Anaconda environment found in `./data/TFM.yml`. Just type in a terminal: `conda env create -f TFM.yml` and then `source activate TFM`.  
Project is based on Jupyter notebooks. Both R and Python kernels are used, so it's important to activate the provided environment because R kernel is not included by default in Anaconda installation.  
If for some reason, TFM environment fails to activate (due to incompatibilities with your system), it will be necessary to install the following libraries using `conda install`:
* numpy
* pandas
* matplotlib
* scipy
* scikit-learn
* flask
* collections
* wtforms
* R kernel for Jupyter notebooks: `conda install -c r r-irkernel`

### Project steps:
* **Introduction**: Jupyter notebook, found in `./src/00 - Introduction.ipynb`. This notebook includes some explanation about the project and the approach.
* **Data exploration and cleaning**: Jupyter notebook with R kernel, found in `./src/01 - Data exploration and cleaning.ipynb`. This notebook covers all the data acquisition and cleaning phase to prepare dataset for modeling.  
* **Data visualization**: Jupyter notebook with R kernel, found in `./src/02 - Data visualization.ipynb`. This notebook inspects the dataset to understand the structure of data and get some useful insights.
* **Modeling**: Jupyter notebook with Python kernel, found in `./src/03 - Modeling.ipynb`. This notebook applies different machine learning algorithms to the dataset in order to predict the price of cars in the most precise way. **WARNING**: some algorithms can take a long time to run, so cells containing them have been commented to avoid execution (uncomment under your responsability!! :-) ). Results has been saved using joblib and are being loaded when it corresponds.
* **Prediction of price using new data**: Little Flask web application tha allows to quote your used car. It can be run from a terminal typing: `python ./src/FlaskApp/app.py`. Then, in a web browser enter the url: `http://localhost:5000/`. Select the features of your car and press **'Send data'** button to get the estimated sale price of your car.
* **Results & conclusions**: Jupyter notebook, found in `./src/04 - Results and conclusions.ipynb`. This notebook includes the main findings on the project.
