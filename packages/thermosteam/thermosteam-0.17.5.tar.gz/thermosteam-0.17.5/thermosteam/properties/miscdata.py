# -*- coding: utf-8 -*-
'''
Miscillaneous data.
'''
__all__ = ('inorganic_data_CRC',
           'organic_data_CRC', 
           'VDI_saturation_dict', 
           'VDI_tabular_data')
import os
import copy
from .utils import to_nums, CASDataReader
from ..functional import rho_to_V

read = CASDataReader(__file__, 'Misc')

### CRC Handbook general tables
inorganic_data_CRC = read('Physical Constants of Inorganic Compounds.csv')
organic_data_CRC = read('Physical Constants of Organic Compounds.csv')

### VDI Saturation

emptydict = {"Name": None, "MW": None, "Tc": None, "T": [], "P": [],
             "Density (l)": [], "Density (g)": [], "Hvap": [], "Cp (l)": [],
            "Cp (g)": [], "Mu (l)": [], "Mu (g)": [], "K (l)": [], "K (g)": [],
            "Pr (l)": [], "Pr (g)": [], "sigma": [], "Beta": [],
            "Volume (l)": [], "Volume (g)": []}

# After some consideration, it has been devided to keep this load method as is.

VDI_saturation_dict = {}
with open(os.path.join(read.folder, 'VDI Saturation Compounds Data.csv')) as f:
    '''Read in a dict of assorted chemical properties at saturation for 58
    industrially important chemicals, from:
    Gesellschaft, V. D. I., ed. VDI Heat Atlas. 2E. Berlin : Springer, 2010.
    This listing is the successor to that in:
    Schlunder, Ernst U, and International Center for Heat and Mass Transfer.
    Heat Exchanger Design Handbook. Washington: Hemisphere Pub. Corp., 1983.
    '''
    next(f)
    for line in f:
        values = to_nums(line.strip('\n').split('\t'))
        (CASRN, _name, _MW, _Tc, T, P, rhol, rhog, Hvap, cpl, cpg, mul, mug, kl, kg, prl, prg, sigma, Beta) = values
        newdict = (VDI_saturation_dict[CASRN] if CASRN in VDI_saturation_dict else copy.deepcopy(emptydict))
        newdict["Name"] = _name
        newdict["MW"] = _MW
        newdict["Tc"] = _Tc
        newdict["T"].append(T)
        newdict["P"].append(P)
        newdict["Density (l)"].append(rhol)
        newdict["Density (g)"].append(rhog)  # Not actually used
        newdict["Hvap"].append(Hvap)
        newdict["Cp (l)"].append(cpl)  # Molar
        newdict["Cp (g)"].append(cpg)  # Molar
        newdict["Mu (l)"].append(mul)
        newdict["Mu (g)"].append(mug)
        newdict["K (l)"].append(kl)
        newdict["K (g)"].append(kg)
        newdict["Pr (l)"].append(prl)
        newdict["Pr (g)"].append(prl)
        newdict["sigma"].append(sigma)
        newdict["Beta"].append(Beta)
        newdict["Volume (l)"].append(rho_to_V(rhol, _MW))
        newdict["Volume (g)"].append(rho_to_V(rhog, _MW))
        VDI_saturation_dict[CASRN] = newdict


def VDI_tabular_data(CASRN, prop):
    r'''This function retrieves the tabular data available for a given chemical
    and a given property. Lookup is based on CASRNs. Length of data returned
    varies between chemicals. All data is at saturation condition from [1]_.

    Function has data for 58 chemicals.

    Parameters
    ----------
    CASRN : string
        CASRN [-]
    prop : string
        Property [-]

    Returns
    -------
    Ts : list
        Temperatures where property data is available, [K]
    props : list
        Properties at each temperature, [various]

    Notes
    -----
    The available properties are 'P', 'Density (l)', 'Density (g)', 'Hvap',
    'Cp (l)', 'Cp (g)', 'Mu (l)', 'Mu (g)', 'K (l)', 'K (g)', 'Pr (l)',
    'Pr (g)', 'sigma', 'Beta', 'Volume (l)', and 'Volume (g)'.

    Data is available for all properties and all chemicals; surface tension
    data was missing for mercury, but added as estimated from the a/b
    coefficients listed in Jasper (1972) to simplify the function.

    Examples
    --------
    >>> VDI_tabular_data('67-56-1', 'Mu (g)')
    ([337.63, 360.0, 385.0, 410.0, 435.0, 460.0, 500.0], [1.11e-05, 1.18e-05, 1.27e-05, 1.36e-05, 1.46e-05, 1.59e-05, 2.04e-05])

    References
    ----------
    .. [1] Gesellschaft, VDI, ed. VDI Heat Atlas. 2E. Berlin : Springer, 2010.
    '''
    try:
        d = VDI_saturation_dict[CASRN]
    except KeyError:
        raise Exception('CASRN not in VDI tabulation')
    try:
        props, Ts = d[prop], d['T']
    except:
        raise Exception('Property not specified correctly')
    Ts = [T for p, T in zip(props, Ts) if p]
    props = [p for p in props if p]

    # Not all data series convererge to correct values
    if prop == 'sigma':
        Ts.append(d['Tc'])
        props.append(0)
    return Ts, props


