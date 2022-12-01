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
    coord : tuple
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
            x-value (equivalent of East-West latitude lines) of the CRS
        y : float
            y-value (equivalent of North-Sound longitude lines) of the CRS
        coord : tuple
            x,y values in tuple format

        >>> from data_extraction import CrsDataPoint
        >>> coord = CrsDataPoint('montreal', 4326, 45.508888, -73.561668)
        >>> print(coord)
        id : montreal
        EPSG : 4326
        Map coordinates :
            x = 45.508888
            y = -73.561668
        ###########################
        """
        self.id = id
        self.epsg = epsg
        self.x = x
        self.y = y
        self.coord = (self.x, self.y)

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

        >>> 
        """
        return(
            'id : {}\nEPSG : {}\nMap coordinates :\n\tx = {}\n\ty = {}\n###########################'
            .format(self.id, self.epsg, self.x, self.y)
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
            longitude (x-value, North-South lines) that range between -90 and +90 degrees.
        y_out : float
            latitude (y-value, East-West lines) that range between -90 and +90 degrees.


        >>> from data_extraction import CrsDataPoint
        >>> coord = CrsDataPoint('c1', 3005, 4760950.613410814, 1516444.4032389917)
        >>> print(coord)
        id : c1
        EPSG : 3005
        Map coordinates :
            x = 4760950.613410814
            y = 1516444.4032389917
        ###########################
        >>> coord_transformed = coord.transform_GPS()
        >>> print(coord_transformed)
        id : c1_transformed
        EPSG : 4326
        Map coordinates :
            x = 45.508888000000034
            y = -73.56166799999998
        ###########################

        """
        transformer = Transformer.from_crs(self.epsg, CRS.from_epsg(epsg_out))
        x_out, y_out = transformer.transform(self.x, self.y)
        # return (x_out, y_out)
        return CrsDataPoint(self.id+"_transformed", epsg_out, x_out, y_out)

    def df_to_dict(dataframe) :
        """
        Takes the input df and returns a dictionnary of CrsDataPoint objects

        Parameters
        ----------
        df : dataframe

        Returns
        -------
        Dictionnary of CrsDataPoint objects

        >>> df = pd.DataFrame({
        ... 'id' : ['montreal', 'paris'],
        ... 'epsg' : [4326,3005],
        ... 'x' : [45.508888, 48.864716],
        ... 'y' : [-73.561668, 2.349014],
        ... })
        >>> crs_data_points = CrsDataPoint.df_to_dict(df)
        >>> print(crs_data_points)
        {'montreal': <data_extraction.CrsDataPoint object at 0x7f561ab6a310>, 'paris': <data_extraction.CrsDataPoint object at 0x7f561ab68a90>}
        >>> print(crs_data_points['specimen1'])
        id : specimen1
        EPSG : 4326
        Map coordinates :
            x = 44.2
            y = 32
        ###########################

        """
        crs_data_points = {}
        for index, row in dataframe.iterrows() :
            crs_data_points[row['id']] = CrsDataPoint(row['id'], row['epsg'], row['x'], row['y'])
        return crs_data_points

coord = CrsDataPoint()

with rasterio.open('./data/CHELSA_bio2_1981-2010_V.2.1.tif') as dat:
    vals = list(rasterio.sample.sample_gen(dat, coords))
    for (lon,lat), val in zip(coords, vals):
        print(lon,lat,val[0])