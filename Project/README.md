# Title: How flights delay?
Team members: FU Yan, FENG Wentao, SUN Zhaodong, HUANG Yunbei

## Abstract
In this project we explored through our dataset and set up a model predicting delay for given conditions, and based on this model we can give advice on choosing flights on different seasons, airlines and hours. Due to the constraint on difficulties getting whole world delay dataset, and the US is the largest flight country, in our project the delay analysis is mostly based on the US data.

We want to know :

* What will affect mostly on the delay of a flight, could it be departure season, hours or airlines?
* And can we predict if and how long will a flight delays given certain situations?
* Or, if some one wants to fly from city A to city B, can we give him or her some advices on choose flights based on the delay rate?


## Dataset
In our project we used two data set, `OpenFlight` and `FlightDelay` data set.

`OpenFlight` dataset is obtained from: https://openflights.org/data.html

This OpenFlights/Airline Route Mapper Route Database contains 67,663 routes (EDGES) between 3,321 airports (NODES) on 548 airlines spanning the globe. 

`FlightDelay` is obtained from Kaggle:

https://www.kaggle.com/usdot/flight-delays#flights.csv

This dataset is collected by the U.S. Department of Transportation's (DOT) Bureau of Transportation Statistics, who tracks the on-time performance of domestic flights operated by large air carriers from 01/01/2015 to 31/21/2015. And features information flight number, airline, departure and arrival time, delay time, air time, distance, origin and destination airport and delay reason( not for all delayed flights). Also, the documents including relationship of IATA code and full information of airports and airlines are given. 

License(https://opendatacommons.org/licenses/odbl/1.0/) and Database Contents License(https://opendatacommons.org/licenses/dbcl/1.0/).


## Result


## Structure of repo