import numpy as np
import matplotlib.pylab as plt
import pylhef

import sys

lhefile = pylhef.read(sys.argv[1])

pts = []

for event in lhefile.events:
    particles = event.particles

    for particle in particles:
        if particle.id == 6:
            p = particle.p
            pt = np.sqrt(p[1]*p[1] + p[2]*p[2])
            pts.append(pt)


plt.figure()
plt.hist(pts,bins=50)
plt.show()
