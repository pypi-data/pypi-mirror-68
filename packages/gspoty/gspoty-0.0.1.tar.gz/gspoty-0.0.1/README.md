# Gspoty

Spotify List metadata extractor

## Environment variables

This script loads a JSON file with the form specified by [example_key.json](./example_keys.json), 
this file must be named `key.json` , and should have valid client / secret values from Spotify and a valid device di from Google Music

**You should get those keys from the spotify developers page and google music oauth2. Please see spotipy and gmusic API for further information**

## Requirements

Basically with Python3 and pip you are set up! pip will handle dependencies using
requirements file, but specifically the only dependency appart from a default 
python 3 environment will be [ `spotipy` ](https://pypi.org/project/spotipy/), and [ `gmusicapi` ](https://pypi.org/project/gmusicapi/) see [ `requirements.txt` ](./requirements.txt) file for specific version. 

* Python 3
* pip
* spotipy
* gmusicapi

`pip install -r requirements.txt` 

## Run the module

```bash
python -m gspoty https://open.spotify.com/playlist/74OoKks94WOn8h14OwLChP
```

optionally you can pass the location to json file with the required keys 

```
python -m gspoty https://open.spotify.com/playlist/74OoKks94WOn8h14OwLChP /tmp/keys_custom.json
```