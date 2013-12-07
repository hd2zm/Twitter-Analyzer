from __future__ import print_function

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import matplotlib.cbook as cbook
import matplotlib.ticker as ticker
import datetime

#datafile = cbook.get_sample_data('aapl.csv', asfileobj=False)
#print ('loading %s' % datafile)
#r = mlab.csv2rec(datafile)

date = [2013-12-01,2013-12-02,2013-12-03,2013-12-04,2013-12-06]
date.sort()
val = [1,3,4,6,7]
#r = r[-30:]  # get the last 30 days


# first we'll do it the default way, with gaps on weekends
fig, ax = plt.subplots()
ax.plot(date, val, 'o-')
fig.autofmt_xdate()

# next we'll write a custom formatter
N = len(date)
ind = np.arange(N)  # the evenly spaced plot indices

def format_date(x, pos=None):
    thisind = np.clip(int(x+0.5), 0, N-1)
    #year,month,day = str(date[thisind]).split('-')
    return date[thisind]
    #return (datetime.date(int(year), int(month), int(day))).strftime('%Y-%m-%d')

fig, ax = plt.subplots()
ax.plot(ind, val, 'o-')
ax.xaxis.set_major_formatter(ticker.FuncFormatter(format_date))
fig.autofmt_xdate()

plt.show()