# Vectorize-Address

Simple configurable script to create ESRI shapefile from a single geocoded address.

## Requirements

- Python 3
- [GEOS](https://trac.osgeo.org/geos/)
    - Ubuntu: `sudo apt install libgeos-dev`
    - Mac: `brew install geos`

## Installation

```
git clone git@github.com:hdbhdb/vectorizeaddress.git
cd vectorizeaddress
pip install -r requirements.txt
chmod +x vectaddy.py
sudo ln vectaddy.py /usr/local/bin/vectaddy
```

## Setup

Geocoding results from Google Maps are generally much higher quality than OpenStreetMaps. The default is to use OSM unless a [Google Maps API token](https://developers.google.com/maps/documentation/embed/get-api-key) has been added to the configuration using `vectaddy -G [TOKEN]`. 

To make it simpler to perform multiple queries within the same city or country, you can specify a default location using `vectaddy -L [LOCATION]` which will append the specified location to all queries.

## Usage

```
vectaddy [-h] [-o [OUTPUT]] [-L [DEFAULT_LOCATION]] [-G [GOOGLE_API]]
                [input]

geocode address and plot point as shp file

positional arguments:
  input                 address to geocode

optional arguments:
  -h, --help            show this help message and exit
  -o [OUTPUT], --output [OUTPUT]
                        output filename for shp file. if no output is
                        specified, print point coordinates.
  -L [DEFAULT_LOCATION], --default-location [DEFAULT_LOCATION]
                        configure default location (city, state, country,
                        etc.) to addend to searches
  -G [GOOGLE_API], --google-api [GOOGLE_API]
                        add Google Maps API key to configuration
```
