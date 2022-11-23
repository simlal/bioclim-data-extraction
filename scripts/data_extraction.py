import yaml
import rasterio
from rasterio.plot import show
from pyproj import Transformer
import matplotlib.pyplot as plt
import numpy as np


# Read dataset (use with open() for proper open/close cycle)
with rasterio.open("../data/CHELSA_bio2_1981-2010_V.2.1.tif", masked=True) as small :
    print("boundaries : {}".format(small.bounds))
    sm = small.read()
    

    #transform GPS coords to raster EPSG  (which is the same in this case is 4326 so the same...)
    latlon = [(45.508888, -73.561668), (48.864716, 2.349014)]     # montreal + paris in Lat + Lon form
    transformer = Transformer.from_crs("epsg:4326", small.crs)
    coords = [transformer.transform(x,y) for x,y in latlon]

    print(coords)

    #filter array ?
    # sm_filt = np.where(sm<5000, np.nan, sm)
    
    # Extract data from transformed locations
    #* Beware of the correction factor + offset in Chelsa
    vals = list(rasterio.sample.sample_gen(small, coords))
    for (lon,lat), val in zip(coords, vals):
        print(lon,lat,val[0])

    #Plot with colorbar
    sm_res = rasterio.plot.reshape_as_image(sm) # reshape arr as img
    fig, ax = plt.subplots(figsize=(10,10))
    img = plt.imshow(sm_res)
    fig.colorbar(img, ax=ax)
    plt.show()