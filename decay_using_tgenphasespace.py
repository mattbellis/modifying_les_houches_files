import ROOT
import numpy as np
from numpy import sin,cos,arccos,sqrt
import time

################################################################################
def decay_particle(parent_p4, child_masses, max_weight=0, child_widths=None, rnd = None):

    if rnd == None:
        rnd = ROOT.TRandom(int(1000000*time.time()))

    event = ROOT.TGenPhaseSpace()

    e = parent_p4[0]
    px = parent_p4[1]
    py = parent_p4[2]
    pz = parent_p4[3]

    #parent_mass = np.sqrt(e*e - (px*px + py*py + pz*pz))

    parent_TLV = ROOT.TLorentzVector( px, py, pz, e )

    weight = -1e9
    children = None

    masses_to_use = []
    if child_widths is None:
        masses_to_use = list(child_masses)
    else:
        for m,w in zip(child_masses,child_widths):
            mass = 1e9
            if w is None or w==0:
                masses_to_use.append(m)
            else:
                #print("diff: ",parent_TLV.M()-sum(masses_to_use))
                while mass > (parent_TLV.M()-sum(masses_to_use)) or mass<0: 
                    mass = rnd.BreitWigner(m,w)
                    #print('mass: ',mass)
                masses_to_use.append(mass)

    masses_to_use = np.array(masses_to_use)
    #print(masses_to_use)
    if event.SetDecay(parent_TLV, len(masses_to_use), masses_to_use, ""):

        wmax = event.GetWtMax()
        #print("wtmax: ",wmax)

        weight = -1 # Do this while loop to avoid negative weights

        while weight<0:

            weight = event.Generate()
            #print("HERE: ",weight)

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








