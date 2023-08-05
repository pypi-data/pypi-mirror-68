# -*- coding: utf-8 -*-
'''
All data and methods related to chemical identifiers.
'''

__all__ = ('checkCAS', 'CAS_from_any', 'PubChem', 'MW', 'formula', 'smiles', 
           'InChI', 'InChI_Key', 'IUPAC_name', 'name', 'synonyms', 
           '_MixtureDict', 'mixture_from_any', 'cryogenics', 'dippr_compounds',
           'pubchem_db')
import os
from .utils import CAS2int, int2CAS, to_nums
from .elements import periodic_table, homonuclear_elemental_gases, charge_from_formula, serialize_formula

folder = os.path.join('Data', 'Identifiers')
folder = os.path.join(os.path.dirname(__file__), folder)

def checkCAS(CASRN):
    '''Checks if a CAS number is valid. Returns False if the parser cannot 
    parse the given string..

    Parameters
    ----------
    CASRN : string
        A three-piece, dash-separated set of numbers

    Returns
    -------
    result : bool
        Boolean value if CASRN was valid. If parsing fails, return False also.

    Notes
    -----
    Check method is according to Chemical Abstract Society. However, no lookup
    to their service is performed; therefore, this function cannot detect
    false positives.

    Function also does not support additional separators, apart from '-'.
    
    CAS numbers up to the series 1 XXX XXX-XX-X are now being issued.
    
    A long can hold CAS numbers up to 2 147 483-64-7

    Examples
    --------
    >>> checkCAS('7732-18-5')
    True
    >>> checkCAS('77332-18-5')
    False
    '''
    try:
        check = CASRN[-1]
        CASRN = CASRN[::-1][1:]
        productsum = 0
        i = 1
        for num in CASRN:
            if num == '-':
                pass
            else:
                productsum += i*int(num)
                i += 1
        return (productsum % 10 == int(check))
    except:
        return False


class ChemicalMetadata:
    __slots__ = ['pubchemid', 'formula', 'MW', 'smiles', 'InChI', 'InChI_key',
                 'iupac_name', 'common_name', 'all_names', 'CAS', '_charge']
    def __repr__(self):
        return ('<ChemicalMetadata, name=%s, formula=%s, smiles=%s, MW=%g>'
                %(self.common_name, self.formula, self.smiles, self.MW))
        
    @property
    def charge(self):
        '''Charge of the species as an integer. Computed as a property as most
        species do not have a charge and so storing it would be a waste of 
        memory.
        '''
        try:
            return self._charge
        except AttributeError:
            self._charge = charge_from_formula(self.formula)
            return self._charge
        
    @property
    def CASs(self):
        return int2CAS(self.CAS)
    
    def __init__(self, pubchemid, CAS, formula, MW, smiles, InChI, InChI_key,
                 iupac_name, common_name, all_names):
        self.pubchemid = pubchemid
        self.CAS = CAS
        self.formula = formula
        self.MW = MW
        self.smiles = smiles
        self.InChI = InChI
        self.InChI_key = InChI_key
        self.iupac_name = iupac_name
        self.common_name = common_name
        self.all_names = all_names
        

