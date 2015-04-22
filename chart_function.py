import matplotlib.pyplot as plt
import matplotlib as mpl

def barchart(data, ticks, title="Barchart"):
    mpl.rcParams['toolbar'] = 'None'
    fig = plt.figure()
    fig.canvas.set_window_title(title) 
    n = len(data)
    x = [i+0.5 for i in range(n)]
    plt.bar(x, data, 1)
    plt.xticks(x, [str(t) for t in ticks])
    plt.show()

def piechart(data, labels, title="Piechart"):
    mpl.rcParams['toolbar'] = 'None'
    fig = plt.figure(figsize=(6,6))
    fig.canvas.set_window_title(title) 
    plt.pie(data,labels=labels)
    plt.show()