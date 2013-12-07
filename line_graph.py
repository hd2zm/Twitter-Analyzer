from __future__ import print_function

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import matplotlib.cbook as cbook
import matplotlib.ticker as ticker

from plot_graph import *
import datetime

class LineGraph(PlotGraph):
    def plot(self, date, val):
        # datafile = cbook.get_sample_data('aapl.csv', asfileobj=False
        # #print ('loading %s' % datafile)
        # #r = mlab.csv2rec(datafile)
        #r = r[-30:]  # get the last 30 days

        # first we'll do it the default way, with gaps on weekends
        '''
        fig, ax = plt.subplots()
        ax.plot(date, val, 'o-')
        fig.autofmt_xdate()
        '''
        # next we'll write a custom formatter
        N = len(date)
        ind = np.arange(N)  # the evenly spaced plot indices

        def format_date(x, pos=None):
            thisind = np.clip(int(x+0.5), 0, N-1)
            #year,month,day = str(date[thisind]).split('-')
            #return (datetime.date(int(year), int(month), int(day))).strftime('%Y-%m-%d')
            return date[thisind].strftime("%m/%d/%Y")

        fig, ax = plt.subplots()
        ax.plot(ind, val, 'o-')
        ax.xaxis.set_major_formatter(ticker.FuncFormatter(format_date))
        fig.autofmt_xdate()

        plt.show()