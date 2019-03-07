# Title: A network tour to flight delay in the US
Team members: FU Yan, FENG Wentao, SUN Zhaodong, WANG Yunbei

## Structure of repo
`README.md`: A simple introduction to the project.

`FINAL.ipynb`: The notebook including all codes and analysis of our data set.

`TransLearn.py`: The py containing functions used in transductive learning.

`data` folder: The folder containing part of used data (not all for some data is too large to be uploaded in Github; not uploaded data can be found in links in `Dataset` description.

## Abstract
In this project, we explored through our dataset and set up a model predicting delay for given conditions, and based on this model we can advise on choosing flights on different seasons, airlines and hours. Due to the constraint on difficulties getting whole world delay dataset, and the US is the largest flight country, in our project the delay analysis is mostly based on the US data.

We want to know :

* What will affect mostly on the delay of a flight, could it be departure season, hours or airlines?
* And can we predict if and how long will a flight delay given certain situations?
* Or, if someone wants to fly from city A to city B, can we give him or her some advice on choose flights based on the delay rate?


## Dataset
In our project we used two data set, `OpenFlight` and `FlightDelay` data set.

`OpenFlight` dataset is obtained from https://openflights.org/data.html

This OpenFlights/Airline Route Mapper Route Database contains 67,663 routes (EDGES) between 3,321 airports (NODES) on 548 airlines spanning the globe. 

`FlightDelay` is obtained from Kaggle:

https://www.kaggle.com/usdot/flight-delays#flights.csv

This dataset is collected by the U.S. Department of Transportation's (DOT) Bureau of Transportation Statistics, who tracks more than 5,714,000 samples of domestic flights operated by large air carriers from 01/01/2015 to 31/21/2015, with 322 airports. Also, features information flight number, airline, departure and arrival time, delay time, air time, distance, origin and destination airport and delay reason( not for all delayed flights). Also, the documents including the relationship of IATA code and full information of airports and airlines are given. 

## Result
We created our graph using airports as nodes, the distance between airports after Gaussian kernel as weights.

We analyzed delay in two ways: first, we binarized the delay time into 1 (the departure airport tends to delay) or -1 (the departure airport tends to arrive earlier), then we used k means, spectral graph and transductive learning to perform clustering. The **accuracy** are 64.3%(5 clusters), 69.4%(threshold eigenvalue is0.004) and 72.3%(recovering from 30% data) respectively.

Then we wanted to use more features than the distance to predict the delay time. We used LightGBM, a tree-based algorithm. After model building and hyperparameter tuning, we got a model with **prediction RMSE = 2.3**, which worked quite well. Moreover, we also developed a recommendation system. Given departure date and airports, our recommendation system returns the best combination of airline and departure time, and also the predicted delay minutes. 
