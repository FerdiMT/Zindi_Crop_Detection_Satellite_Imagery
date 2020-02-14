# Required libraries
import requests
from urllib.parse import urlparse
from pathlib import Path
from datetime import datetime

API = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJqa3dNMEpFTURsRlFrSXdOemxDUlVZelJqQkdPRFpHUVRaRVFqWkRNRVJGUWpjeU5ERTFPQSJ9.eyJpc3MiOiJodHRwczovL3JhZGlhbnRlYXJ0aC5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWU0MjhjNTU0NTU2ZjgwZGI5Y2ZlNjhjIiwiYXVkIjpbImh0dHBzOi8vYXBpLnJhZGlhbnQuZWFydGgvdjEiLCJodHRwczovL3JhZGlhbnRlYXJ0aC5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNTgxNTgxODE3LCJleHAiOjE1ODIxODY2MTcsImF6cCI6IlAzSXFMcWJYUm0xMEJVSk1IWEJVdGU2U0FEbjBTOERlIiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsInBlcm1pc3Npb25zIjpbXX0.XKDMWOSAuU56ejBP88hSAZ49mlCHlr2okJnFmCw24_KJ_q3NZOKZjQ8RddkM4uojruurJoqteIif2agcuhbE00puC83GlLuIact8svNPiI7cOKacqKvW0iCNwzd-uWNRdsv1fxQdgq07MF0EpJ-UL-wRrFFf-yQyRlIg2MEbE_Vkdm1rv7HgHp6AortBOiSJcTz2Wch_yweJJApJxAOS0Z-YSFF2Ivpsn8NX-Pg5zYdTRznDBudQZa-XVMBfO9AR9fEv28bPriaVINpGsSWT8Dp2wkNDDKOjA5S3q1i761jyHF6wbtUvVPKtORXp2wtxeoz6LNCXD48DQmgOUnodLQ'

output_path = Path("data/")

# these headers will be used in each request
headers = {
    'Authorization': f'Bearer {API}',
    'Accept':'application/json'
}


def get_download_url(item, asset_key, headers):
    asset = item.get('assets', {}).get(asset_key, None)
    if asset is None:
        print(f'Asset "{asset_key}" does not exist in this item')
        return None
    r = requests.get(asset.get('href'), headers=headers, allow_redirects=False)
    return r.headers.get('Location')


def download_label(url, output_path, tileid):
    filename = urlparse(url).path.split('/')[-1]
    outpath = output_path / tileid
    outpath.mkdir(parents=True, exist_ok=True)

    r = requests.get(url)
    f = open(outpath / filename, 'wb')
    for chunk in r.iter_content(chunk_size=512 * 1024):
        if chunk:
            f.write(chunk)
    f.close()
    print(f'Downloaded {filename}')
    return


def download_imagery(url, output_path, tileid, date):
    filename = urlparse(url).path.split('/')[-1]
    outpath = output_path / tileid / date
    outpath.mkdir(parents=True, exist_ok=True)

    r = requests.get(url)
    f = open(outpath / filename, 'wb')
    for chunk in r.iter_content(chunk_size=512 * 1024):
        if chunk:
            f.write(chunk)
    f.close()
    print(f'Downloaded {filename}')
    return


# paste the id of the labels collection:
collectionId = 'ref_african_crops_kenya_02_labels'

# these optional parameters can be used to control what items are returned.
# Here, we want to download all the items so:
limit = 100
bounding_box = []
date_time = []

# retrieves the items and their metadata in the collection
r = requests.get(f'https://api.radiant.earth/mlhub/v1/collections/{collectionId}/items', params={'limit':limit, 'bbox':bounding_box,'datetime':date_time}, headers=headers)
collection = r.json()


# retrieve list of features (in this case tiles) in the collection
for feature in collection.get('features', []):
    assets = feature.get('assets').keys()
    print("Feature", feature.get('id'), 'with the following assets', list(assets))

for feature in collection.get('features', []):

    tileid = feature.get('id').split('tile_')[-1][:2]

    # download labels
    download_url = get_download_url(feature, 'labels', headers)
    download_label(download_url, output_path, tileid)

    # download field_ids
    download_url = get_download_url(feature, 'field_ids', headers)
    download_label(download_url, output_path, tileid)


# paste the id of the imagery collection:
collectionId = 'ref_african_crops_kenya_02_source'

# these optional parameters can be used to control what items are returned.
# Here, we want to download all the items so:
limit = 500
bounding_box = []
date_time = []

# retrieves the items and their metadata in the collection
r = requests.get(f'https://api.radiant.earth/mlhub/v1/collections/{collectionId}/items', params={'limit':limit, 'bbox':bounding_box,'datetime':date_time}, headers=headers)
collection = r.json()


# List assets of the items
for feature in collection.get('features', []):
    assets = feature.get('assets').keys()
    print(list(assets))
    break #all the features have the same type of assets. for simplicity we break the loop here.


# This cell downloads all the multi-spectral images throughout the growing season for this competition.
# The size of data is about 1.5 GB, and download time depends on your internet connection.
# Note that you only need to run this cell and download the data once.
i = 0
for feature in collection.get('features', []):
    assets = feature.get('assets').keys()
    tileid = feature.get('id').split('tile_')[-1][:2]
    date = datetime.strftime(datetime.strptime(feature.get('properties')['datetime'], "%Y-%m-%dT%H:%M:%SZ"), "%Y%m%d")
    for asset in assets:
        i += 1
        if i > 0: # if resuming after it failed
          download_url = get_download_url(feature, asset, headers)
          download_imagery(download_url, output_path, tileid, date)