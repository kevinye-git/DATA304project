""" draw from an empirical distribution, uses the inverse
    transformation method and linear interpolation"""

import numpy as np
import random
#import scipy
import pylab


def draw_empirical(data, r):
    """one draw (for given r ~ U(0,1)) from the
    empirical cdf based on data"""

    d = {x: data.count(x) for x in data}
    obs_values, freq = zip(*sorted(zip(d.keys(), d.values())))
    obs_values = list(obs_values)
    freq = list(freq)
    empf = [x*1.0/len(data) for x in freq]
    ecum = np.cumsum(empf).tolist()
    ecum.insert(0, 0)
    obs_values.insert(0, 0)

    for x in ecum:
        if r <= x:
            rpt = x
            break
    r_end = ecum.index(rpt)
    y = obs_values[r_end] - 1.0*(ecum[r_end]-r)*(obs_values[r_end] -
                                                 obs_values[r_end-1])/(ecum[r_end]-ecum[r_end-1])
    return y


# Experiment ---------
if __name__ == "__main__":

    data = [1, 2, 2, 2, 6, 2, 5, 9, 4, 4]
    r = random.random()

    print(r)
    print(draw_empirical(data, r))

##ys = scipy.rand(10000)
##xs = [draw_empirical(data, a) for a in ys]
# pylab.scatter(xs,ys)
# pylab.show()
