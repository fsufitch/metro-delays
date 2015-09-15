import json, requests, sys

from metrodelay.common.config import Configuration

def get_metro_network(config):
    api_key = config.get('primary_key', filekey='wmata_api')
    base_url = config.get('base_url', filekey='wmata_api')
    
    lines_url = base_url + '/Rail.svc/json/jLines'
    response = requests.get(lines_url, headers={'api_key': api_key})
    lines = {}

    for line_data in response.json()['Lines']:
        line_id = line_data['LineCode']
        line_name = line_data['DisplayName']

        lines[line_id] = {
            'id': line_id,
            'name': line_name,
            }

    stations_url = base_url + '/Rail.svc/json/jStations'
    response = requests.get(stations_url, headers={'api_key': api_key})
    stations = {}

    for station_data in response.json()['Stations']:
        station_id = station_data['Code']
        station_name = station_data['Name']
        station_lines = [station_data['LineCode%s'%x] for x in range(1,5)]
        station_lines = list(filter(lambda x: x, station_lines))
        stations[station_id] = {
            'id': station_id,
            'name': station_name,
            'lines': station_lines,
            }

        for line_id in station_lines:
            if 'stations' not in lines[line_id]:
                lines[line_id]['stations'] = []
            lines[line_id]['stations'].append(station_id)

    network = {
        'lines': lines,
        'stations': stations,
        }
    
    return network

def dump_metro_network(metro_network):
    print(json.dumps(metro_network))

def main():
    main_conf = sys.argv[1]
    config = Configuration(main_conf)
    metro_network = get_metro_network(config)
    dump_metro_network(metro_network)
