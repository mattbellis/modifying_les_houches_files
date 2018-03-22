import sys
import mod_lhe_tools as mlt
import pylhef
from decay_using_tgenphasespace import decay_particle
import numpy as np

infilename = sys.argv[1]

meta = []
tmpinfile = open(infilename,'r')
save_line = False
output = ""
for line in tmpinfile:
    if '<mgrwt>' in line:
        output = ""
        save_line = True
    elif '</mgrwt>' in line:
        output += line
        save_line = False
        meta.append(output)
        output = ""

    if save_line:
        output += line






outfilename = "testout.lhe"

header = mlt.get_header(infilename)
footer = '</LesHouchesEvents>'

print(header)
print(footer)

outfile = open(outfilename,"w")
outfile.write(header)

lhfile = pylhef.read(infilename)

output = ""
for mginfo,event in zip(meta,lhfile.events):
    #print("------------")
    output = "<event>\n"

    #print(event.nup,event.process_id,event.weight,event.scale,event.alpha_qcd,event.alpha_qed)
    #output += "%+.10e " % (evnent.nup)
    output += "%-7d " % (6)
    output += "%d " % (event.process_id)
    output += "%+.7e " % (event.weight)
    output += "%.8e " % (event.scale)
    output += "%.8e " % (event.alpha_qcd)
    output += "%.8e\n" % (event.alpha_qed)

    particles = event.particles

    new_children = []

    for ipart,particle in enumerate(particles):

        if particle.id != 6:
            output += mlt.write_particle(particle)
            #print(output)

        elif particle.id == 6: # top quark

            particle.status = 2 # BECAUSE IT DECAYED IN LHE IS THIS TRUE???

            output += mlt.write_particle(particle,status=2)
            #print(output)

            energy = particle.p[0]
            px = particle.p[1]
            py = particle.p[2]
            pz = particle.p[3]

            # b-quark and W boson
            #print(energy,px,py,pz)
            #print(mlt.invmass(energy,px,py,pz))
            child_masses = np.array([4.7,80.419002])
            #child_masses = np.array([4.7,2.419002])

            #w = -1
            #while w<0:
            w,children = decay_particle([energy,px,py,pz],child_masses)
            #print(w)
            #print(children)

            for i,child in enumerate(children):
                raw_particle = []
                if i==0:
                    raw_particle.append(5) # b
                else:
                    raw_particle.append(24) # W+

                raw_particle.append(1) # Status
                raw_particle.append(ipart) # First mother
                raw_particle.append(ipart) # Second mother
                if i==0: # b
                    raw_particle.append(particle.color[0]) # Color # NOT CORRECT RIGHT NOW
                    raw_particle.append(particle.color[1]) # Color # NOT CORRECT RIGHT NOW
                else: # W
                    raw_particle.append(0) # Color # NOT CORRECT RIGHT NOW
                    raw_particle.append(0) # Color # NOT CORRECT RIGHT NOW

                raw_particle.append(child[1]) # 
                raw_particle.append(child[2]) # 
                raw_particle.append(child[3]) # 
                raw_particle.append(child[0]) # 
                raw_particle.append(mlt.invmass(child[0],child[1],child[2],child[3])) # 
                raw_particle.append(0.0) # Lifetime
                raw_particle.append(-1) # SpinUp # NOT CORRECT RIGHT NOW LOOK AT PYLHEF

                p = pylhef.Particle(raw_particle)

                new_children.append([p,ipart+1])


    for nc in new_children:
        p = nc[0]
        ipart = nc[1]
        output += mlt.write_particle(p,parent_index=ipart)
        #print(output)

    output += mginfo
    output += "</event>\n"
    print(output)
    outfile.write(output)


outfile.write(footer)
outfile.write("\n")
outfile.close()


