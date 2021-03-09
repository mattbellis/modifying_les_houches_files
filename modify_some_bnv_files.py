import sys
import mod_lhe_tools as mlt
import pylhef
from decay_using_tgenphasespace import decay_particle
import numpy as np
import ROOT

infilename = sys.argv[1]
decay = sys.argv[2]
#decay = 't2mubc'
#decay = 't2mudc'
#decay = 't2mubu'
#decay = 't2mudu'
#decay = 't2ebc'
#decay = 't2edc'
#decay = 't2ebu'
#decay = 't2edu'

#decay = 'tbar2mubc'
#decay = 'tbar2mudc'
#decay = 'tbar2mubu'
#decay = 'tbar2mudu'
#decay = 'tbar2ebc'
#decay = 'tbar2edc'
#decay = 'tbar2ebu'
#decay = 'tbar2edu'

top = 6
W = 24
bfromtop = 5
lep = -13
qdown = -5
qup = -4

lep_mass = 0.10566
qdown_mass = 4.7
qup_mass = 1.42

if decay.find('eb')>=0 or decay.find('ed')>=0:
    lep = -11
    lep_mass = 0.000511

if decay.find('dc')>=0 or decay.find('du')>=0:
    qdown = -1
    qdown_mass = 0.0047

if decay.find('bu')>=0 or decay.find('du')>=0:
    qup = -2
    qup_mass = 0.0022


if decay.find('tbar')>=0:
    top *= -1
    W *= -1
    bfromtop *= -1
    lep *= -1
    qup *= -1
    qdown *= -1

print("Going to decay {0} --> {1} {2} {3}".format(top,lep,qdown,qup))
#exit()

# GET ALL THE REWEIGHTING INFO
meta = []
tmpinfile = open(infilename,'r')
save_line = False
output = ""
for line in tmpinfile:
    #if '<mgrwt>' in line:
    if '<scales ' in line:
        output = ""
        save_line = True
    #elif '</mgrwt>' in line:
    elif '</rwgt>' in line:
        output += line
        save_line = False
        meta.append(output)
        output = ""

    if save_line:
        output += line

rnd = ROOT.TRandom()

#outfilename = "bnv_ttbar_t2mubc.lhe"
#outfilename = "bnv_ttbar_tbar2bjj_t2mubc.lhe"
#outfilename = "bnv_ttbar_tbar2bmunu_t2mubc.lhe"
#outfilename = "bnv_ttbar_tbar2blnu_t2mubc.lhe"
#outfilename = infilename.split('/')[-1].split('.lhe')[0] + '_' + decay + '.lhe'
#outfilename = infilename.split('/')[-4].split('PROC_')[1] + '_BNV_PS_' + decay + '.lhe'
outfilename = infilename.split('.lhe')[0] + '_BNV_PS_' + decay + '.lhe'

for n in range(0,50):
    ntag = '_{0:02d}'.format(n)
    outfilename = outfilename.replace(ntag,'')
print(outfilename)
#exit()

header = mlt.get_header(infilename)
print(header)

footer = '</LesHouchesEvents>'

print(header)
print(footer)
#exit()

outfile = open(outfilename,"w")
outfile.write(header)

lhfile = pylhef.read(infilename)

