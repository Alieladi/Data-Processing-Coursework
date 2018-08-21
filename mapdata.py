import math
import urllib.request
import sys
from PIL import Image

def deg2num(lat_deg, lon_deg, zoom): # source http://wiki.openstreetmap.org/wiki/Slippy_map_tilenames#Derivation_of_tile_names
	lat_rad = math.radians(lat_deg)
	n = 2.0 ** zoom
	xtile = int((lon_deg + 180.0) / 360.0 * n)
	ytile = int((1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n)
	return (xtile, ytile) # accessible like a list


x_topleft = float(sys.argv[1])
y_topleft = float(sys.argv[2])
x_downright = float(sys.argv[3])
y_downright = float(sys.argv[4])
name_picture = sys.argv[5]

tile_topleft = deg2num(x_topleft,y_topleft, 13)
tile_downright = deg2num(x_downright,y_downright, 13)


"""
tile_topleft_x = tile_topleft[0]
tile_downright_x = tile_downright[0]
tile_topleft_y = tile_topleft[1]
tile_downright_y = tile_downright[1]
"""

tiles_in_x = abs(tile_topleft[0] - tile_downright[0]) +1 # number of tiles in x-axis
tiles_in_y = abs(tile_topleft[1] - tile_downright[1]) +1 # number of tiles in y-axis
print(tiles_in_x)
print(tiles_in_y)
im = Image.new("RGB", (tiles_in_x * 256, tiles_in_y * 256))

for i in range(tiles_in_x): # tiles_in_x: in the exple 9
	for j in range(tiles_in_y): # tiles_in_y: in the exple 6		
		data = urllib.request.urlopen("http://tile.openstreetmap.org/13/%s/%s.png"%(tile_topleft[0] + i, tile_topleft[1] + j))
		img = Image.open(data)
		im.paste(img,(i*256, j*256)) # Tiles are 256 × 256 pixel PNG files

im.save(name_picture, "PNG")