import sys
import mod_lhe_tools as mlt
import pylhef
from decay_using_tgenphasespace import decay_particle
import numpy as np
import ROOT

infilename = sys.argv[1]

split_by_Nevents = 10


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

################################################################################



header = mlt.get_header(infilename)
footer = '</LesHouchesEvents>'

#print(header)
#print(footer)

still_writing = True

begin_events = 0
end_events = begin_events + split_by_Nevents

ev_count = 0

lhfile = pylhef.read(infilename)

for mginfo,event in zip(meta,lhfile.events):

    file_not_closed = True

    if ev_count == 0:
        outfilename = "{0}_{1:d}_{2:d}.lhe".format(infilename.split('.lhe')[0],begin_events, end_events-1)
        print(outfilename)
        outfile = open(outfilename,"w")
        outfile.write(header)

    #print("------------")
    output = "<event>\n"

    #print(event.nup,event.process_id,event.weight,event.scale,event.alpha_qcd,event.alpha_qed)
    #output += "%+.10e " % (evnent.nup)
    output += "%-7d " % (6) # Number of particles
    #output += "%-7d " % (7) # Number of particles 
    output += "%d " % (event.process_id)
    output += "%+.7e " % (event.weight)
    output += "%.8e " % (event.scale)
    output += "%.8e " % (event.alpha_qcd)
    output += "%.8e\n" % (event.alpha_qed)

    particles = event.particles

    new_children = []

    for ipart,particle in enumerate(particles):

        output += mlt.write_particle(particle)

    output += mginfo
    output += "</event>\n"
    #print(output)
    outfile.write(output)

    ev_count += 1

    if ev_count>=split_by_Nevents:
        ev_count = 0
        begin_events = end_events
        end_events = begin_events + split_by_Nevents

        outfile.write(footer)
        outfile.write("\n")
        outfile.close()

        file_not_closed = False


if file_not_closed:
    outfile.write(footer)
    outfile.write("\n")
    outfile.close()

