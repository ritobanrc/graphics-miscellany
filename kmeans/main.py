#!/usr/bin/python3
import requests
from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt
import matplotlib.animation as anim
import matplotlib as mpl
import numpy as np

width = height = 800
k = 12 
fig = plt.figure()

response = requests.get(f'https://picsum.photos/{width}/{height}/?random')
img = (Image.open(BytesIO(response.content)))
img = np.array(img)
flattened = np.reshape(img, (width*height, 3))

print('Image Recieved: ', response.headers)

def init_centroids(points, k):
    centroids = points.copy()
    np.random.shuffle(centroids)
    return centroids[:k]

centroids = init_centroids(flattened, k)
print('Centroids: ', centroids)


ax1 = fig.add_subplot(131)
ax1.imshow(img)
ax1.set_xticks([])
ax1.set_yticks([])

ax2 = fig.add_subplot(132)
im = ax2.imshow(img, animated=True)
ax2.set_xticks([])
ax2.set_yticks([])

# Create the subplot to show swatches of color
ax3 = fig.add_subplot(133)
ax3.set_xlim((0,k))
ax3.set_ylim((0, 1))
ax3.set_xticks([])
ax3.set_yticks([])
ax3.set_aspect('equal')


def closest_centroid(points, centroids):
    sq_dists = ((points - centroids[:, np.newaxis])**2).sum(axis=2)
    return np.argmin(sq_dists, axis=0)


def move_centroids(points, closest, centroids):
    return np.array([points[closest==c].mean(axis=0) 
                     for c in range(centroids.shape[0]) if np.any(closest == c)])

def mean_squared_error(points, closest, centroids):
    # import ipdb; ipdb.set_trace()
    return np.sum([np.linalg.norm([points[closest==c] - centroids[c]]) for c in range(centroids.shape[0])])
    # return np.sum([(points[closest==c] - centroids[c])**2 for c in range(centroids.shape[0])])

def update(*args):
    global centroids

    closest = closest_centroid(flattened, centroids)
    segmented = centroids[np.reshape(closest, (width, height))]/255

    print('Error: ', mean_squared_error(flattened, closest, centroids))
    dirty=[]

    im.set_array(segmented)
    dirty.append(im)
    for x, color in enumerate(centroids):
        dirty.append(ax3.add_patch(mpl.patches.Rectangle((x, 0), 1, 1, facecolor=color/255)))

    centroids = move_centroids(flattened, closest, centroids)
    return dirty

ani = anim.FuncAnimation(fig, update, interval=20, blit=True)
plt.show()
