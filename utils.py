import glob
import numpy as np

def load_angst_sfh(name, sfhdir = 'data/sfhs/'):
    ty = '<f8'
    dt = np.dtype([('t1', ty), ('t2',ty), ('dmod',ty), ('sfr',ty), ('met', ty)])
    fn = glob.glob("{0}*{1}*sfh".format(sfhdir,name))
    data = np.loadtxt(fn[0], usecols = (0,1,2,3,6) ,dtype = dt)

    return data

def nearest_index(array, value, axis = -1):
        return (np.abs(array-value)).argmin(axis = axis)

def rebin_sfh(pars, sfrs, subs):

    masses = sfrs* (10**pars['bin_starts']-10**pars['bin_ends'])
    nrebin = subs.max()+1
    sfr_rebin = np.zeros(nrebin)
    for i in range(nrebin):
        sfr_rebin[i] = masses[np.where(subs == i)].sum()
    
    pars['nrebin'] = nrebin
    pars['rebin_starts'] = (pars['bin_starts']
                            [np.searchsorted(subs,np.arange(nrebin), side = 'right') -1])
    pars['rebin_ends'] = (pars['bin_ends']
                          [np.searchsorted(subs,np.arange(nrebin), side = 'left')])
    pars['rebin_centers'] = (pars['rebin_starts']+pars['rebin_ends'])/2. -9 #in Gyr

    return sfr_rebin/(10**pars['rebin_starts']-10**pars['rebin_ends'])
