import numpy as np
import pylhef
import sys

def invmass(e,px,py,pz):

    m2 = e*e - (px*px + py*py + pz*pz)
    if m2>=0:
        return np.sqrt(m2)
    else:
        return -np.sqrt(-m2)


def get_header(infilename):

    infile = open(infilename, "r")

    header = ""

    for line in infile:

        header += line

        if line.find("</init>")>=0:
            break

    return header


# Write particle out
def write_particle(p,status=None,parent_index=None):
    
    output = ""
    output += "%9d " % (p.id)
    if status==None:
        output += "%2d " % (p.status)
    else:
        output += "%2d " % (status)

    if parent_index==None:
        output += "%4s " % (1) # Parent index
        output += "%4s " % (2) # Parent index
    else:
        output += "%4s " % (parent_index) # Parent index
        output += "%4s " % (parent_index) # Parent index

    output += "%4s " % (p.color[0]) # Color
    output += "%4s " % (p.color[1]) # Color
    output += "%+.10e " % (p.p[1])
    output += "%+.10e " % (p.p[2])
    output += "%+.10e " % (p.p[3])
    output += "%.10e  " % (p.p[0])
    output += "%.10e " % (p.mass)
    output += "%.4e " % (p.lifetime)
    output += "%.4e\n" % (p.spin)
    # Assumes pylhe particle
    #simpart = [s_pid,s_inout,s_fmom,s_lmom,s_col1,s_col2,s_px,s_py,s_pz,s_energy,s_mas,s_lt,s_spi] 
    #string = "%9d %2d %4s %4s %4s %4s %3s %3s %3s %3s  %3s %3s %3s\n" % (int(ev[0]),int(ev[1]),ev[2],ev[3],ev[4],ev[5],ev[6],ev[7],ev[8],ev[9],ev[10],ev[11],ev[12])

    return output

