# Required libraries
#import tifffile as tiff
import datetime


def load_file(fp):
    """Takes a PosixPath object or string filepath
    and returns np array"""

    return tiff.imread(fp.__str__())


# List of dates that an observation from Sentinel-2 is provided in the training dataset
dates = [datetime.datetime(2019, 6, 6, 8, 10, 7),
         datetime.datetime(2019, 7, 1, 8, 10, 4),
         datetime.datetime(2019, 7, 6, 8, 10, 8),
         datetime.datetime(2019, 7, 11, 8, 10, 4),
         datetime.datetime(2019, 7, 21, 8, 10, 4),
         datetime.datetime(2019, 8, 5, 8, 10, 7),
         datetime.datetime(2019, 8, 15, 8, 10, 6),
         datetime.datetime(2019, 8, 25, 8, 10, 4),
         datetime.datetime(2019, 9, 9, 8, 9, 58),
         datetime.datetime(2019, 9, 19, 8, 9, 59),
         datetime.datetime(2019, 9, 24, 8, 9, 59),
         datetime.datetime(2019, 10, 4, 8, 10),
         datetime.datetime(2019, 11, 3, 8, 10)]

bands = ['B01', 'B02', 'B03', 'B04', 'B05', 'B06', 'B07', 'B08', 'B8A', 'B09', 'B11', 'B12', 'CLD']


# Not super efficient but  ¯\_(ツ)_/¯
import pandas as pd

row_locs = []
col_locs = []
field_ids = []
labels = []
tiles = []
for tile in range(4):
  fids = f'/content/data/0{tile}/{tile}_field_id.tif'
  labs = f'/content/data/0{tile}/{tile}_label.tif'
  fid_arr = load_file(fids)
  lab_arr = load_file(labs)
  for row in range(len(fid_arr)):
    for col in range(len(fid_arr[0])):
      if fid_arr[row][col] != 0:
        row_locs.append(row)
        col_locs.append(col)
        field_ids.append(fid_arr[row][col])
        labels.append(lab_arr[row][col])
        tiles.append(tile)

df = pd.DataFrame({
    'fid':field_ids,
    'label':labels,
    'row_loc': row_locs,
    'col_loc':col_locs,
    'tile':tiles
})

print(df.shape)
print(df.groupby('fid').count().shape)
df.head()

# Sample the bands at different dates as columns in our new dataframe
col_names = []
col_values = []

for tile in range(4):  # 1) For each tile
    print('Tile: ', tile)
    for d in dates:  # 2) For each date
        print(str(d))
        d = ''.join(str(d.date()).split('-'))  # Nice date string
        t = '0' + str(tile)
        for b in bands:  # 3) For each band
            col_name = d + '_' + b

            if tile == 0:
                # If the column doesn't exist, create it and populate with 0s
                df[col_name] = 0

            # Load im
            im = load_file(f"data/{t}/{d}/{t[1]}_{b}_{d}.tif")

            # Going four levels deep. Each second on the outside is four weeks in this loop
            # If we die here, there's no waking up.....
            vals = []
            for row, col in df.loc[df.tile == tile][
                ['row_loc', 'col_loc']].values:  # 4) For each location of a pixel in a field
                vals.append(im[row][col])
            df.loc[df.tile == tile, col_name] = vals
df.head()

df.to_csv('sampled_data.csv', index=False)