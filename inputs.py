#! python

########################################
### Input parameters for ORIGEN sims ###
########################################

NUM_CYCLES = 21
COOLING_INTERVALS = (0.000694, 7, 30, 365.25, 2292) #1 min, 1 week, 1 month, 1 year, 8 years in days

# average power
PWR_PWR = 30.0
BWR_PWR = 20.0
PHWR_PWR = 20.0

# enrichments %U235
LWR_ENR = (1.5, 3.0, 4.0, 5.0)
PHWR_ENR = (0.711,)
VVER_ENR = (2.4, 3.6, 3.82, 4.25, 4.38)

# moderator densities g/cc
LWR_MOD = 0.72
PHWR_MOD = 0.84

# burnup constants MW/MTU
# init burnup and burn steps:
LWR_BURN = 3000.0
PHWR_BURN = 500.0 

# reactors + arp lib files (enr-based)
# order of each list element must correspond to the libs

# ORIGEN reactor types + general types
o_rxtrs = ('ce14x14', 'ce16x16', 'w14x14', 'w15x15', 'w17x17', 
           's14x14', 's18x18', 'bw15x15', 'vver440', 'vver1000', 
           'ge7x7-0', 'ge8x8-1', 'ge9x9-2', 'ge10x10-8', 'abb8x8-1', 
           'atrium9x9-9', 'atrium10x10-9', 'svea64-1', 'svea100-0', 
           'candu19', 'candu28', 'candu37'
           )

rxtr_types = ('pwr',)*10 + ('bwr',)*9 + ('phwr',)*3

# Corresponding ARP libs by enrichment
all_arps = (('ce14_e15', 'ce14_e30', 'ce14_e40', 'ce14_e50'), 
            ('ce16_e15', 'ce16_e30', 'ce16_e40', 'ce16_e50'), 
            ('w14_e15', 'w14_e30', 'w14_e40', 'w14_e50'), 
            ('w15_e15', 'w15_e30', 'w15_e40', 'w15_e50'), 
            ('w17_e15', 'w17_e30', 'w17_e40', 'w17_e50'), 
            ('s14_e15', 's14_e30', 's14_e40', 's14_e50'), 
            ('s18_e15', 's18_e30', 's18_e40', 's18_e50'), 
            ('bw15_e15', 'bw15_e30', 'bw15_e40', 'bw15_e50'), 
            ('vver440_e24', 'vver440_e36', 'vver440_rad_e38', 'vver440_rad_e42', 'vver440_rad_e43'),
            ('vver1000_e15', 'vver1000_e30', 'vver1000_e40', 'vver1000_e50'), 
            ('ge7_e15w07', 'ge7_e30w07', 'ge7_e40w07', 'ge7_e50w07'),
            ('ge8_e15w07', 'ge8_e30w07', 'ge8_e40w07', 'ge8_e50w07'), 
            ('ge9_e15w07', 'ge9_e30w07', 'ge9_e40w07', 'ge9_e50w07'), 
            ('ge10_e15w07', 'ge10_e30w07', 'ge10_e40w07', 'ge10_e50w07'), 
            ('abb_e15w07', 'abb_e30w07', 'abb_e40w07', 'abb_e50w07'), 
            ('a9_e15w07', 'a9_e30w07', 'a9_e40w07', 'a9_e50w07'), 
            ('a10_e15w07', 'a10_e30w07', 'a10_e40w07', 'a10_e50w07'), 
            ('svea64_e15w07', 'svea64_e30w07', 'svea64_e40w07', 'svea64_e50w07'), 
            ('svea100_e15w07', 'svea100_e30w07', 'svea100_e40w07', 'svea100_e50w07'), 
            ('candu19_e07',), 
            ('candu28_e07',), 
            ('candu37_e07',)
            )
