import json
from pathlib import Path
import csv

data_dir = Path('./data/')
json_in = 'us-state-capitals.json'  # https://raw.githubusercontent.com/vega/vega/main/docs/data/us-state-capitals.json
csv_out = 'us-state-capitals.csv'

# Read json
with open(data_dir / json_in) as json_file:
    json_data = json.load(json_file)
print(json_data[0])

# convert json to csv with proper formating
if Path.is_file(data_dir / csv_out):
    raise FileExistsError(f'{csv_out} file already exists!')
else :
    
    with open(data_dir / csv_out, 'w', newline='') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=['id', 'epsg', 'x', 'y'])
        csv_writer.writeheader()
        states_formatted = {}
        for data in json_data:
            states_formatted['id'] = data['city']+'_'+data['state']
            states_formatted['epsg'] = 4326
            states_formatted['x'] = data['lon']
            states_formatted['y'] = data['lat']
            csv_writer.writerow(states_formatted)   