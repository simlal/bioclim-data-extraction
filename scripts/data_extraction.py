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

        >>> 
        """
        return(
            'id : {}\nEPSG : {}\nMap coordinates :\n\tx = {}\n\ty = {}\n\t(x,y) = \n###########################'
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



        """
        transformer = Transformer.from_crs(self.epsg, CRS.from_epsg(epsg_out))
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

mont = CrsDataPoint('montreal', 4326, 45.508888, -73.561668)
with rasterio.open('./data/CHELSA_bio2_1981-2010_V.2.1.tif') as dat:
    val = rasterio.sample.sample_gen(dat, [mont.xy_pt])
    # val = generator of data extracted at given xy_coord
    
    test_dict = {}
    for (x,y),v in zip([mont.xy_pt], val):
        # print(x,y, v[0])
        test_dict = {'id' : mont.id, 'epsg' : mont.epsg, 'x' : x, 'y' : y, 'val' : v[0]}
    # print(test_dict) 
    

df = pd.DataFrame({
    'id' : ['montreal', 'paris'],
    'epsg' : [4326,3857],
    'x' : [45.508888, 48.864716],
    'y' : [-73.561668, 2.349014],
        })
print(df)
crs_data_points = CrsDataPoint.df_to_dict(df)
print(crs_data_points['paris'])

with rasterio.open('./data/CHELSA_bio2_1981-2010_V.2.1.tif') as dat:
    xy_pts = [v.xy_pt for k,v in crs_data_points.items()]
    clim_dat = rasterio.sample.sample_gen(dat, xy_pts)

    df_test = pd.DataFrame(columns = ['id', 'epsg', 'x', 'y', '(xy)', 'clim'])

    for i,(xy,clim) in enumerate(zip(xy_pts, clim_dat)):
        df_test.loc[i] = [
            (list(crs_data_points.values())[i]).id,
            (list(crs_data_points.values())[i]).epsg,
            xy[0], xy[1], xy, clim[0]
            ]
    print(df_test)

