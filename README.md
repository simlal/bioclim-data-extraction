# Bioclimatic variables data extraction at high resolution

## Databases
### WorldClim Bioclimatic variables (latest version 2.1)

Latest publication : 
[WorldClim 2: new 1-km spatial resolution climate surfaces for global land areas (2017)](https://doi.org/10.1002/joc.5086)

Historical data range : 
1970-2000

Data at 1 km<sup>2</sup> resolution for all 19 BIOCLIM vars : (https://geodata.ucdavis.edu/climate/worldclim/2_1/base/wc2.1_30s_bio.zip) 

### Chelsa - Climatologies at high resolution for the earth’s land surface areas (latest version V2.1)

Latest publication : 
[Global climate-related predictors at kilometre resolution for the past and future. (preprint)](https://doi.org/10.5194/essd-2022-212)

Historical data range : 
1981-2010

Data at 1 km<sup>2</sup> resolution for all 19 BIOCLIM vars/ 

## Installation
### Requirements
TODO: create requirements.txt

### Linux-based systems
1. **Create a new conda environement**

`conda create --name bioclim --file requirements.txt`

2. Activate the environement

`conda activate bioclim`

3. Clone the repo

    1. `git clone git@github.com:simlal/bioclim-data-extraction.git`
    2. `cd bioclim-data-extraction`

## Download data

***Steps :***

1. Run **bioclim_download.py** from the command line

`python bioclim_download.py`

2. To be continued...

## Extract data

Scripts + Examples