output = ""
for mginfo,event in zip(meta,lhfile.events):
    #print("------------")
    output = "<event>\n"

    #print(event.nup,event.process_id,event.weight,event.scale,event.alpha_qcd,event.alpha_qed)
    #output += "%+.10e " % (evnent.nup)
    #output += "%-7d " % (6)
    #output += "%-7d " % (7) # Number of particles  # This is for just the ttbar
    output += "%-7d " % (11) # Number of particles  # This is for just the ttbar, tbar--> b j j 
    output += "%d " % (event.process_id)
    output += "%+.7e " % (event.weight)
    output += "%.8e " % (event.scale)
    output += "%.8e " % (event.alpha_qcd)
    output += "%.8e\n" % (event.alpha_qed)

    particles = event.particles

    topBNV_index = None
    WBNV_index = None
    topSM_index = None
    WSM_index = None
    helicities = []

    topSM = None
    WSM = None
    bSM = None
    WchildrenSM = []

    topBNV = None
    WBNV = None
    bBNV = None
    WchildrenBNV = []

    for ipart,particle in enumerate(particles):

        # Write out the initial state particles
        if particle.status == -1:
            output += mlt.write_particle(particle)
            #print(output)

        ####### BNV #######################################
        elif particle.id == top: # top quark
            topBNV = particle
            topBNV_index = ipart+1
            continue

        elif particle.id == W and particle.first_mother==topBNV_index: # W boson from the top we want to remove
            WBNV_index = ipart+1
            WBNV = particle
            continue

        elif particle.id == bfromtop and particle.first_mother==topBNV_index: # b quark from the top we want to remove
            helicities.append(particle.spin)
            bBNV = particle
            continue

        elif particle.first_mother==WBNV_index: # Decay products from W from top, we can remove these
            helicities.append(particle.spin)
            WchildrenBNV.append(particle)
            continue

        ######## SM #######################################
        elif particle.id == -top: # top quark
            topSM = particle
            topSM_index = ipart+1
            continue

        elif particle.id == -W and particle.first_mother==topSM_index: # W boson from the top we want to remove
            WSM_index = ipart+1
            WSM = particle
            continue

        elif particle.id == -bfromtop and particle.first_mother==topSM_index: # b quark from the top we want to remove
            bSM = particle
            continue

        elif particle.first_mother==WSM_index: # Decay products from W from top, we can remove these
            WchildrenSM.append(particle)
            continue

    ############################################################################
    #### Write out the other particles
    ############################################################################
    output += mlt.write_particle(topSM) # 3
    output += mlt.write_particle(topBNV) # 4
    output += mlt.write_particle(WSM,parent_index=3) # 5
    output += mlt.write_particle(bSM,parent_index=3) # 6
    output += mlt.write_particle(WchildrenSM[0],parent_index=5) # 7
    output += mlt.write_particle(WchildrenSM[1],parent_index=5) # 8

    # Decay the top to the BNV children
    particle = topBNV
    #particle.status = 2 # BECAUSE IT DECAYED IN LHE
    child_colors = [0, 0]
    if particle.color[0]==501:
        child_colors = [502,503]
    elif particle.color[0]==502:
        child_colors = [501,503]
    elif particle.color[0]==503:
        child_colors = [501,502]
    elif particle.color[0]==504:
        child_colors = [502,503]
    elif particle.color[0]==505:
        child_colors = [503,504]
    else:
        child_colors = [504,505]

    #output += mlt.write_particle(particle,status=2)
    #print(output)

    energy = particle.p[0]
    px = particle.p[1]
    py = particle.p[2]
    pz = particle.p[3]

    # muon, b-quark, and s-quark
    #print(energy,px,py,pz)
    #print(mlt.invmass(energy,px,py,pz))
    #child_masses = np.array([0.105,4.7,1.42])
    child_masses = np.array([lep_mass, qdown_mass, qup_mass])
    child_widths = np.array([0,0,0])

    #w = -1
    #while w<0:
    w,children = decay_particle([energy,px,py,pz],child_masses,child_widths=child_widths,rnd=rnd)
    #print(w)
    #print(children)

    new_children = []

    #print(children)
    for i,child in enumerate(children):
        raw_particle = []
        if i==0:
            #raw_particle.append(-13) # mu+
            raw_particle.append(lep) # 
            raw_particle.append(1) # Status
        elif i==1:
            #raw_particle.append(-5) # anti-b
            raw_particle.append(qdown) # 
            raw_particle.append(1) # Status
        else:
            #raw_particle.append(-4) # anti-charm
            raw_particle.append(qup) #
            raw_particle.append(1) # Status

        raw_particle.append(ipart) # First mother
        raw_particle.append(ipart) # Second mother
        if i==0: # mu
            raw_particle.append(0) # Color 
            raw_particle.append(0) # Color 
        elif i==1: # b
            raw_particle.append(0) # Color # NOT CORRECT RIGHT NOW
            raw_particle.append(child_colors[0]) # Color # MAYBE CORRECT RIGHT NOW
        else: # s
            raw_particle.append(0) # Color # NOT CORRECT RIGHT NOW
            raw_particle.append(child_colors[1]) # Color # MAYBE CORRECT RIGHT NOW

        raw_particle.append(child[1]) # 
        raw_particle.append(child[2]) # 
        raw_particle.append(child[3]) # 
        raw_particle.append(child[0]) # 
        raw_particle.append(mlt.invmass(child[0],child[1],child[2],child[3])) # 
        raw_particle.append(0.0) # Lifetime
        raw_particle.append(helicities[i]) # Helicities

        p = pylhef.Particle(raw_particle)
        output += mlt.write_particle(p,parent_index=4)
        #print(raw_particle)
        #print(p.status)

        #new_children.append([p,ipart+1])

    '''
    for nc in new_children:
        p = nc[0]
        ipart = nc[1]
        output += mlt.write_particle(p,parent_index=ipart)
        #print(output)
    '''
    #print(helicities)

    output += mginfo
    output += "</event>\n"
    #print(output)
    outfile.write(output)


outfile.write(footer)
outfile.write("\n")
outfile.close()


