import yaml
import rasterio
from rasterio.plot import show
from rasterio.crs import CRS
import pyproj
from pyproj import Transformer
import matplotlib.pyplot as plt
import numpy as np
import re

EPSG_codes = [int(code) for code in pyproj.get_codes('EPSG', 'CRS')]


class SingleCoords :
    """
    A class to a single data point under geographic coordinate system standard (CRS) from reference to a pixel map locations.

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
        Prints the SingleCoords information

    transform_gps(epsg_out):
        Transforms the coordinates to the desired EPSG coordinate reference system
    """
    def __init__(self, id, epsg, x, y,) :
        """
        Constructor for SingleCoords object.

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
        """
        self.id = id
        self.epsg = epsg
        self.x = x
        self.y = y
        self.coord = (self.x,self.y)

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
        Prints the SingleCoords object information.
        """
        return('id : {}\nEPSG : {}\nMap coordinates :\n\tx = {}\n\ty = {}'.format(self.id, self.epsg, self.x, self.y))

    
    def transform_GPS(self,epsg_out) :
        """
        Transforms the coordinates to the desired EPSG coordinate reference system
        
        Returns lat : float
            latitude (y-value, East-West lines) that range between -90 and +90 degrees.
        lon : float
            latitude (x-value, North-South lines) that range between -90 and +90 degrees.
        """
        transformer = Transformer.from_crs(self.epsg, CRS.from_epsg(epsg_out))
        x_out, y_out = transformer.transform(self.x, self.y)
        return (x_out, y_out)
    
test = SingleCoords('c1',4326,45.508888,-73.561668)
transfo = test.transform_GPS(3005)
print(transfo)









# #transform GPS coords to raster EPSG  (which is the same in this case is 4326 so the same...)
# latlon = [(45.508888, -73.561668), (48.864716, 2.349014)]     # montreal + paris in Lat + Lon form
# transformer = Transformer.from_crs("epsg:4326", dat.crs)
# coords = [transformer.transform(x,y) for x,y in latlon]

# print(coords)

# #filter array ?
# # data_filt = np.where(data<5000, np.nan, data)

# # Extract data from transformed locations
# #* Beware of the correction factor + offset in Chelsa
# vals = list(rasterio.sample.sample_gen(dat, coords))
# for (lon,lat), val in zip(coords, vals):
#     print(lon,lat,val[0])
