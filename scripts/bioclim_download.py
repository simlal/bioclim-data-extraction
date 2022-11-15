import yaml
import requests
import time
import sys
# from tqdm.auto import tqdm

# Load yaml and set vars

with open('config.yaml') as f:
    config = yaml.safe_load(f)

chelsa_urls = config["url-files"]["chelsa"]
worldclim_urls = config["url-files"]["worldclim"]
test_urls = config["url-files"]["test"]
download_path = config["download-path"]


# Download zip files
def download_zip(urlfile, filepath):
    with open(urlfile) as f:
        urls = [line.rstrip() for line in f]
        for url in urls :
            filename = url.split("/")[-1]
            response = requests.get(url, stream=True)
            # Check file size
            total_size = float(response.headers['Content-Length'])
            print("{} is {:.1f} MB".format(filename, total_size/1000000))
            # Download in chunks of 1 MB
            if response.status_code == 200 : 
                print("Server response OK from {}, Downloading {}".format(''.join(url.split(".")[:3]), filename))
                with open(filename, 'wb') as f :
                    chunksize = 1024 * 1000
                    for n, chunk in enumerate(response.iter_content(chunk_size=chunksize)) :
                        percent = (n * chunksize / total_size) * 100 
                        sys.stdout.write("\r{:.2f} % of {:.1f} MB  downloaded".format(percent, total_size/1000000))
                        time.sleep(0.1)
                        sys.stdout.flush()
                        f.write(chunk)
            else :
                print("File {} cannot be downloaded. Status code : {}".format(filename, response.status_code))
            
            return filepath+filename

download_zip(test_urls, download_path)

# Multiprocessing/parralel download