class ChemicalMetadataDB:
    __slots__ = ('pubchem_index',
                 'smiles_index',
                 'InChI_index',
                 'InChI_key_index',
                 'name_index',
                 'CAS_index',
                 'formula_index',
                 'main_dbs',
                 'user_dbs',
    )
    def __init__(self, 
                 dbs=(os.path.join(folder, 'chemical identifiers.tsv'),
                      os.path.join(folder, 'chemical identifiers example user db.tsv'),
                      os.path.join(folder, 'Cation db.tsv'),
                      os.path.join(folder, 'Anion db.tsv'),
                      os.path.join(folder, 'Inorganic db.tsv'))):                
        self.pubchem_index = {}
        self.smiles_index = {}
        self.InChI_index = {}
        self.InChI_key_index = {}
        self.name_index = {}
        self.CAS_index = {}
        self.formula_index = {}
        for db in dbs: self.load(db)
        self.load_elements()
        
    def load_elements(self):
        for ele in periodic_table:
            CAS = int(ele.CAS.replace('-', '')) # Store as int for easier lookup
            all_names = [ele.name.lower()]
            
            obj = ChemicalMetadata(pubchemid=ele.PubChem, CAS=CAS, 
                                   formula=ele.symbol, MW=ele.MW, smiles=ele.smiles,
                                   InChI=ele.InChI, InChI_key=ele.InChI_key,
                                   iupac_name=ele.name.lower(), 
                                   common_name=ele.name.lower(), 
                                   all_names=all_names)
            
            if ele.InChI_key in self.InChI_key_index:
                if ele.number not in homonuclear_elemental_gases:
                    obj_old = self.InChI_key_index[ele.InChI_key]
                    for name in obj_old.all_names:
                        self.name_index[name] = obj    
            
            self.InChI_key_index[ele.InChI_key] = obj
            self.CAS_index[CAS] = obj
            self.pubchem_index[ele.PubChem] = obj
            self.smiles_index[ele.smiles] = obj
            self.InChI_index[ele.InChI] = obj
            self.formula_index[obj.formula] = obj
            
            if ele.number in homonuclear_elemental_gases:
                for name in all_names: self.name_index['monatomic ' + name] = obj    
            else:
                for name in all_names: self.name_index[name] = obj    

    def load(self, file_name):
        f = open(file_name)
        for line in f:
            # This is effectively the documentation for the file format of the file
            values = line.rstrip('\n').split('\t')
            (pubchemid, CAS, formula, MW, smiles, InChI, InChI_key, iupac_name, common_name) = values[0:9]
            CAS = int(CAS.replace('-', '')) # Store as int for easier lookup
            all_names = values[7:]
            pubchemid = int(pubchemid)

            obj = ChemicalMetadata(pubchemid, CAS, formula, float(MW), smiles,
                                    InChI, InChI_key, iupac_name, common_name, 
                                    all_names)
            
            # Lookup indexes
            self.CAS_index[CAS] = obj
            self.pubchem_index[pubchemid] = obj
            self.smiles_index[smiles] = obj
            self.InChI_index[InChI] = obj
            self.InChI_key_index[InChI_key] = obj
            self.formula_index[obj.formula] = obj
            for name in all_names: self.name_index[name] = obj
            for name in all_names:
                if name in self.name_index: pass
                else: self.name_index[name] = obj
                    
        f.close()
    
    def search_pubchem(self, pubchem):
        if not isinstance(pubchem, int): pubchem = int(pubchem)
        try: return self.pubchem_index[pubchem]
        except: pass
        
    def search_CAS(self, CAS):
        if not isinstance(CAS, int): CAS = CAS2int(CAS)
        try: return self.CAS_index[CAS]
        except: pass

    def search_smiles(self, smiles):
        try: return self.smiles_index[smiles]
        except: pass

    def search_InChI(self, InChI):
        try: return self.InChI_index[InChI]
        except: pass

    def search_InChI_key(self, InChI_key):
        try: return self.InChI_key_index[InChI_key]
        except: pass

    def search_name(self, name):
        try: return self.name_index[name]
        except: pass
    
    def search_formula(self, formula):
        try: return self.formula_index[formula]
        except: pass

pubchem_db = ChemicalMetadataDB()

