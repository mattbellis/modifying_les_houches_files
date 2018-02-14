import numpy as np
import pylhef
import sys
from decimal import Decimal

from decay_using_tgenphasespace import decay_particle

################################################################################
# Get max weights
################################################################################
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
################################################################################



################################################################################
# Read in the data file
################################################################################
lhfile = pylhef.read(sys.argv[1])

sim_events = []
eventlength = []
tqlist=[]

for event in lhfile.events:       # iterates through all events, modifies existing charactersistics of top quark
    
    tq = 0
    particles=event.particles      #finds the index of the top quark
    eventlength.append(len(particles))
    for particle in particles:
        if particle.id == 6:
            tqlist.append(tq)
            break
        else:
            tq += 1
    
   # defines values for each entry in simulated event
    part = event.particles[tq] 
    pid = part.id
    inout = 1
    fmom = tq+1
    lmom = tq+1
    col1 = part.color[0]
    col2 = part.color[1]
    px = part.p[1]/2
    py = part.p[2]/2
    pz = part.p[3]/2
    energy = part.p[0]/2
    mas = part.mass
    lt = part.lifetime
    spi = part.spin
                      
    # converts all inputs to strings, converts relevant items to scientific notation
    s_part = str(part)
    s_pid = str(pid)
    s_inout = str(inout)
    s_fmom = str(fmom)
    s_lmom = str(lmom)
    s_col1 = str(col1)
    s_col2 = str(col2)
    s_px = '%.10e' % Decimal(px)
    s_py = '%.10e' % Decimal(py)
    s_pz = '%.10e' % Decimal(pz)
    s_energy = '%.10e' % Decimal(energy)
    s_mas = '%.10e' % Decimal(mas) 
    s_lt = '%.4e' % Decimal(lt)
    s_spi = '%.4e' % Decimal(spi)    
    
    simpart = [s_pid,s_inout,s_fmom,s_lmom,s_col1,s_col2,s_px,s_py,s_pz,s_energy,s_mas,s_lt,s_spi]        
    sim_events.append(simpart)                      # writes simulated particle to entry in list


sim_events[0]     
sim_events_str = []
for n in range(len(sim_events)):
    #string = ' '.join(str(e) for e in sim_events[n]),'\n'
    ev = sim_events[n]
    string = "%9d %2d %4s %4s %4s %4s %3s %3s %3s %3s  %3s %3s %3s\n" % (int(ev[0]),int(ev[1]),ev[2],ev[3],ev[4],ev[5],ev[6],ev[7],ev[8],ev[9],ev[10],ev[11],ev[12])
    
    sim_events_str.append(string)

test=open('test_events.lhe','r')
file=[]

output = ""
for line in test:
    file.append(line)

# finds line number in original lhe file where each event starts
lines=[i for i,x in enumerate(file) if x=='<event>\n']
len(lines) # = 94

toplist=[]
for u in range(len(lines)):
    top = lines[u]+2+tqlist[u]
    topparticle = file[top]
    topparticle = topparticle.replace(" 6  1 "," 6  2 ")
    toplist.append(topparticle)
    
    
sims=[]
n=0
while n<=len(lines):
    if n==0:                               # writes header up to first event as first entry in list sims
        place = lines[n]+2+eventlength[n]    ## writes first event and first simulated particle to list
        topplace = lines[n]+2+tqlist[n]
        sims.append(file[0:topplace])
        sims.append(toplist[n])
        sims.append(file[topplace+1:place])
        sims.append(sim_events_str[n])
    elif n < len(lines):                  # writes each event and respective simulated particle to list
        place = lines[n]+2+eventlength[n]
        topplace = lines[n]+2+tqlist[n]
        last = lines[n-1]+2+eventlength[n-1]
        sims.append(file[last:topplace])
        sims.append(toplist[n])
        sims.append(file[topplace+1:place])
        sims.append(sim_events_str[n])
    else:                                      # writes last few lines of last event to list
        last = lines[n-1]+2+eventlength[n-1]
        sims.append(file[last:len(file)-1])
    n=n+1
    
head = sims[0][0:-6]               # establishes header
foot = '</LesHouchesEvents>'       # establishes footer

# prepares header and footer in proper form
header = ('').join(head)
e1 = ('').join(sims[0][-6:last])

# writes strings to new file
f = open('simulated_event.lhe', 'w')
f.write(header)
f.write(e1)

for n in range(1,len(sims)):       # iterates entries of sims (excluding header/footer), writes the strings to file
    fix = ('').join(sims[n])
    f.write(fix)

f.write(foot)

f.close()

