# Bioclimatic variables data extraction at high resolution

## About the project
This is a small python program that allows easy and fast extraction of [Bioclimatic variables](https://www.worldclim.org/data/bioclim.html) (commonly used in ecological analyses and modeling) from 2 of the most prohiminent climate datasets, [Chelsa](https://chelsa-climate.org) and [WorldClim](https://www.worldclim.org/). To extract the data, you only need the lon/lat (x,y) coordinates using any of the Coordinate Reference System in combination with the download GeoTIFF files. The program will take care of offset + scale correction and will output the data in the proper units for each variable.
## Databases
### WorldClim Bioclimatic variables (latest version 2.1)

Latest publication : 
[WorldClim 2: new 1-km spatial resolution climate surfaces for global land areas (2017)](https://doi.org/10.1002/joc.5086)

Historical data range : 
1970-2000

Data at 1 km<sup>2</sup> resolution for all 19 BIOCLIM vars <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 576 512" width="16px"><!-- Font Awesome Pro 5.15.4 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) --><path d="M510.5 225.5c-6.9-37.2-39.3-65.5-78.5-65.5-12.3 0-23.9 3-34.3 8-17.4-24.1-45.6-40-77.7-40-53 0-96 43-96 96 0 .5.2 1.1.2 1.6C187.6 233 160 265.2 160 304c0 44.2 35.8 80 80 80h256c44.2 0 80-35.8 80-80 0-39.2-28.2-71.7-65.5-78.5zm-386.4 34.4c-37.4-37.4-37.4-98.3 0-135.8 34.6-34.6 89.1-36.8 126.7-7.4 20-12.9 43.6-20.7 69.2-20.7.7 0 1.3.2 2 .2l8.9-26.7c3.4-10.2-6.3-19.8-16.5-16.4l-75.3 25.1-35.5-71c-4.8-9.6-18.5-9.6-23.3 0l-35.5 71-75.3-25.1c-10.2-3.4-19.8 6.3-16.4 16.5l25.1 75.3-71 35.5c-9.6 4.8-9.6 18.5 0 23.3l71 35.5-25.1 75.3c-3.4 10.2 6.3 19.8 16.5 16.5l59.2-19.7c-.2-2.4-.7-4.7-.7-7.2 0-12.5 2.3-24.5 6.2-35.9-3.6-2.7-7.1-5.2-10.2-8.3zm69.8-58c4.3-24.5 15.8-46.4 31.9-64-9.8-6.2-21.4-9.9-33.8-9.9-35.3 0-64 28.7-64 64 0 18.7 8.2 35.4 21.1 47.1 11.3-15.9 26.6-28.9 44.8-37.2zm330.6 216.2c-7.6-4.3-17.4-1.8-21.8 6l-36.6 64c-4.4 7.7-1.7 17.4 6 21.8 2.5 1.4 5.2 2.1 7.9 2.1 5.5 0 10.9-2.9 13.9-8.1l36.6-64c4.3-7.7 1.7-17.4-6-21.8zm-96 0c-7.6-4.3-17.4-1.8-21.8 6l-36.6 64c-4.4 7.7-1.7 17.4 6 21.8 2.5 1.4 5.2 2.1 7.9 2.1 5.5 0 10.9-2.9 13.9-8.1l36.6-64c4.3-7.7 1.7-17.4-6-21.8zm-96 0c-7.6-4.3-17.4-1.8-21.8 6l-36.6 64c-4.4 7.7-1.7 17.4 6 21.8 2.5 1.4 5.2 2.1 7.9 2.1 5.5 0 10.9-2.9 13.9-8.1l36.6-64c4.3-7.7 1.7-17.4-6-21.8zm-96 0c-7.6-4.3-17.4-1.8-21.8 6l-36.6 64c-4.4 7.7-1.7 17.4 6 21.8 2.5 1.4 5.2 2.1 7.9 2.1 5.5 0 10.9-2.9 13.9-8.1l36.6-64c4.3-7.7 1.7-17.4-6-21.8z"/></svg> https://www.worldclim.org/

Metadata : bioclim-data-extraction/data/specs/anuclim61.pdf

### Chelsa - Climatologies at high resolution for the earth’s land surface areas (latest version V2.1)

Latest publication : 
[Global climate-related predictors at kilometre resolution for the past and future. (preprint)](https://doi.org/10.5194/essd-2022-212)

Historical data range : 
1981-2010

Data at 1 km<sup>2</sup> resolution for all 19 BIOCLIM vars/ <img src="https://chelsa-climate.org/wp-content/uploads/2016/02/logotest3.gif" width="32px"> https://chelsa-climate.org

Metadata : bioclim-data-extraction/data/specs/CHELSA_tech_specification_V2.pdf

## Installation
Use [conda](https://conda.io) to setup the python environment 
### Requirements
For full requirements see **requirements.txt**. Uses mainly **python > 3** with the following main libraries:
- rasterio
- pyproj
- pandas

### Linux-based systems
**Clone the repo**
``` bash
git clone git@github.com:simlal/bioclim-data-extraction.git
cd bioclim-data-extraction
```
**Create a new conda environement**

``` bash
conda create --name bioclim --file requirements.txt
conda activate bioclim
```
There are some unused dependencies in there, but there are some intricacies regarding compatible versions of *rasterio* and *pyproj* so just go ahead and use the requirements.txt

**Dir structure**
``` bash
.
├── data
│   ├── bioclim
│   ├── specs
│   │   ├── anuclim61.pdf
│   │   └── CHELSA_tech_specification_V2.pdf
│   ├── states.csv
│   └── urls
│       ├── chelsa_bioclim19_S3paths.txt
│       └── worldclim_bioclim19_30s_path.txt
├── scripts
│   ├── config.yaml
│   ├── data_extraction.py
│   ├── download.py
│   ├── __init__.py
├──requirements.txt
└── run.py
```
We will perform our data analysis from the main directory (i.e. run.py in this example).

## Download data

### With wget
```bash
mkdir data/bioclim/
wget -i data/urls/chelsa_bioclim19_S3paths.txt -P data/bioclim/
wget -i data/urls/worldclim_bioclim19_30s_path.txt -P data/bioclim/
```

### Directly with Python
**Steps**

1. Run **bioclim_download.py** from the command line.

```bash
python scripts/download.py
```
```
chelsa : for Chelsa bioclim19 dataset 
worldclim : for WorldClim bioclim19 dataset 
both : for Chelsa and WorldClim bioclim datasets 

Enter which dataset(s) you would like to download.
```

2. Entering dataset (or 'both') keyword will start the download.

There will be some infographics about the progress and speed of the download within the terminal. Note that the download will proceed by chunks.

## Extract data for bioclim 1 to 19 + elevation variables

### For a single data point
Use directly with CrsDataPoint class from run.py 
#### Create a CrsDataPoint instance
```python
>>> from scripts.data_extraction import CrsDataPoint

>>> sherby_3857 = CrsDataPoint('Sherbrooke', epsg=3857, x=-8002765.769038227, y=5683742.6823244635)
>>> sherby_3857.get_info()
id : Sherbrooke
EPSG : 3857
Map coordinates :
        x = -8002765.769038227
        y = 5683742.6823244635
        (x,y) = (-8002765.769038227, 5683742.6823244635)
```

#### Transform to other EPSG if needed
```python
>>> sherby_4236 = sherby_3857.transform_crs()    # default is 4326 (aka GPS)
>>> sherby_gps.get_info()
id : Sherbrooke_transformed
EPSG : 4326
Map coordinates :
   x = -71.89006805555556
   y = 45.39386888888889
   (x,y) = (-71.89006805555556, 45.39386888888889)
```
Since both Worldclim and Chelsa db (GeoTIFF) are encoded with the EPSG:4326 coordinate reference system (crs), we need to convert the x/y coords to EPSG:4326.

The method `transform_crs()` will be automatically called when encountering a non-"4326" object and convert the coordinates accordingly.

#### Extract bioclim 1 to 19 + elevation from Wordclim or Chelsa datasets
Get values and relevant metadata
```python
>>> from scripts.data_extraction import CrsDataPoint

>>> sherby_3857 = CrsDataPoint('Sherbrooke', epsg=3857, x=-8002765.769038227, y=5683742.6823244635)
>>> sherby_4236_chelsa = sherby_3857.extract_bioclim_elev(dataset='chelsa')     # As dictionary
Data point with x,y other than EPSG:4326. Calling transform_crs() method...
...than extracting values for Sherbrooke_transformed at lon=-71.890 lat=45.394  for all climate variables bio1 to bio19 in CHELSA V2.1 (1981-2010)  + elevation in WorldClim 2.1 dataset...
Done!

# Convert to DataFrame
>>> import pandas as pd
>>> sherby_bio_chelsa = pd.DataFrame([sherby_4236_chelsa])
>>> with pd.option_context('display.max_colwidth', 15):
    print(sherby_bio_chelsa)       # Output will vary base on terminal width
               id  epsg        lon        lat  bio1 (Celcius)  ... bio19 (kg / m**2 / month)  bio19_longname  bio19_explanation elevation_Meters elevation_explanation
0  Sherbrooke_...  4326 -71.890068  45.393869            6.05  ...           243.0            mean monthl...  The coldest...                158   Elevation i...      

[1 rows x 63 columns]
```
**To get a leaner dataframe with only relevant class information + values**
```python
>>> from scripts.data_extraction import trim_data

>>> sherby_bio_chelsa_trimmed = trim_data(sherby_4236_chelsa) # From full dict to trimmed dict
>>> print(pd.DataFrame([sherby_bioclim_trimmed]))       # Display as df
                       id  epsg        lon  ...  bio18 (kg / m**2 / month)  bio19 (kg / m**2 / month)  elevation_Meters
0  Sherbrooke_transformed  4326 -71.890068  ...                      375.8                      243.0               158

[1 rows x 24 columns]

```
---
### For multiple data points from a csv file
#### Instantiate from csv
Use the `load_csv()` classmethod with a csv containing the CrsDataPoint attributes as header
```python
>>> from scripts.data_extraction import CrsDataPoint
>>> from pathlib import Path

# State centroid example
>>> csv_file = Path("./data/states.csv")
>>> data = CrsDataPoint.load_csv(csv_file)      # As list of CrsDataPoint objects

# First 3 states
>>> print(data[0:3])
```
We can check at anypoint the complete list of all instantiated objects with by using the `CrsDataPoint.all` attribute.

**To extract the bioclim1 to 19 + elevation values for a given database**
Calling the `extract_multiple_bioclim_elev(specimens_list, dataset, trimmed=True` function returns a dataframe (trimmed or exhaustive depending on *trimmed* arg).
```python
>>> from scripts.data_extraction import extract_multiple_bioclim_elev

# Extract bioclim values for all states
>>> df_trimmed = extract_multiple_bioclim_elev(data, 'worldclim', trimmed=True) # if False : full df
Extracting values for Alaska at lon=-154.493 lat=63.589  for all climate variables bio1 to bio19  + elevation in WorldClim 2.1 (1970-2000) dataset...
Done!
Extracting values for Alabama at lon=-86.902 lat=32.318  for all climate variables bio1 to bio19  + elevation in WorldClim 2.1 (1970-2000) dataset...
Done!
...
Extracting values for Wyoming at lon=-107.290 lat=43.076  for all climate variables bio1 to bio19  + elevation in WorldClim 2.1 (1970-2000) dataset...
Done!

# Checking the first five states
>>> print(df_trimmed.head())
           id  epsg         lon  ...  bio18 (kg / m**2 / month)  bio19 (kg / m**2 / month)  elevation_Meters
0      Alaska  4326 -154.493062  ...                      208.0                       54.0               366
1     Alabama  4326  -86.902298  ...                      319.0                      392.0                57
2    Arkansas  4326  -91.831833  ...                      276.0                      306.0               136
3     Arizona  4326 -111.093731  ...                      203.0                      166.0              1587
4  California  4326 -119.417932  ...                        5.0                      195.0               149

[5 rows x 24 columns]
```

**Then save to csv**
```python
>>> bioclim_out = data_dir / "states_bioclim.csv"
>>> if not Path.is_file(bioclim_out):
>>>     df_trimmed.to_csv(bioclim_out)
```



## Contact
Feel free to contact me for any questions of feedback!