def CAS_from_any(ID):
    '''
    Looks up the CAS number of a chemical by searching and testing for the
    string being any of the following types of chemical identifiers:
    
    * Name, in IUPAC form or common form or a synonym registered in PubChem
    * InChI name, prefixed by 'InChI=1S/' or 'InChI=1/'
    * InChI key, prefixed by 'InChIKey='
    * PubChem CID, prefixed by 'PubChem='
    * SMILES (prefix with 'SMILES=' to ensure smiles parsing; ex.
      'C' will return Carbon as it is an element whereas the SMILES 
      interpretation for 'C' is methane)
    * CAS number (obsolete numbers may point to the current number)    

    If the input is an ID representing an element, the following additional 
    inputs may be specified as 
    
    * Atomic symbol (ex 'Na')
    * Atomic number (as a string)

    Parameters
    ----------
    ID : str
        One of the name formats described above

    Returns
    -------
    CASRN : string
        A three-piece, dash-separated set of numbers

    Notes
    -----
    A LookupError is raised if the name cannot be identified. The PubChem 
    database includes a wide variety of other synonyms, but these may not be
    present for all chemcials.

    Examples
    --------
    >>> CAS_from_any('water')
    '7732-18-5'
    >>> CAS_from_any('InChI=1S/C2H6O/c1-2-3/h3H,2H2,1H3')
    '64-17-5'
    >>> CAS_from_any('CCCCCCCCCC')
    '124-18-5'
    >>> CAS_from_any('InChIKey=LFQSCWFLJHTTHZ-UHFFFAOYSA-N')
    '64-17-5'
    >>> CAS_from_any('pubchem=702')
    '64-17-5'
    >>> CAS_from_any('O') # only elements can be specified by symbol
    '17778-80-2'
    '''
    ID = ID.strip()
    ID_lower = ID.lower()
    
    # Permutate through various name options
    ID_no_space = ID.replace(' ', '')
    if not ID: raise ValueError('ID cannot be empty')
    ID_no_space_dash = ID_no_space[:-1].replace('-', '') + ID_no_space[-1]
    for name in (ID, ID_no_space, ID_no_space_dash):
        for name2 in (name, name.lower()):
            name_lookup = pubchem_db.search_name(name2)
            if name_lookup: return name_lookup.CASs
    
    if ID in periodic_table:
        return periodic_table[ID].CAS

    if checkCAS(ID):
        CAS_lookup = pubchem_db.search_CAS(ID)
        if CAS_lookup: return CAS_lookup.CASs
        
        # Handle the case of synonyms
        CAS_alternate_loopup = pubchem_db.search_name(ID)
        if CAS_alternate_loopup: return CAS_alternate_loopup.CASs
        
        raise LookupError('a valid CAS number was recognized, but its not in the database')
        
    ID_len = len(ID)
    if ID_len > 9:
        inchi_search = False
        # normal upper case is 'InChI=1S/'
        if ID_lower[0:9] == 'inchi=1s/':
            inchi_search = ID[9:]
        elif ID_lower[0:8] == 'inchi=1/':
            inchi_search = ID[8:]
        if inchi_search:
            inchi_lookup = pubchem_db.search_InChI(inchi_search)
            if inchi_lookup: return inchi_lookup.CASs
            raise LookupError('A valid InChI name was recognized, but it is not in the database')
        if ID_lower[0:9] == 'inchikey=':
            inchi_key_lookup = pubchem_db.search_InChI_key(ID[9:])
            if inchi_key_lookup: return inchi_key_lookup.CASs
            raise LookupError('A valid InChI Key was recognized, but it is not in the database')
    if ID_len > 8:
        if ID_lower[0:8] == 'pubchem=':
            pubchem_lookup = pubchem_db.search_pubchem(ID[8:])
            if pubchem_lookup: return pubchem_lookup.CASs
            raise LookupError('A PubChem integer identifier was recognized, but it is not in the database.')
    if ID_len > 7:
        if ID_lower[0:7] == 'smiles=':
            smiles_lookup = pubchem_db.search_smiles(ID[7:])
            if smiles_lookup: return smiles_lookup.CASs
            raise LookupError('A SMILES identifier was recognized, but it is not in the database.')

    # Try the smiles lookup anyway
    # Parsing SMILES is an option, but this is faster
    # Pybel API also prints messages to console on failure
    smiles_lookup = pubchem_db.search_smiles(ID)
    if smiles_lookup: return smiles_lookup.CASs
    
    try:
        formula_query = pubchem_db.search_formula(serialize_formula(ID))
        if formula_query and isinstance(formula_query, ChemicalMetadata):
            return formula_query.CASs
    except: pass
    
    # Try a direct lookup with the name - the fastest
    name_lookup = pubchem_db.search_name(ID)
    if name_lookup: return name_lookup.CASs
    
    raise LookupError(f'chemical {repr(ID)} not recognized')


def PubChem(CASRN):
    '''Given a CASRN in the database, obtain the PubChem database
    number of the compound.

    Parameters
    ----------
    CASRN : string
        Valid CAS number in PubChem database [-]

    Returns
    -------
    pubchem : int
        PubChem database id, as an integer [-]

    Notes
    -----
    CASRN must be an indexing key in the pubchem database.

    Examples
    --------
    >>> PubChem('7732-18-5')
    962

    References
    ----------
    .. [1] Pubchem.
    '''
    return pubchem_db.search_CAS(CASRN).pubchemid



def MW(CASRN):
    '''Given a CASRN in the database, obtain the Molecular weight of the
    compound, if it is in the database.

    Parameters
    ----------
    CASRN : string
        Valid CAS number in PubChem database

    Returns
    -------
    MolecularWeight : float

    Notes
    -----
    CASRN must be an indexing key in the pubchem database. No MW Calculation is
    performed; nor are any historical isotopic corrections applied.

    Examples
    --------
    >>> MW('7732-18-5')
    18.01528

    References
    ----------
    .. [1] Pubchem.
    '''
    return pubchem_db.search_CAS(CASRN).MW


def formula(CASRN):
    '''
    >>> formula('7732-18-5')
    'H2O'
    '''
    return pubchem_db.search_CAS(CASRN).formula


def smiles(CASRN):
    '''
    >>> smiles('7732-18-5')
    'O'
    '''
    return pubchem_db.search_CAS(CASRN).smiles


def InChI(CASRN):
    '''
    >>> InChI('7732-18-5')
    'H2O/h1H2'
    '''
    return pubchem_db.search_CAS(CASRN).InChI


def InChI_Key(CASRN):
    '''
    >>> InChI_Key('7732-18-5')
    'XLYOFNOQVPJJNP-UHFFFAOYSA-N'
    '''
    return pubchem_db.search_CAS(CASRN).InChI_key


def IUPAC_name(CASRN):
    '''
    >>> IUPAC_name('7732-18-5')
    'oxidane'
    '''
    return pubchem_db.search_CAS(CASRN).iupac_name

def name(CASRN):
    '''
    >>> name('7732-18-5')
    'water'
    '''
    return pubchem_db.search_CAS(CASRN).common_name


