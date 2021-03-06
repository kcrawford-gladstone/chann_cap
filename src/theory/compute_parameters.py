import pickle
# Our numerical workhorses
import numpy as np
import pandas as pd

# Import matplotlib stuff for plotting
import matplotlib.pyplot as plt
import matplotlib.cm as cm

# Seaborn, useful for graphics
import seaborn as sns

# Import the utils for this project
import ccutils

# Define mRNA rate
# gm = 0.00284  # s**-1
# http://bionumbers.hms.harvard.edu/bionumber.aspx?id=105717&ver=3&trm=lacZ%20mRNA%20lifetime&org=
gm = 1 / (3 * 60)

# Define cell volume
Vcell = 2.15 # fL

# Define diffusion limiting rate
k0 = 2.7E-3

# =============================================================================
# Single promoter
# =============================================================================
# Load the flat-chain
with open('../../data/mcmc/lacUV5_constitutive_mRNA_prior.pkl', 'rb') as file:
    unpickler = pickle.Unpickler(file)
    gauss_flatchain = unpickler.load()
    gauss_flatlnprobability = unpickler.load()

# Generate a Pandas Data Frame with the mcmc chain
index = ['kp_on', 'kp_off', 'rm']

# Generate a data frame out of the MCMC chains
df_mcmc = pd.DataFrame(gauss_flatchain, columns=index)

# reasign the index with the new entries
index = df_mcmc.columns

# map value of the parameters
max_idx = np.argmax(gauss_flatlnprobability, axis=0)
kpon, kpoff, rm = df_mcmc.iloc[max_idx, :]

# ea range
kpon_hpd = ccutils.stats.hpd(df_mcmc.iloc[:, 0], 0.95)
kpoff_hpd = ccutils.stats.hpd(df_mcmc.iloc[:, 1], 0.95)
rm_hpd = ccutils.stats.hpd(df_mcmc.iloc[:, 2], 0.95)

# Print results
print('Single gene copy parameters: ')
print("""
The most probable parameters for the model
------------------------------------------
kp_on = {0:.1f} -{1:0.1f} +{2:0.1f}
kp_off = {3:.1f} -{4:0.1f} +{5:0.1f}
rm = {6:.1f} -{7:0.1f} +{8:0.1f}
""".format(kpon, np.abs(kpon-kpon_hpd[0]), np.abs(kpon-kpon_hpd[1]),\
           kpoff, np.abs(kpoff-kpoff_hpd[0]), np.abs(kpoff-kpoff_hpd[1]),\
           rm, np.abs(rm-rm_hpd[0]), np.abs(rm-rm_hpd[1])))



# Print results
print("""
The most probable parameters for the model in seconds^-1
--------------------------------------------------------
kp_on = {0:.3f} -{1:0.3f} +{2:0.3f} s^-1
kp_off = {3:.3f} -{4:0.3f} +{5:0.3f} s^-1
rm = {6:.3f} -{7:0.3f} +{8:0.3f} s^-1
""".format(kpon * gm, np.abs(kpon-kpon_hpd[0]) * gm,
           np.abs(kpon-kpon_hpd[1]) * gm,
           kpoff * gm, np.abs(kpoff-kpoff_hpd[0]) * gm,
           np.abs(kpoff-kpoff_hpd[1]) * gm,
           rm * gm, np.abs(rm-rm_hpd[0]) * gm, np.abs(rm-rm_hpd[1]) * gm))

# =============================================================================
# Double promoter
# =============================================================================

# Load the flat-chain
with open('../../data/mcmc/lacUV5_constitutive_mRNA_double_expo.pkl',
          'rb') as file:
    unpickler = pickle.Unpickler(file)
    gauss_flatchain = unpickler.load()
    gauss_flatlnprobability = unpickler.load()

# Generate a Pandas Data Frame with the mcmc chain
index = ['kp_on', 'kp_off', 'rm']

# Generate a data frame out of the MCMC chains
df_mcmc = pd.DataFrame(gauss_flatchain, columns=index)

