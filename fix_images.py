import os
from PIL import Image, ImageOps
import time

root = '/home/sbalan7/Desktop/Code/charting-Gaia/plots/'
clusters = os.listdir(root+'raw/')
print(len(clusters))

graph_l = 65
graph_u = 54
graph_r = 1062
graph_b = 551
i = 0
tt = 0

for cluster in clusters:
    tic = time.time()
    
    path = root + 'raw/' + cluster
    im = Image.open(path)
    im = im.crop((graph_l, graph_u, graph_r, graph_b))

    width, height = im.size
    im = im.resize((height, height), Image.ANTIALIAS)

    im = im.transpose(Image.ROTATE_90)
    im = ImageOps.mirror(im)
    im = ImageOps.flip(im)
    
    im.save(root+'mod/'+cluster, quality=100)

    toc = time.time()
    tt += (toc - tic)
    i += 1
    print(f'Iteration {i}/{len(clusters)}: writing {cluster}, time taken = {toc-tic}')

print(f'Conversion complete in {tt} seconds')
