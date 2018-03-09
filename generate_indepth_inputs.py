#! /usr/bin/env python3

from training_set import *

class ConstParams(object):
    def __init__(self, avg_power, enrich, num_enrich, num_cycles, mod_density, burn_step, init_burn, cooling_ints):
        self.avg_power = avg_power
        self.enrich = enrich
        self.num_enrich = num_enrich
        self.num_cycles = num_cycles
        self.mod_density = mod_density
        self.burn_step = burn_step
        self.init_burn = init_burn
        self.cooling_ints = cooling_ints

class CalcParams(object):
    def __init__(self, burnup, cycle_time, cycle_avg_power, cooling_times, xsec_cycle, rad_time):
        self.burnup = burnup
        self.cycle_time = cycle_time
        self.cycle_avg_power = cycle_avg_power
        self.cooling_times = cooling_times
        self.xsec_cycle = xsec_cycle
        self.rad_time = rad_time

class RxtrFiles(object):
    def __init__(self, lib_type, arp_libs, out_lib, inp_file):
        self.lib_type = lib_type
        self.arp_libs = arp_libs #list of reactor+enrichment library
        self.out_lib = out_lib
        self.inp_file = inp_file

def addto_arpdata(c, p, s):
    with open('arpdata.txt', 'a') as arp:
        arp.write('!' + s.lib_type + '\n')                           # config-name
        arp.write(str(c.num_enrich) +' 1 '+ str(c.num_cycles) +'\n') # nums: enrich, mod_dens, burn_steps
        arp.writelines('%s ' % i for i in c.enrich)                  # list enrichments
        arp.write('\n' + str(c.mod_density) + '\n')                  # list moderator densities (1 here)
        arp.writelines("'%s' " % i for i in s.arp_libs)              # list ORIGEN-ARP files for each enr/mod_dens combo
        arp.write('\n\t')
        arp.writelines('%s ' % i for i in p.burnup)                  # list burnup values
        arp.write('\n\n')
    return

def generate_inpfile(c, p, s):
    with open(s.inp_file, 'w') as inp:
        for enr in c.enrich:
            out_lib = str(s.out_lib[:-4] + '_enr' + str(enr) + '.f33')
            enr_file = out_lib[:-4]
            save_file = enr_file + '.f71'
            #ARP section
            inp.write('=arp\n')
            inp.write(s.lib_type + '\n')
            inp.write(str(enr) + '\n')
            inp.write(str(c.num_cycles) + '\n')
            inp.writelines('%s\n' % i for i in p.cycle_time)
            inp.writelines('%s\n' % i for i in p.cycle_avg_power)
            inp.writelines('%s\n' % i for i in p.xsec_cycle)
            inp.write(str(c.mod_density) + '\n')
            ino.write(out_lib + '\n') 
            inp.write('end\n')
            #ORIGEN section
            inp.write('=origen\n')
            inp.write('bounds{gamma=[100L 1.0e7 1.0e-5]}\n')
            for n in range(0, c.num_cycles):
                if n == 0:
                    inp.write('case(i' + str(n+1) + ') {\n')
                    inp.write('lib {file="' + out_lib + '" pos=1}\n')
                    inp.write('title = "' + enr_file + ', 1 MTU: IRRAD+DECAY ' + str(n+1) + '"\n')
                    inp.write('mat {units=GRAMS iso=[u234=356 u235=28000 u236=184 u238=971460]}\n')    
                else:
                    inp.write('}\n')
                    inp.write('case(i' + str(n+1) + ') {\n')
                    inp.write('title = "' + enr_file + ', 1 MTU: IRRAD+DECAY ' + str(n+1) + '"\n')
                    inp.write('mat {previous=1}\n')
                # weak point: presumes 5 cooling times
                inp.write('time = [' + str(p.rad_time[n]) + ' ' + 
                          str(p.cooling_times[n][0]) + ' ' + 
                          str(p.cooling_times[n][1]) + ' ' + 
                          str(p.cooling_times[n][2]) + ' ' + 
                          str(p.cooling_times[n][3]) + ' ' + 
                          str(p.cooling_times[n][4]) + ']\n')
                inp.write('power = [' + str(c.avg_power) + ' 0 0 0 0 0' + ']\n')
                inp.write('gamma = yes\n')
                # save block for binary output file
                inp.write('save{file="'+ save_file + '"}\n')
            inp.write('}\n' + 'end\n')
            #OPUS section
            ###nuclide conc###
            inp.write('=opus\n')
            inp.write('library="' + out_lib + '"\n')
            inp.write('data="' + save_file + '"\n')
            inp.write('typarams=nuclides\n')
            inp.write('libtype=act\n')
            inp.write('title="' + enr_file + ' SNF nuclide concentrations" \nend\n')
            ###gamma spec###
            inp.write('=opus\n')
            inp.write('library="' + out_lib + '"\n')
            inp.write('data="' + save_file + '"\n')
            inp.write('typarams=gspectrum\n')
            inp.write('libtype=act\n')
            inp.write('title="' + enr_file + ' SNF gamma spectra" \nend\n')
    return

