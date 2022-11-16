import yaml
import requests
import time
from functools import partial

# Get urls from url-file
def get_urls(urlfile):
    with open(urlfile) as f:
        urls = [line.rstrip() for line in f]
        return urls

# Download a single file
def download_single(url, savepath):
    filename = url.split("/")[-1]
    try :
        response = requests.get(url, stream=True)
        print("\n####   Trying get request to download...   ####")
        # Calc file size in MB
        total_size = (float(response.headers['Content-Length']))/1000000
        print("{} is {:.1f} MB".format(filename, total_size))
        # Download in chunks of 5 MB and save to disk
        if response.status_code == 200 : 
            print("Server response OK from {}, starting to download {}".format((url.split("/")[2]), filename))
            with open(savepath+filename, 'wb') as f :
                chunksize = 1024 * 5000
                start_time = time.time()
                for n, chunk in enumerate(response.iter_content(chunk_size=chunksize)) :
                    percent = (n * chunksize / (total_size*1000000)) * 100
                    now_time = time.time()
                    current_speed = (n * chunksize) / (now_time - start_time) / 1000000
                    print(
                        "Progress for {} : {:.2f} % completed of {:.1f} MB downloaded [ current speed of  {:.1f} MB/s ]"
                        .format(filename, percent, total_size, current_speed), end="\r"
                        )
                    time.sleep(0.1)
                    f.write(chunk)
                end_time = time.time()
                print(
                    "Progress for {} : 100.00 % completed of {:.1f} MB downloaded [ average speed of  {:.1f} MB/s ]         "
                    .format(filename, total_size, total_size/(end_time-start_time)), end="\r"
                    )
                print()
                print(
                    "Done downloading {} in {:.2f} seconds !"
                    .format(filename, end_time-start_time,)
                    )
                    
    except :
        print("File {} cannot be downloaded. Status code : {}".format(filename, response.status_code))
    return savepath+filename

if __name__ == "__main__" :
    
    # Load yaml and set vars
    with open('config.yaml') as f:
        config = yaml.safe_load(f)
    chelsa_urls = config["url-files"]["chelsa"]
    worldclim_urls = config["url-files"]["worldclim"]
    test_urls = config["url-files"]["test"]
    download_path = config["download-path"]

    # Ask url-file input to download
    possible_answer = ["chelsa", "worldclim", "both"]
    while True :
        to_download = input(
            "\nchelsa : for Chelsa bioclim19 dataset \n"
            "worldclim : for WorldClim bioclim19 dataset \n"
            "both : for Chelsa and WorldClim bioclim datasets \n\n"
            "Enter which dataset(s) you would like to download.\n"
            )
        if to_download not in possible_answer :
            print("Please enter an exact name :)")
            continue
        else : 
            print("Starting to download {} dataset(s)".format(to_download))
            break

    # Download all user-wanted files
    download_fixpath = partial(download_single, savepath = download_path)   # fix download_single with a single arg
    # Chelsa dataset only
    if to_download == "chelsa" :
        chelsa = get_urls(chelsa_urls)
        list(map(download_fixpath, chelsa))
    
    elif to_download == "worldclim" :
        worldclim = get_urls(worldclim_urls)
        list(map(download_fixpath, worldclim))

    else : 
        chelsa = get_urls(chelsa_urls)
        worldclim = get_urls(worldclim_urls)
        list(map(download_fixpath, chelsa))
        list(map(download_fixpath, worldclim))