
import matplotlib.pyplot as plt 
import matplotlib as mpl
import urllib
import cStringIO
from PIL import Image
from multiprocessing import Process

def show_image(url, title='Image'):
    p = Process(target=plot_image, args=(url, title))
    p.start()
    # p.join()

def plot_image(url,title):
    mpl.rcParams['toolbar'] = 'None'
    fig = plt.figure() 
    fig.canvas.set_window_title(title) 
    im = Image.open(cStringIO.StringIO(urllib.urlopen(url).read()))
    plt.imshow(im)
    frame = plt.gca()
    frame.axes.get_xaxis().set_visible(False)
    frame.axes.get_yaxis().set_visible(False)
    plt.show()
    # plt.axis('off')