def get_params(c):
    p = CalcParams([], [], [], [], [], [])
    p.burnup = []
    for i in range(0, c.num_cycles):
        if i == 0: 
            p.burnup.append(c.init_burn)
        else:
            p.burnup.append(float(p.burnup[i-1]+c.burn_step))
        p.rad_time.append(p.burnup[i]/c.avg_power)
        if i == 0:
            p.cycle_time.append(p.rad_time[i] - 0)
        else:
            p.cycle_time.append(p.rad_time[i] - p.rad_time[i-1])
        row = []
        for d in c.cooling_ints:
            row.append(d + p.rad_time[i])
        p.cooling_times.append(row)
        p.cycle_avg_power.append(c.avg_power)
        p.xsec_cycle.append(1)
    return p

def get_pwr_data():
    c = ConstParams(avg_power = PWR_PWR, enrich = LWR_ENR, 
                    num_enrich = len(LWR_ENR), num_cycles = NUM_CYCLES, 
                    mod_density = LWR_MOD, burn_step = LWR_BURN, 
                    init_burn = LWR_BURN, cooling_ints = COOLING_INTERVALS)
    return c

def get_bwr_data():
    c = ConstParams(avg_power = BWR_PWR, enrich = LWR_ENR, 
                    num_enrich = len(LWR_ENR), num_cycles = NUM_CYCLES, 
                    mod_density = LWR_MOD, burn_step = LWR_BURN, 
                    init_burn = LWR_BURN, cooling_ints = COOLING_INTERVALS)
    return c

def get_phwr_data():
    c = ConstParams(avg_power = PHWR_PWR, enrich = PHWR_ENR, 
                    num_enrich = len(PHWR_ENR), num_cycles = NUM_CYCLES, 
                    mod_density = PHWR_MOD, burn_step = PHWR_BURN,
                    init_burn = PHWR_BURN, cooling_ints = COOLING_INTERVALS)
    return c

def main():
    print('Generating Inputs\n')
    for i in range(0, len(O_RXTRS)):
        r = RXTR_TYPES[i]
        # c is the class of 'constants'
        if r == 'pwr':
            c = get_pwr_data()
            if 'vver440' in O_RXTRS[i]:
                c.enrich = VVER_ENR
                c.num_enrich = len(VVER_ENR)
        elif r == 'bwr':
            c = get_bwr_data()
        else:
            c = get_phwr_data()
        # p is the class of inputs that require loops
        p = get_params(c)
        # s is the class of string of libs and files
        s = RxtrFiles(lib_type = O_RXTRS[i],                 
                      arp_libs = [lib + '.f33' for lib in ALL_ARPS[i]],
                      out_lib  = O_RXTRS[i] + '.f33', 
                      inp_file = O_RXTRS[i] + '.inp'
                      )
        # Make input file and add to arpdata.txt
        generate_inpfile(c, p, s)
        addto_arpdata(c, p, s)
    return

if __name__ == "__main__":
    main()
