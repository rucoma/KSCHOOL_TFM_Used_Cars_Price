# Modelo de predicción de precio de coches usados

### KSchool I Data Science Master Project

A partir de un dataset alojado en [Kaggle](https://www.kaggle.com/orgesleka/used-cars-database) consistente en una tabla de aproximadamente 370k registros de coches usados a la venta en [eBay Clasificados Alemania](https://www.ebay-kleinanzeigen.de/) intentaremos crear un modelo predictivo que nos dé información acerca del precio de venta aproximado al que los usuarios deberían poner sus coches en el portal.  

El dataset contiene diferentes variables descriptivas de los vehículos como la marca, el modelo, el tipo de vehículo, la antigüedad, los kilómetros, potencia, la ubicación, etc. que nos permitirán crear el modelo predictivo.  

Las etapas del proyecto, idealmente serían las siguientes:  

* *Obtención del dataset*: En este caso, no habrá un proceso de extracción del dato, ya que partiremos de un dataset ya dado.  
* *Limpieza del dataset*: Selección de las variables, a priori, relevantes para el estudio. Limpieza o imputación de valores perdidos.  
* *Exploración del dataset*: Descripción de las distribuciones de las variables y de las relaciones entre ellas.  
* *Transformación de las variables predictoras*: Si fuese necesario, aplicaríamos *feature engineering* para encontrar un mejor ajuste a los datos.  
* *Proceso de modelización*: Aplicaciónn de diferentes algoritmos de regresión para encontrar la metodología que consigue mejores resultados predictivos.  
* *Creación de un simulador interactivo*: A partir de los resultados, creación de un entorno en el cual el usuario pueda introducir los parámetros de su vehículo para obtener un precio de tasación.  
