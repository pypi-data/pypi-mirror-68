# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 18:40:05 2019

@author: yoelr
"""
from flexsolve import njitable
from ..utils import thermo_user, Cache
from scipy.optimize import differential_evolution
from .._thermal_condition import ThermalCondition
from .vle import VLE
import numpy as np

__all__ = ('LLE', 'LLECache')

def liquid_activities(mol_l, T, f_gamma):
    total_mol_l = mol_l.sum()
    if total_mol_l:
        x = mol_l / total_mol_l
        gamma = f_gamma(x, T)
        xgamma = x * gamma
    else:
        xgamma = np.ones_like(mol_l)
    return xgamma

@njitable
def gibbs_free_energy_of_liquid(mol_l, xgamma):
    xgamma[xgamma <= 0] = 1
    g_mix = (mol_l * np.log(xgamma)).sum()
    return g_mix

def lle_objective_function(mol_l, mol, T, f_gamma):
    mol_L = mol - mol_l
    xgamma_l = liquid_activities(mol_l, T, f_gamma)
    xgamma_L = liquid_activities(mol_L, T, f_gamma)
    g_mix_l = gibbs_free_energy_of_liquid(mol_l, xgamma_l)
    g_mix_L = gibbs_free_energy_of_liquid(mol_L, xgamma_L)
    g_mix = g_mix_l + g_mix_L
    return g_mix

def solve_lle_liquid_mol(mol, T, f_gamma, **differential_evolution_options):
    args = (mol, T, f_gamma)
    bounds = np.zeros([mol.size, 2])
    bounds[:, 1] = mol
    result = differential_evolution(lle_objective_function, bounds, args,
                                    **differential_evolution_options)
    return result.x

@thermo_user
class LLE:
    """
    Create a LLE object that performs liquid-liquid equilibrium when called.
    Differential evolution is used to find the solution that globally minimizes
    the gibb's free energy of both phases.
        
    Parameters
    ----------
    imol : MaterialIndexer
        Chemical phase data is stored here.
    thermal_condition=None : ThermalCondition, optional
        The temperature and pressure used in calculations are stored here.
    thermo=None : Thermo, optional
        Themodynamic property package for equilibrium calculations.
        Defaults to `thermosteam.settings.get_thermo()`.
    
    Examples
    --------
    >>> from thermosteam import indexer, equilibrium, settings
    >>> settings.set_thermo(['Water', 'Ethanol', 'Octane', 'Hexane'])
    >>> imol = indexer.MolarFlowIndexer(
    ...             l=[('Water', 304), ('Ethanol', 30)],
    ...             L=[('Octane', 40), ('Hexane', 1)])
    >>> lle = equilibrium.LLE(imol)
    >>> lle(T=360)
    >>> lle
    LLE(imol=MolarFlowIndexer(
            L=[('Water', 2.671), ('Ethanol', 2.284), ('Octane', 39.92), ('Hexane', 0.9885)],
            l=[('Water', 301.3), ('Ethanol', 27.72), ('Octane', 0.07885), ('Hexane', 0.01154)]),
        thermal_condition=ThermalCondition(T=360.00, P=101325))
    
    """
    __slots__ = ('_thermo', # [float] Thermo object for estimating mixture properties.
                 '_imol', # [MaterialIndexer] Stores vapor and liquid molar data.
                 '_thermal_condition', # [ThermalCondition] T and P values are stored here.
)
    differential_evolution_options = {'seed': 0,
                                      'popsize': 12,
                                      'tol': 0.002}
    
    def __init__(self, imol, thermal_condition=None, thermo=None):
        self._load_thermo(thermo)
        self._thermal_condition = thermal_condition or ThermalCondition(298.15, 101325.)
        self._imol = imol
    
    def __call__(self, T, P=None):
        """
        Perform liquid-liquid equilibrium.

        Parameters
        ----------
        T : float
            Operating temperature [K].
        P : float, optional
            Operating pressure [Pa].
            
        """
        thermal_condition = self._thermal_condition
        thermal_condition.T = T
        if P: thermal_condition.P = P
        imol = self._imol
        mol, index, lle_chemicals = self.get_liquid_mol_data()
        total_mol = mol.sum()
        if total_mol:
            gamma = self.thermo.Gamma(lle_chemicals)
            mol_l = solve_lle_liquid_mol(mol, T, gamma,
                                         **self.differential_evolution_options)
            imol['l'][index] = mol_l
            imol['L'][index] = mol - mol_l
    
    def get_liquid_mol_data(self):
        # Get flow rates
        imol = self._imol
        imol['l'] = mol =  imol['l'] + imol['L']
        imol['L'] = 0
        index = self.chemicals.get_lle_indices(mol > 0)
        mol = mol[index]
        chemicals = self.chemicals.tuple
        lle_chemicals = [chemicals[i] for i in index]
        return mol, index, lle_chemicals
    
    imol = VLE.imol
    thermal_condition = VLE.thermal_condition
    __format__ = VLE.__format__
    __repr__ = VLE.__repr__

class LLECache(Cache): load = LLE
del Cache    