def synonyms(CASRN):
    '''
    >>> synonyms('98-00-0')
    ['furan-2-ylmethanol', 'furfuryl alcohol', '2-furanmethanol', '2-furancarbinol', '2-furylmethanol', '2-furylcarbinol', '98-00-0', '2-furanylmethanol', 'furfuranol', 'furan-2-ylmethanol', '2-furfuryl alcohol', '5-hydroxymethylfuran', 'furfural alcohol', 'alpha-furylcarbinol', '2-hydroxymethylfuran', 'furfuralcohol', 'furylcarbinol', 'furyl alcohol', '2-(hydroxymethyl)furan', 'furan-2-yl-methanol', 'furfurylalcohol', 'furfurylcarb', 'methanol, (2-furyl)-', '2-furfurylalkohol', 'furan-2-methanol', '2-furane-methanol', '2-furanmethanol, homopolymer', '(2-furyl)methanol', '2-hydroxymethylfurane', 'furylcarbinol (van)', '2-furylmethan-1-ol', '25212-86-6', '93793-62-5', 'furanmethanol', 'polyfurfuryl alcohol', 'pffa', 'poly(furfurylalcohol)', 'poly-furfuryl alcohol', '(fur-2-yl)methanol', '.alpha.-furylcarbinol', '2-hydroxymethyl-furan', 'poly(furfuryl alcohol)', '.alpha.-furfuryl alcohol', 'agn-pc-04y237', 'h159', 'omega-hydroxypoly(furan-2,5-diylmethylene)', '(2-furyl)-methanol (furfurylalcohol)', '40795-25-3', '88161-36-8']
    '''
    return pubchem_db.search_CAS(CASRN).all_names


### DIPPR Database, chemical list only
# Obtained via the command:
# list(pd.read_excel('http://www.aiche.org/sites/default/files/docs/pages/sponsor_compound_list-2014.xlsx')['Unnamed: 2'])[2:]
# This is consistently faster than creating a list and then making the set.
dippr_compounds = set()
with open(os.path.join(folder, 'dippr_2014.csv')) as f:
    dippr_compounds.update(f.read().split('\n'))


_MixtureDict = {}
_MixtureDictLookup = {}
with open(os.path.join(folder, 'Mixtures Compositions.tsv')) as f:
    '''Read in a dict of 90 or so mixutres, their components, and synonyms.
    Small errors in mole fractions not adding to 1 are known.
    Errors in adding mass fraction are less common, present at the 5th decimal.
    TODO: Normalization
    Mass basis is assumed for all mixtures.
    '''
    next(f)
    for line in f:
        values = to_nums(line.strip('\n').strip('\t').split('\t'))
        _name, _source, N = values[0:3]
        N = int(N)
        _CASs, _names, _ws, _zs = values[3:3+N], values[3+N:3+2*N], values[3+2*N:3+3*N], values[3+3*N:3+4*N]
        _syns = values[3+4*N:]
        if _syns:
            _syns = [i.lower() for i in _syns]
        _syns.append(_name.lower())
        _MixtureDict[_name] = {"CASs": _CASs, "N": N, "Source": _source,
                               "Names": _names, "ws": _ws, "zs": _zs,
                               "Synonyms": _syns}
        for syn in _syns:
            _MixtureDictLookup[syn] = _name


def mixture_from_any(ID):
    '''Looks up a string which may represent a mixture in the database of 
    thermo to determine the key by which the composition of that mixture can
    be obtained in the dictionary `_MixtureDict`.

    Parameters
    ----------
    ID : str
        A string or 1-element list containing the name which may represent a
        mixture.

    Returns
    -------
    key : str
        Key for access to the data on the mixture in `_MixtureDict`.

    Notes
    -----
    White space, '-', and upper case letters are removed in the search.

    Examples
    --------
    >>> mixture_from_any('R512A')
    'R512A'
    >>> mixture_from_any(u'air')
    'Air'
    '''
    ID = ID.lower().strip()
    ID2 = ID.replace(' ', '')
    ID3 = ID.replace('-', '')
    for i in [ID, ID2, ID3]:
        if i in _MixtureDictLookup:
            return _MixtureDictLookup[i]
    raise Exception('Mixture name not recognized')


# TODO LIST OF REFRIGERANTS FOR USE IN HEAT TRANSFER CORRELATIONS

cryogenics = {'132259-10-0': 'Air', '7440-37-1': 'Argon', '630-08-0':
'carbon monoxide', '7782-39-0': 'deuterium', '7782-41-4': 'fluorine',
'7440-59-7': 'helium', '1333-74-0': 'hydrogen', '7439-90-9': 'krypton',
'74-82-8': 'methane', '7440-01-9': 'neon', '7727-37-9': 'nitrogen',
'7782-44-7': 'oxygen', '7440-63-3': 'xenon'}
