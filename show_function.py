
import matplotlib.pyplot as plt 
import urllib
import cStringIO
from PIL import Image
from multiprocessing import Process


def show_image(url):
    p = Process(target=plot_image, args=(url,))
    p.start()
    # p.join()

def plot_image(url):
    im = Image.open(cStringIO.StringIO(urllib.urlopen(url).read()))
    plt.imshow(im)
    frame1 = plt.gca()
    frame1.axes.get_xaxis().set_visible(False)
    frame1.axes.get_yaxis().set_visible(False)
    plt.show()
    # plt.axis('off')