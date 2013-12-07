from __future__ import print_function

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import matplotlib.cbook as cbook
import matplotlib.ticker as ticker

from plot_graph import *
import datetime

class BarGraph(PlotGraph):
    def plot(self, values, narray, name):
        N = len(values)

        ind = np.arange(N)  # the x locations for the groups
        width = 0.05       # the width of the bars

        fig, ax = plt.subplots()
        rects1 = ax.bar(ind, tuple(values), width, color='r')

# add some
        ax.set_ylabel('Occurance')
        ax.set_title(('Frequence of %s in given tweet collection')%name)
        ax.set_xticks(ind+width)
        ax.set_xticklabels( tuple(narray) )

        #ax.legend( (rects1[0], rects2[0]), ('Men', 'Women') )

        def autolabel(rects):
            # attach some text labels
            for rect in rects:
                height = rect.get_height()
                ax.text(rect.get_x()+rect.get_width()/2., 1.05*height, '%d'%int(height),
                        ha='center', va='bottom')

        autolabel(rects1)
        plt.show()