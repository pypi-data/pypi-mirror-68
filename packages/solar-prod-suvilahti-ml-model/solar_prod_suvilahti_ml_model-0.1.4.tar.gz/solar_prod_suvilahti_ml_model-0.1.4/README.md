# Solar Production Suvilahti Regression Model

This is a package containing a regression model and a ML pipeline for an end-to-end machine learning project that provides hourly prediction of produced energy at Suvilahti PV plant for the upcoming 36 hours. The model utilizes the Finnish Meteorological Institute (FMI) open data and weather API as input parameters. Github project [source](https://github.com/screwdriver66/solar_prod_suvilahti).

## Documentation

Documentation can be found in [[source](https://github.com/screwdriver66/solar_prod_suvilahti/tree/master/documentation)]


## Licenses

- The source code is under the GNU GPL v3 license [![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

- Weather observation part of the data set, downloaded from https://en.ilmatieteenlaitos.fi/open-data, prior to its modification is under [Creative Commons Attribution 4.0 International
License][cc-by]. [![CC BY 4.0][cc-by-shield]][cc-by]

- Solar energy production part of the data set was downloaded from https://www.helen.fi/en/solar-panels/solar-power-plants/suvilahti-solar-power-plant prior to its modification had no license document on the web page.

The aforementioned datasets were used in model training and testing. The modified versions are located in regression model's package [datasets](/packages/regression_model/regression_model/datasets/) folder.



[cc-by]: http://creativecommons.org/licenses/by/4.0/
[cc-by-shield]: https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg
