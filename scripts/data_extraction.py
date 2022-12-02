import rasterio
from rasterio import sample
from rasterio.crs import CRS
import pyproj
from pyproj import Transformer
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

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
    __str__():
        Prints the CrsDataPoint information

    transform_gps(epsg_out):
        Transforms the coordinates to the desired EPSG coordinate reference system

    df_to_dict(df):
        XXXXX
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

    @epsg.setter
    def epsg(self, value):
        if value not in EPSG_codes :
            raise ValueError("Not a valid EPSG code. Use int associated with EPSG codes")   
        else :
            self._epsg = value

    
    def __str__(self) :
        """
        Prints the CrsDataPoint object information. 
        """
        return(
            'id : {}\nEPSG : {}\nMap coordinates :\n\tx = {}\n\ty = {}\n\t(x,y) = {}\n'
            .format(self.id, self.epsg, self.x, self.y, self.xy_pt)
            )

    
    def transform_GPS(self, epsg_out=4326) :
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

        >>> sherby = CrsDataPoint('Sherbrooke', epsg=3857, x=-8002765.769038227, y=5683742.6823244635)
        >>> sherby_gps = sherby.transform_GPS()
        >>> print(sherby_gps)
        id : Sherbrooke_transformed
        EPSG : 4326
        Map coordinates :
            x = -71.89006805555556
            y = 45.39386888888889
            (x,y) = (-71.89006805555556, 45.39386888888889)

        """
        transformer = Transformer.from_crs(self.epsg, CRS.from_epsg(epsg_out), always_xy=True)
        x_out, y_out = transformer.transform(self.x, self.y)
        return CrsDataPoint(self.id+"_transformed", epsg_out, x_out, y_out)

    def df_to_dict(df) :
        """
        Takes the input df and returns a dictionnary of CrsDataPoint objects.
        Calls transform_GPS() method if any epsg codes are not 4326.

        Parameters
        ----------
        df : dataframe

        Returns
        -------
        Dictionnary of CrsDataPoint objects

        >>> df = pd.DataFrame({
        ...     'id' : ['Sherbrooke', 'Paris'],
        ...     'epsg' : [3857, 4326],
        ...     'x' : [-8002765.769038227, 2.346963],
        ...     'y' : [5683742.6823244635, 48.858885],
        ...         })
        >>> cities = CrsDataPoint.df_to_dict(df)
        Dataframe contains data with CRS other than EPSG:4326. Calling transform_GPS()...
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
            print("Dataframe contains data with CRS other than EPSG:4326. Calling transform_GPS()...")
            for index, row in df.iterrows() :
                if row['epsg'] == 4326 : 
                    crs_data_points[row['id']] = CrsDataPoint(row['id'], row['epsg'], row['x'], row['y'])
                else : 
                    crs_data_points[row['id']] = CrsDataPoint(row['id'], row['epsg'], row['x'], row['y']).transform_GPS()
            return crs_data_points
        else :     
            for index, row in df.iterrows() :
                crs_data_points[row['id']] = CrsDataPoint(row['id'], row['epsg'], row['x'], row['y'])
            return crs_data_points

    def single_point_extraction():
        """
        
        """
