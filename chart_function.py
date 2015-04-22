import matplotlib.pyplot as plt
import matplotlib as mpl
from multiprocessing import Process

def make_linechart(data, ticks, title ='Linechart'):
    mpl.rcParams['toolbar'] = 'None'
    fig = plt.figure()
    fig.canvas.set_window_title(title) 
    n = len(data)
    x = range(n)
    plt.plot(x, data)
    plt.xticks(x, [str(t) for t in ticks])
    plt.show()
    pass

def make_barchart(data, ticks, title="Barchart"):
    mpl.rcParams['toolbar'] = 'None'
    fig = plt.figure()
    fig.canvas.set_window_title(title) 
    n = len(data)
    x = range(n)
    plt.bar(x, data, 1)
    plt.xticks([i+0.5 for i in x], [str(t) for t in ticks])
    plt.show()

def make_piechart(data, labels, title="Piechart"):
    print 'make_piechart'
    mpl.rcParams['toolbar'] = 'None'
    fig = plt.figure(figsize=(6,6))
    fig.canvas.set_window_title(title) 
    plt.pie(data,labels=labels)
    plt.show()

def make_chart(style='line', args=()):
    target_func = None
    if style == 'line':
        target_func = make_linechart
    elif style == 'bar':
        target_func = make_barchart
    elif style == 'pie':
        target_func = make_piechart

    p = Process(target=target_func, args=args)
    print target_func
    p.start()
    # p.join()