# rerbsine the index with the new entries
index = df_mcmc.columns

# map value of the parameters
max_idx = np.argmax(gauss_flatlnprobability, axis=0)
kpon_double, kpoff_double, rm_double = df_mcmc.iloc[max_idx, :]

# ea range
kpon_hpd = ccutils.stats.hpd(df_mcmc.iloc[:, 0], 0.95)
kpoff_hpd = ccutils.stats.hpd(df_mcmc.iloc[:, 1], 0.95)
rm_hpd = ccutils.stats.hpd(df_mcmc.iloc[:, 2], 0.95)

# Print results
print('Two-promoter model')
print("""
The most probable parameters for the model
------------------------------------------
kp_on = {0:.1f} -{1:0.1f} +{2:0.1f}
kp_off = {3:.1f} -{4:0.1f} +{5:0.1f}
rm = {6:.1f} -{7:0.1f} +{8:0.1f}
""".format(kpon_double, np.abs(kpon_double-kpon_hpd[0]),
           np.abs(kpon_double-kpon_hpd[1]),
           kpoff_double, np.abs(kpoff_double-kpoff_hpd[0]),
           np.abs(kpoff_double-kpoff_hpd[1]),
           rm_double, np.abs(rm_double-rm_hpd[0]),
           np.abs(rm_double-rm_hpd[1])))

# Print results
print("""
The most probable parameters for the model in seconds^-1
--------------------------------------------------------
kp_on = {0:.3f} -{1:0.3f} +{2:0.3f} s^-1
kp_off = {3:.2f} -{4:0.2f} +{5:0.2f} s^-1
rm = {6:.1f} -{7:0.1f} +{8:0.1f} s^-1
""".format(kpon_double * gm, np.abs(kpon_double-kpon_hpd[0]) * gm,
           np.abs(kpon_double-kpon_hpd[1]) * gm,
           kpoff_double * gm, np.abs(kpoff_double-kpoff_hpd[0]) * gm,
           np.abs(kpoff_double-kpoff_hpd[1]) * gm,
           rm_double * gm, np.abs(rm_double-rm_hpd[0]) * gm,
           np.abs(rm_double-rm_hpd[1]) * gm))


# =============================================================================
# Repressor rates
# =============================================================================
# Define binding energies of the different operators
energies = {'Oid': -17, 'O1': -15.3, 'O2': -13.9, 'O3': -9.7}

# Compute the rates for each repressor
kr_offs = {key: ccutils.model.kr_off_fun(value, k0, 
                                     kpon_double,
                                     kpoff_double,
                                     Vcell=Vcell) for key, value in
                                     energies.items()}

# Print repressor rates
print("""
The most probable parameters for the repressor in seconds^-1
------------------------------------------------------------
""")
for key, value in kr_offs.items():
    print('kr_off {0:s} = {1:.5f} s^-1'.format(key, value))
    

# =============================================================================
# Compute probability of each of the states
# =============================================================================

def prob_promoter(kr_on, kr_off, kp_on, kp_off, rm):
    '''
    Computes the probability of the three promoter states for a regulated
    promoter
    '''
    P_B = (kr_off * kp_on) / (kp_off * kr_off + kp_off * kr_on + kr_off * kp_on)
    P_E = (kp_off * kr_off) / (kp_off * kr_off + kp_off * kr_on + kr_off * kp_on)
    P_R = (kp_off * kr_on) / (kp_off * kr_off + kp_off * kr_on + kr_off * kp_on)

    return {'P_B': P_B, 'P_E': P_E, 'P_R': P_R}

# O1
R = 22
kr_on = 1 / Vcell / 0.6022 * k0 * R

probs_O1 = prob_promoter(kr_on, kr_offs['O1'], kpon_double, 
                         kpoff_double, rm_double)


print('''
Probability of each promoter state for O1 - R{:d}
-------------------------------------------------
'''.format(R))
for key, value in probs_O1.items():
    print('State {0:s} = {1:.5f}'.format(key, value))
 
