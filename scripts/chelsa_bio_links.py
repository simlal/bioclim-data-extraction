import yaml
import subprocess
import requests

# Load yaml and set vars

with open('../config.yaml') as f:
    config = yaml.safe_load(f)

chelsa_urlfile = config["url-files"]["chelsa"]
worldclim_urlfile = config["url-files"]["worldclim"]
test_urlfile = config["url-files"]["test"]

# wget with subprocess
def wget_py():
    wget = subprocess.Popen(['wget', 'https://www.w3schools.com/images/colorpicker2000.pngg'], stdout=subprocess.PIPE, text=True)
    if wget.stderr == 0 :
        print(wget.stdout)
    else : print(wget.stderr)
    


# Parse data
def parse_urlfile(urlfile):
    with open(urlfile) as f:
        urls = [line.rstrip() for line in f]
        for url in urls : 
            response = requests.get(url)
            if response.status_code == 200 : 
                print(url)
            else :
                print("URL {} cannot be downloaded. Status code : {}".format(url,response.status_code))

parse_urlfile(test_urlfile)

# Multiprocessing/parralel download
