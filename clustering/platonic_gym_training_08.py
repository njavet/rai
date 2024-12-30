"""
kmeans image compression
"""

from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.metrics import pairwise_distances_argmin
import operator
import numpy as np
import matplotlib.pyplot as plt

from typing import Optional
from PIL import Image
import requests
from io import BytesIO


def download_img(url: str) -> Image:
    """
    This function fetches an image from the internet and returns a PIL.Image object
    see: https://pillow.readthedocs.io/en/stable/reference/Image.html

    we tested it mainly on images from wikimedia
    """

    # have to set a fake user-agent so we dont get blocked by wikimedia
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}
    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        # if you hit this exception, consider using another image
        raise Exception(f'download failed:\n{url}')

    return Image.open(BytesIO(r.content)).convert('RGB')


def img2arr(img: Image) -> np.array:
    """
    convert a PIL.Image object to a numpy array
    the resulting array has 3 dimensions [height, width, 3]
    the last dimension contains rgb values

    the rgb values are normalized to be between 0. and 1.
    """
    return np.asarray(img) / 255


def arr2img(arr: np.array) -> Image:
    """
    convert a numpy array back into a PIL.Image object
    we expect the rgb values of the array to be between 0. and 1.
    """
    return Image.fromarray((arr * 255).astype(np.int8), mode='RGB')


def rg_chromaticity(color_arr: np.array) ->  np.array:
    """
    helper function
    """
    sums = np.sum(color_arr, axis=1, keepdims=True)
    normed = np.divide(color_arr, sums, where=sums > 0.)
    return normed


def rg_chroma_plot(ax, img_arr: np.array, centers: Optional[np.array] = None):
    """
    plot an image in rg-chromaticity space
    this is a 2D representation of 3D rgb data
    refer to wikipedia for details: https://en.wikipedia.org/wiki/Rg_chromaticity

    Note: the resulting plot will not accurately reflect the original euclidean distances

    inputs:
    img_arr: a numpy array with 3 dimensions [height, width, 3] representing an image
    centers: a numpy array with 2 dimensions [n_centers, 3] representing the cluster centers
    """
    colors = np.copy(img_arr).reshape((-1, 3))
    colors = np.unique(colors, axis=0)
    img_rg = rg_chromaticity(colors)
    ax.scatter(img_rg[:, 0], img_rg[:, 1], c=[tuple(colors[i]) for i in range(colors.shape[0])], s=.1)

    if centers is not None:
        crg = rg_chromaticity(centers)
        ax.scatter(crg[:, 0], crg[:, 1], c='black', marker='x', s=25.)

    ax.set_xlabel('red')
    ax.set_ylabel('green')


def replace_nearest_color(img_arr: np.array, centers: np.array):
    """
    replace each pixel color in `img_arr` by the closest color in `centers`

    input:
    img_arr: a numpy array with 3 dimensions [height, width, 3] representing an image
    centers: a numpy array with 2 dimensions [n_centers, 3] representing the cluster centers
    """
    colors = img_arr.reshape((-1, 3))
    labels = pairwise_distances_argmin(colors, centers)
    compressed = labels.reshape(img_arr.shape[:2])
    replaced = centers[compressed]
    return replaced


def main():
    img_url = 'https://upload.wikimedia.org/wikipedia/commons/d/d7/RGB_24bits_palette_sample_image.jpg'

    img = download_img(img_url)
    img_arr = img2arr(img)

    fig = plt.figure(figsize=(32, 16))
    # visualize the np.array version of the same image
    pixels = img_arr.reshape(-1, 3)
    # rg_chroma_plot(img_arr)

    elbow = []
    scs = []
    for k in range(2, 9):
        km = KMeans(n_clusters=k)
        labels = km.fit_predict(pixels)
        sc = silhouette_score(pixels, labels)
        print(f'silhouette score for {k} = {sc}')
        scs.append((k, sc))
        elbow.append((k, km.inertia_))

    ax = fig.add_subplot(231)
    xs, ys = zip(*elbow)
    ax.set_title('Elbow Plot')
    ax.set_xlabel('Number of clusters')
    ax.set_ylabel('sum of squared distance of point to closest centroid')
    ax.grid()
    ax.plot(xs, ys, label='elbow', marker='x')

    ax = fig.add_subplot(232)
    xs, ys = zip(*scs)
    ax.set_title('Silhouette Plot')
    ax.set_xlabel('Number of clusters')
    ax.set_ylabel('Silhouette Score')
    ax.grid()
    ax.plot(xs, ys, label='silhouette', marker='x')

    k, _ = sorted(scs, key=operator.itemgetter(1), reverse=True)[0]
    km = KMeans(n_clusters=k)
    labels = km.fit_predict(pixels)

    # generate 8 random colors for illustration
    # random_centers = np.random.default_rng(0x101).random(size=(8, 3))

    # plot the random centers on top of the colors of the image
    ax = fig.add_subplot(233)
    ax.set_title('Chroma plot')
    rg_chroma_plot(ax, img_arr, km.cluster_centers_)
    
    # replace original colors by their nearest neighbors out of the candidate centers
    ax = fig.add_subplot(234)
    ax.set_title('Original Image')
    ax.imshow(img_arr)

    ax = fig.add_subplot(235)
    ax.set_title('Compressed image')
    replaced = replace_nearest_color(img_arr, km.cluster_centers_)

    # convert to PIL.Image and visualize

    ax.imshow(arr2img(replaced))
    plt.show()


if __name__ == '__main__':
    main()

