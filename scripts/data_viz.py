import yaml
import rasterio
from rasterio.plot import show
import matplotlib.pyplot as plt


#Read dataset (use with open() for proper open/close cycle)
with rasterio.open("../data/CHELSA_kg0_1981-2010_V.2.1.tif", masked=True) as dat :
    print("boundaries : {}".format(dat.bounds))
    data = dat.read()
        
    #Plot with colorbar
    data_res = rasterio.plot.reshape_as_image(data) # reshape arr as img
    fig, ax = plt.subplots(figsize=(10,10))
    img = plt.imshow(data_res)
    fig.colorbar(img, ax=ax)
    plt.show()