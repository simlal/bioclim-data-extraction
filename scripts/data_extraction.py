from pathlib import Path
import rasterio
from rasterio import sample
from rasterio.crs import CRS
import pyproj
from pyproj import Transformer
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import yaml
import re

# Path references for src and data files
#TODO pathlib implement
 
# Reference to config.YAML containing metadata from https://chelsa-climate.org/bioclim/ 
#TODO change ref using pathlib
with open('./scripts/config.yaml') as f:
    cfg = yaml.safe_load(f)

# YAML shorthand refs
chelsa_data = cfg['chelsa_data']        # Nested dicts of Chelsa metadata
worldclim_data = cfg['worldclim_data']      # Nested dicts of Worldclim metadata
worldclim_elev = cfg['worldclim_data']['elevation']     # Worldclim elevation dict of params

# List of all EPSG reference codes
EPSG_codes = [int(code) for code in pyproj.get_codes('EPSG', 'CRS')]

class CrsDataPoint :
    """
    A class to represent, transform and extract information of a data point under a geographic coordinate system standard (CRS) 

    ...

    Attributes
    ----------
    id : str
        identifier of single data point
    epsg : int
        EPSG Geodetic Parameter Dataset code of the coordinate reference system (CRS)
    x : float
        x-value (equivalent of East-West latitude lines) of the CRS
    y : float
        y-value (equivalent of North-Sound longitude lines) of the CRS
    coord_xy : tuple
        x,y in tuple format

    Methods
    -------
    get_info():
        Prints the CrsDataPoint information

    transform_crs(epsg_out):
        Transforms the coordinates to the desired EPSG coordinate reference system

    df_to_dict(df):
        Takes the input df and returns a dictionnary of CrsDataPoint objects.
        Calls transform_crs() method if any epsg codes are not 4326.

    extract_bioclim_elev(dataset):
        Extracts the pixel values from the specified GeoTIFF file. Calls transform_crs() method if needed.
    """

    def __init__(self, id, epsg, x, y,) :
        """
        Constructor for CrsDataPoint object.

        Parameters
        ----------
        id : str
            identifier of single data point
        epsg : int
            EPSG Geodetic Parameter Dataset code of the coordinate reference system (CRS)
        x : float
            x-value (equivalent of East-West longitude lines for EPSG:4326) of the CRS
        y : float
            y-value (equivalent of North-Sound latitude lines for EPSG:4326) of the CRS
        xy_pt : tuple
            x,y values in tuple format

        Examples
        --------
        >>> from data_extraction import CrsDataPoint
        >>> sherby = CrsDataPoint('Sherbrooke', epsg=4326, x=-71.890068, y=45.393869)
        >>> print(sherby)
        id : Sherbrooke
        EPSG : 4326
        Map coordinates :
            x = -71.890068
            y = 45.393869
            (x,y) = (-71.890068, 45.393869)
        
        """
        self.id = id
        self.epsg = epsg
        self.x = x
        self.y = y
        self.xy_pt = (self.x, self.y)

    @property
    def epsg(self) :
        return self._epsg
    @property
    def x(self) : 
        return self._x
    @property
    def y(self) : 
        return self._y

    @epsg.setter
    def epsg(self, value):
        if value not in EPSG_codes :
            raise ValueError("Not a valid EPSG code. Use int associated with EPSG codes")   
        else :
            self._epsg = value
    @x.setter
    def x(self, value) :
        if not isinstance(value, float):
            raise TypeError("x value must be a float")
        else : 
            self._x = value
    @y.setter
    def y(self, value) :
        if not isinstance(value, float):
            raise TypeError("y value must be a float") 
        else : 
            self._y = value 

    
    def get_info(self) :
        """
        Prints the CrsDataPoint object information. 
        """
        return(
            "id : {}\nEPSG : {}\nMap coordinates :\n\tx = {}\n\ty = {}\n\t(x,y) = {}\n"
            .format(self.id, self.epsg, self.x, self.y, self.xy_pt)
            )

    
    def transform_crs(self, epsg_out=4326) :
        """
        Transforms the coordinates to the desired EPSG coordinate reference system. 
        Default argument is EPSG:4326 which is the reference for the WorldClim and Chelsa datasets
        
        Parameters
        ----------
        epsg_out : int
            EPSG Geodetic Parameter Dataset code of the coordinate reference system (CRS) (default is 4326)

        Returns
        -------
        CrsDataPoint object with updated x-y values for the given EPSG code. 
        With default arg it will output the following x/y values :
        x_out : float
            longitude (x-value, North-South lines) that range between -180 and +180 degrees.
        y_out : float
            latitude (y-value, East-West lines) that range between -90 and +90 degrees.

        Examples
        --------
        >>> sherby = CrsDataPoint('Sherbrooke', epsg=3857, x=-8002765.769038227, y=5683742.6823244635)
        >>> sherby_gps = sherby.transform_crs()
        >>> print(sherby_gps)
        id : Sherbrooke_transformed
        EPSG : 4326
        Map coordinates :
            x = -71.89006805555556
            y = 45.39386888888889
            (x,y) = (-71.89006805555556, 45.39386888888889)

        """
        # Check if code valid
        if epsg_out not in EPSG_codes:
            raise ValueError("Input EPSG code not valid, see https://pyproj4.github.io/pyproj/stable/api/database.html#pyproj.database.get_codes")
        
        # Call transform method from pyproj
        transformer = Transformer.from_crs(self.epsg, CRS.from_epsg(epsg_out), always_xy=True)
        x_out, y_out = transformer.transform(self.x, self.y)
        return CrsDataPoint(self.id+"_transformed", epsg_out, x_out, y_out)

    def df_to_dict(df) :
        """
        Takes the input df and returns a dictionnary of CrsDataPoint objects.
        Calls transform_crs() method if any epsg codes are not 4326.

        Parameters
        ----------
        df : dataframe
            Input dataframe with the following structure : 
            {'id' : specimen name(any) , 'epsg' : code(int), 'x' : x-value(float), 'y' : y-value(float)}

        Returns
        -------
        Dictionnary of CrsDataPoint objects

        Examples
        --------
        >>> df = pd.DataFrame({
        ...     'id' : ['Sherbrooke', 'Paris'],
        ...     'epsg' : [3857, 4326],
        ...     'x' : [-8002765.769038227, 2.346963],
        ...     'y' : [5683742.6823244635, 48.858885],
        ...         })
        >>> cities = CrsDataPoint.df_to_dict(df)
        Dataframe contains data with CRS other than EPSG:4326. Calling transform_crs()...
        >>> print(cities['Sherbrooke'])
        id : Sherbrooke_transformed
        EPSG : 4326
        Map coordinates :
            x = -71.89006805555556
            y = 45.39386888888889
            (x,y) = (-71.89006805555556, 45.39386888888889)

        """
        crs_data_points = {}
        if (df['epsg'] != 4326).any() == True :
            print("Dataframe contains data with CRS other than EPSG:4326. Calling transform_crs()...")
            for index, row in df.iterrows() :
                if row['epsg'] == 4326 : 
                    crs_data_points[row['id']] = CrsDataPoint(row['id'], row['epsg'], row['x'], row['y'])
                else : 
                    crs_data_points[row['id']] = CrsDataPoint(row['id'], row['epsg'], row['x'], row['y']).transform_crs()
            return crs_data_points
        else :     
            for index, row in df.iterrows() :
                crs_data_points[row['id']] = CrsDataPoint(row['id'], row['epsg'], row['x'], row['y'])
            return crs_data_points

    def extract_bioclim_elev(self, dataset):
        """
        Extracts the pixel values from the specified GeoTIFF file. Calls transform_crs() method if needed. 
        

        Parameters
        ----------
        dataset : string
            Name of the dataset to extract the data from : "chelsa" or "worldclim"

        Returns
        -------
        A dictionnary containing sample id, lon(x), lat(y), bio# (Unit) : Corrected (scale + offset where needed) pixel value,
        bio#_longname : Name of the measurement, bio#_explanation : Brief explanation of measurement.

        Examples
        --------
        >>> sherby = CrsDataPoint('Sherbrooke', epsg=4326, x=-71.890068, y=45.393869) 
        >>> sherby_chelsa = sherby.extract_bioclim_elev(dataset='chelsa')
        Extracting values for Sherbrooke at lon=-71.890 lat=45.394  for all climate variables bio1 to bio19 in CHELSA V2.1 (1981-2010)  + elevation from WorldClim 2.1 dataset...
        Done!
        >>> import pandas as pd
        >>> pd.DataFrame([sherby_chelsa])
                id  epsg  ...  elevation_Meters                              elevation_explanation
        0  Sherbrooke  4326  ...               158  Elevation in meters derived from Shuttle Radar...

        [1 rows x 63 columns]
        """
        # CHELSA data extraction
        if dataset == "chelsa" :
            # Checking for EPSG:4326
            if self.epsg == 4326 :  
                single_pt_clim_data = {
                    'id' : self.id,
                    'epsg' : self.epsg,
                    'lon' : self.x,
                    'lat' : self.y,
                }
                print(
                    "Extracting values for {} at lon={:.3f} lat={:.3f}".format(self.id, self.x, self.y),
                    " for all climate variables bio1 to bio19 in CHELSA V2.1 (1981-2010)",
                    " + elevation from WorldClim 2.1 dataset..."
                ) 
                for k,v in chelsa_data.items() :
                    with rasterio.open("./data/"+v['filename']) as tiff :
                        pixel_val = rasterio.sample.sample_gen(tiff, [self.xy_pt])    # Extracting raw pixel value
                        for val in pixel_val :
                            single_pt_clim_data[k+' ('+v['unit']+')'] = val[0]*v['scale']+v['offset']
                            single_pt_clim_data[k+"_longname"] = v['longname']
                            single_pt_clim_data[k+"_explanation"] = v['explanation']
                
                # Extract elevation data
                with rasterio.open("./data/"+worldclim_elev['filename']) as tiff :
                    pixel_val = rasterio.sample.sample_gen(tiff, [self.xy_pt])
                    for val in pixel_val :
                        single_pt_clim_data[worldclim_elev['name']+"_"+worldclim_elev['unit']] = val[0]
                        single_pt_clim_data[worldclim_elev['name']+"_explanation"] = worldclim_elev['explanation']
                print("Done!")
                return single_pt_clim_data

            # Calling transform_crs() method to convert coordinates
            else :
                print("Data point with x,y other than EPSG:4326. Calling transform_crs() method...")
                transformed = self.transform_crs()
                single_pt_clim_data = {
                    'id' : transformed.id,
                    'epsg' : transformed.epsg,
                    'lon' : transformed.x,
                    'lat' : transformed.y,
                }
                print(
                    "...than extracting values for {} at lon={:.3f} lat={:.3f}".format(transformed.id, transformed.x, transformed.y),
                    " for all climate variables bio1 to bio19 in CHELSA V2.1 (1981-2010)",
                    " + elevation in WorldClim 2.1 dataset..."
                )
                for k,v in chelsa_data.items() :
                    with rasterio.open("./data/"+v['filename']) as tiff :
                        pixel_val = rasterio.sample.sample_gen(tiff, [transformed.xy_pt])    # Extracting raw pixel value
                        for val in pixel_val :
                            single_pt_clim_data[k+' ('+v['unit']+')'] = val[0]*v['scale']+v['offset']
                            single_pt_clim_data[k+"_longname"] = v['longname']
                            single_pt_clim_data[k+"_explanation"] = v['explanation']
                    
                # Extract elevation data
                with rasterio.open("./data/"+worldclim_elev['filename']) as tiff :
                    pixel_val = rasterio.sample.sample_gen(tiff, [transformed.xy_pt])
                    for val in pixel_val :
                        single_pt_clim_data[worldclim_elev['name']+"_"+worldclim_elev['unit']] = val[0]
                        single_pt_clim_data[worldclim_elev['name']+"_explanation"] = worldclim_elev['explanation']
                print("Done!")
                return single_pt_clim_data  
        
        # WorldClim data extraction
        if dataset == "worldclim" :
            # Checking for EPSG:4326
            if self.epsg == 4326 :  
                single_pt_clim_data = {
                    'id' : self.id,
                    'epsg' : self.epsg,
                    'lon' : self.x,
                    'lat' : self.y,
                }
                print(
                    "Extracting values for {} at lon={:.3f} lat={:.3f}".format(self.id, self.x, self.y),
                    " for all climate variables bio1 to bio19", 
                    " + elevation in WorldClim 2.1 (1970-2000) dataset..."
                ) 
                for k,v in worldclim_data.items() :
                    with rasterio.open("./data/"+v['filename']) as tiff :
                        pixel_val = rasterio.sample.sample_gen(tiff, [self.xy_pt])    # Extracting raw pixel value
                        for val in pixel_val :
                            single_pt_clim_data[k+' ('+v['unit']+')'] = val[0]
                            single_pt_clim_data[k+"_longname"] = v['longname']
                            single_pt_clim_data[k+"_explanation"] = v['explanation']
                    
                    # Extract elevation data
                with rasterio.open("./data/"+worldclim_elev['filename']) as tiff :
                    pixel_val = rasterio.sample.sample_gen(tiff, [self.xy_pt])
                    for val in pixel_val :
                        single_pt_clim_data[worldclim_elev['name']+"_"+worldclim_elev['unit']] = val[0]
                        single_pt_clim_data[worldclim_elev['name']+"_explanation"] = worldclim_elev['explanation']
                print("Done!")
                return single_pt_clim_data

            # Calling transform_crs() method to convert coordinates
            else :
                print("Data point with x,y other than EPSG:4326. Calling transform_crs() method...")
                transformed = self.transform_crs()
                single_pt_clim_data = {
                    'id' : transformed.id,
                    'epsg' : transformed.epsg,
                    'lon' : transformed.x,
                    'lat' : transformed.y,
                }
                print(
                    "...than extracting values for {} at lon={:.3f} lat={:.3f}".format(transformed.id, transformed.x, transformed.y), 
                    "for all climate variables bio1 to bio19 + elevation in WorldClim V2.1 (1970-2000)..."
                )
                for k,v in worldclim_data.items() :
                    with rasterio.open("./data/"+v['filename']) as tiff :
                        pixel_val = rasterio.sample.sample_gen(tiff, [transformed.xy_pt])    # Extracting raw pixel value
                        for val in pixel_val :
                            single_pt_clim_data[k+' ('+v['unit']+')'] = val[0]
                            single_pt_clim_data[k+"_longname"] = v['longname']
                            single_pt_clim_data[k+"_explanation"] = v['explanation']
                    
                    # Extract elevation data
                with rasterio.open("./data/"+worldclim_elev['filename']) as tiff :
                    pixel_val = rasterio.sample.sample_gen(tiff, [transformed.xy_pt])
                    for val in pixel_val :
                        single_pt_clim_data[worldclim_elev['name']+"_"+worldclim_elev['unit']] = val[0]
                        single_pt_clim_data[worldclim_elev['name']+"_explanation"] = worldclim_elev['explanation']   
                return single_pt_clim_data    
        
        else :
            raise ValueError("Enter the dataset you want to extract the climate data from : \"chelsa\" or \"worldclim\"") 

# Trim data dict with base CrsDataPoint attributes (may be crs_transformed) + bioclim_elev values
def trim_data(full_bioclim_data):
    """
    Function that trims the extracted climate data dictionnary and returns a simplified version with essential data only

    Parameters
    ----------
    full_bioclim_data : dictionnary
        Dictionnary containing the full climate data obtained with the extract_bioclim_elev() method

    Returns
    -------
    Trimmed down version of the extracted climate data dictionnary

    Examples
    --------
    >>>
    
    """
    # Return all keys from dict
    all_keys = [k for k in full_bioclim_data.keys()]
    # Filter for columns with corrected climate data (bio# (Unit) key) + append to id,epsg,lon,lat cols
    filtered_keys = all_keys[:4] + [key for key in all_keys[4:] if re.search("bio[0-9]* ", key)]

    # Extract filtered keys from full climate data dict
    light_clim_data_dict = dict((k, full_bioclim_data[k]) for k in filtered_keys if k in full_bioclim_data)
    return light_clim_data_dict
