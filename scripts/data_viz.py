import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys

#TODO Define functions for graphing instead of running main

# Interactive mapbox + dotplot for bioclim 1-19 +_elevation
if __name__ == "__main__":
    # Input csv file
    in_file = sys.argv[1]

    # Verify arg count + file type
    if len(sys.argv) != 2:
        raise IOError('This script must take 1 argument. Exmaple : python bioclim.csv')
    elif not in_file.endswith(".csv"):
        raise IOError("File must be a csv")
    else :
        # Read infile
        us_capitals_bioclim = pd.read_csv(in_file)
        print(us_capitals_bioclim.set_index('id').head())   # sanity check

        # Get bioclim + elevation : name (units)
        bioclim_elev_fields = list(us_capitals_bioclim.columns)[4:]

        # 1st viz : Create mapbox with scatterpoint displaying all bioclim vars upon hover (colored markers by elevation)
        fig = px.scatter_mapbox(us_capitals_bioclim, lat="lat", lon="lon", color_discrete_sequence="DarkRed",
                                hover_name="id", color="elevation_Meters", hover_data=bioclim_elev_fields,
                                zoom=3, height=600, title="Bioclim and elevation map for US Capitals"
                            )
        fig.update_layout(mapbox_style="stamen-terrain")
        fig.update_layout(margin={"r":0,"t":40,"l":0,"b":0})
        # fig.update_layout(mapbox_bounds={"west": -180, "east": -50, "south": 20, "north": 90}) #! IN THE DOCS BUT RAISE ERROR
        fig.show()

        # 2nd viz : Create scatter plot with categorical data (capitals) for each bioclim + elev vars
        fig = go.Figure()

        for column in bioclim_elev_fields:
            fig.add_trace(
                go.Scatter(
                    x = us_capitals_bioclim[column],
                    y = us_capitals_bioclim["id"],
                    mode = 'markers',
                    name = column,
                    marker = dict(
                        size = 10,
                        color = us_capitals_bioclim[column],
                        colorbar = dict(
                            # orientation = 'h',  #! mixup in documentation : somehow it shows the orientation ppty of scatter.marker object in doc yet in raise error not there 
                            title=column
                        )
                    )
                )
            )

        # Generate buttons for dropdown with update method
        buttons_bioclim = []
        for i,field in enumerate(bioclim_elev_fields) : 
            buttons_bioclim.append(
                dict(label=field, method='update',
                args=list([
                    dict(visible=[True if bioclim_elev_fields[i] == field else False for field in bioclim_elev_fields]),
                    dict(title=field, showlegend=False)
                    ])
                )
            )

        # Dropdown updating with bioclim + elev as buttons
        fig.update_layout(
            updatemenus=[go.layout.Updatemenu(
                active=0,
                buttons=buttons_bioclim
            )]
        )
        # Update title
        fig.update_layout(title_text="Bioclim and elevation map for US Capitals")

        fig.show()


'''
import rasterio
from rasterio.plot import show
import matplotlib.pyplot as plt

# For displaying a raster map with a colorbar
with rasterio.open("./data/bioclim/CHELSA_bio1_1981-2010_V.2.1.tif", masked=True) as dat :
    print("boundaries : {}".format(dat.bounds))
    data = dat.read()
        
    #Plot with colorbar
    data_res = rasterio.plot.reshape_as_image(data) # reshape arr as img
    fig, ax = plt.subplots(figsize=(10,10))
    img = plt.imshow(data_res)
    fig.colorbar(img, ax=ax)
    plt.show()
'''