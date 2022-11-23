import yaml
import rasterio
from rasterio.plot import show
from pyproj import Transformer
import matplotlib.pyplot as plt
import numpy as np


class SingleCoords :
    """
    A class to a single data point under geographic coordinate system standard conventions (EPSG:4326).

    ...

    Attributes
    ----------
    id : str
        identifier of single data point
    lat : float
        latitude (y-value, East-West lines) that range between -90 and +90 degrees.
    lon : float
        latitude (x-value, North-South lines) that range between -90 and +90 degrees.

    Methods
    -------
    info():
        Prints the SingleCoords information
    """
    def __init__(self, id, lat, lon) :
        """
        Constructor for SingleCoords object.

        Parameters
        ----------
        id : str
            identifier of single data point
        lat : float
            latitude (y-value, East-West lines) that range between -90 and +90 degrees.
        lon : float
            latitude (x-value, North-South lines) that range between -90 and +90 degrees.
        """
        self.id = id
        self.lat = lat
        self.lon = lon

    def info(self) :
        """
        Prints the SingleCoords object information.
        """
        print('id : {}\nEPSG:4326 / GPS coordinates :\n\tlat = {}\n\tlon = {}'.format(self.id, self.lat, self.lon))


#Read dataset (use with open() for proper open/close cycle)
with rasterio.open("../data/CHELSA_bio2_1981-2010_V.2.1.tif", masked=True) as dat :
    print("boundaries : {}".format(dat.bounds))
    data = dat.read()
    

    #transform GPS coords to raster EPSG  (which is the same in this case is 4326 so the same...)
    latlon = [(45.508888, -73.561668), (48.864716, 2.349014)]     # montreal + paris in Lat + Lon form
    transformer = Transformer.from_crs("epsg:4326", dat.crs)
    coords = [transformer.transform(x,y) for x,y in latlon]

    print(coords)

    #filter array ?
    # data_filt = np.where(data<5000, np.nan, data)
    
    # Extract data from transformed locations
    #* Beware of the correction factor + offset in Chelsa
    vals = list(rasterio.sample.sample_gen(dat, coords))
    for (lon,lat), val in zip(coords, vals):
        print(lon,lat,val[0])
