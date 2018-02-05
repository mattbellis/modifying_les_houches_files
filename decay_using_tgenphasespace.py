import ROOT
import numpy as np
from numpy import sin,cos,arccos,sqrt

################################################################################
def decay_particle(parent_p4, child_masses, max_weight=0):

    event = ROOT.TGenPhaseSpace()

    e = parent_p4[0]
    px = parent_p4[1]
    py = parent_p4[2]
    pz = parent_p4[3]

    parent_mass = np.sqrt(e*e - (px*px + py*py + pz*pz))

    parent_TLV = ROOT.TLorentzVector( px, py, pz, parent_mass )

    weight = -1e9
    children = None
    if event.SetDecay(parent_TLV, len(child_masses), child_masses, ""):

        weight = event.Generate()

        if max_weight*np.random.random() < weight:

            children = []
            for n in range(len(child_masses)):

                child = event.GetDecay(n)

                children.append([child.E(), child.X(), child.Y(), child.Z()])

    return weight, children
################################################################################

################################################################################
def get_max_weight(parent_p4, child_masses):
    max_weight = 0.0
    return max_weight
################################################################################

if __name__=="__main__":

    child_masses = np.array([5.0, 83])

    max_weight = 0.0
    # Get max weight
    for i in range(10000):
        pmag = 100*np.random.random()
        costh = 2*np.random.random() - 1.0
        #print str(pmag) + " " + str(costh)
        x = sin(arccos(costh))*pmag
        y = 0.0
        z = costh*pmag
        mass = 173
        e = np.sqrt(mass*mass + x*x + y*y + z*z)
        parent_p4 = [e,x,y,z]

        weight,children = decay_particle(parent_p4, child_masses, max_weight=0)
        #print(weight)
        if weight>max_weight:
            max_weight = weight
            print(max_weight)


    for i in range(100):
        pmag = 100*np.random.random()
        costh = 2*np.random.random() - 1.0
        #print str(pmag) + " " + str(costh)
        x = sin(arccos(costh))*pmag
        y = 0.0
        z = costh*pmag
        mass = 173
        e = np.sqrt(mass*mass + x*x + y*y + z*z)
        parent_p4 = [e,x,y,z]

        weight,children = decay_particle(parent_p4, child_masses, max_weight=max_weight)
        print(children)








