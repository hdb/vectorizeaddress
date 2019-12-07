from shapely.geometry import mapping
import fiona
from fiona.crs import from_epsg
from shapely.geometry import Point
import geocoder
import argparse
from pathlib import Path
import yaml
import os

def parse():

    parser = argparse.ArgumentParser(
        prog='vectaddy',
        description='geocode address and plot point as shp file',
        )

    parser.add_argument('input', nargs='?', default=None, help='address to geocode')
    parser.add_argument('-o', '--output', nargs='?', default=None, help='output filename for shp file. if no output is specified, print point coordinates.')
    parser.add_argument('-L', '--default-location', nargs='?', default=None, help='configure default location (city, state, country, etc.) to addend to searches')
    parser.add_argument('-G', '--google-api', nargs='?', default=None, help='add Google Maps API key to configuration')

    args = parser.parse_args()
    return args

def configureAPIKey(apikey):

    try:
        config = yaml.safe_load(open(config_file))
    except:
        config = {}

    config['mapsapikey'] = apikey

    with open(config_file, 'w') as outfile:
        yaml.dump(config, outfile, default_flow_style=False)
    
    print('added key to ' + config_file)

    return apikey

def configureLocation(location):

    try:
        config = yaml.safe_load(open(config_file))
    except:
        config = {}

    config['location'] = location

    with open(config_file, 'w') as outfile:
        yaml.dump(config, outfile, default_flow_style=False)
    
    print('made ' + location + ' default location in ' + config_file)

    return location


def main():

    args = parse()

    global config_file
    config_file = str(Path.home())+"/.plotaddress-conf.yaml"

    if args.google_api is not None:
        configureAPIKey(args.google_api)

    if args.default_location is not None:
        configureLocation(args.default_location)

    if args.input is None:
        print('no address specified. exiting...')
        exit()
   
    try:
        config = yaml.safe_load(open(config_file))
    except:
        config = {}

    global address
    address = args.input

    try:
        search = address + ", " + config['location']
    except:
        search = address

    try:
        g = geocoder.google(search, key=config['mapsapikey'])
    except:
        #print('Google Maps API token not set in config. Go to https://developers.google.com/maps/documentation/embed/get-api-key for more information on Maps API tokens and use "-t TOKEN [-C CONFIG_FILE]" to set token.')
        print('No Google Maps API found in config.\nTo enable Google Maps geocoding, add API token with -G.\nUsing free OSM geocoding.')
        g = geocoder.osm(search)
    address_coordinates = g.latlng

    point = Point(address_coordinates[1],address_coordinates[0])


    schema = {
        'geometry': 'Point',
        'properties': {'id': 'int'},
    }

    if args.output is not None:

        if not args.output.endswith(".shp"):
            try:
                os.mkdir(args.output)
                outputfile = args.output + '/' + os.path.splitext(os.path.basename(args.output))[0] + ".shp"
            except:
                outputfile = args.output + '/' + os.path.splitext(os.path.basename(args.output))[0] + ".shp"
        else:
            outputfile = args.output

        # Write a new Shapefile
        with fiona.open(outputfile, 'w', 'ESRI Shapefile', schema, crs=from_epsg(4326)) as c:

            c.write({
                'geometry': mapping(point),
                'properties': {'id': 123},
            }
        )

        print('saved', address, 'at', address_coordinates, 'to', outputfile)
    else:
        print(address, 'at', address_coordinates)

if __name__ == '__main__':
    main()