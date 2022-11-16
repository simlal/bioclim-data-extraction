import yaml
import requests
import time

# Download zip files
def download_single(urlfile, savepath):
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
                print("Server response OK from {}, starting to download {}".format((url.split("/")[2]), filename))
                with open(savepath+filename, 'wb') as f :
                    chunksize = 1024 * 10000
                    start_time = time.time()
                    for n, chunk in enumerate(response.iter_content(chunk_size=chunksize)) :
                        percent = (n * chunksize / total_size) * 100
                        now_time = time.time()
                        current_speed = (n * chunksize) / (now_time - start_time) / 1000000
                        print(
                            "{} #_progress_# : {:.2f} % completed of {:.1f} MB downloaded [ current speed of  {:.1f} MB/s ]"
                            .format(filename, percent, total_size/1000000, current_speed), end="\r"
                            )
                        time.sleep(0.1)
                        f.write(chunk)
                    print("Done downloading {} in {} !".format(filename, (now_time-start_time)))
            else :
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

    download_single(test_urls, download_path)