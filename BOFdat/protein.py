"""
Protein
=======

This module generates BOFsc for the 20 amino acids contained in proteins.

"""
import pandas as pd
AMINO_ACIDS = ['A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W','Y']

# Methods
'''
DEPRECATED
def _import_genome(genbank):
    from Bio import SeqIO
    try:
        # Unique handle in record
        genome_record = SeqIO.read(genbank, 'genbank')
    except:
        # Multiple handles in record
        genome_record = SeqIO.parse(genbank, 'genbank')
    return genome_record
'''
def _get_protein_sequence(path_to_genbank):
    # Get the prot id and sequence of each protein from genbank file
    from Bio import SeqIO
    try:
        # Unique handle in record
        genome_record = SeqIO.read(path_to_genbank, 'genbank')
        seq_dict = {}
        for i in genome_record.features:
            if i.type == 'CDS' and 'protein_id' in i.qualifiers:
                seq_dict[i.qualifiers['protein_id'][0]] = i.qualifiers['translation'][0]

    except:
        # Multiple handles in record
        genome_record = SeqIO.parse(path_to_genbank, 'genbank')
        seq_dict = {}
        for record in genome_record:
            for i in record.features:
                if i.type == 'CDS' and 'protein_id' in i.qualifiers:
                    seq_dict[i.qualifiers['protein_id'][0]] = i.qualifiers['translation'][0]

    return seq_dict

def _import_model(path_to_model):
    import cobra
    extension = path_to_model.split('.')[-1]
    if extension == 'json':
        return cobra.io.load_json_model(path_to_model)
    elif extension == 'xml':
        return cobra.io.read_sbml_model(path_to_model)

def _import_proteomic(path_to_proteomic):
    import pandas as pd
    proteomics =pd.read_csv(path_to_proteomic, names=['gene_ID', 'Mean'], skiprows=1)
    keys = [k for k in proteomics.gene_ID]
    values = [v for v in proteomics.Mean]
    return dict(zip(keys, values))

def _get_aa_composition(seq_dict):
    # For each protein find the amino acid composition
    # Outputs a dictionnary of dictionnaries where:
    # Keys = locus_tag
    # Values = A dictionary for each amino acid
    # This dictionary contains:
    # Keys = amino acid by letter code
    # Values = the occurence of that amino acid
    list_of_dict = []
    for k,v seq_dict.iteritems():
        list_of_occurences = []
        # Get the occurence for each letter
        for letter in AMINO_ACIDS:
            protein_sequence = v
            occurence_of_letter = protein_sequence.count(letter)
            list_of_occurences.append(occurence_of_letter)
        # Generate dictionary of occurences for a given gene
        dict_of_occurences = dict(zip(AMINO_ACIDS, list_of_occurences))
        # Generate dict for each gene
        dict_per_prot = {k: dict_of_occurences}
        # Store the amount of each amino acid per gene in a list
        list_of_dict.append(dict_per_prot)

    return list_of_dict

def _normalize_aa_composition(list_of_dict, path_to_proteomic):
    # Normalize the value of each amino acid per protein following proteomic data
    normalized_dict = {'A': 0., 'C': 0., 'D': 0., 'E': 0., 'F': 0., 'G': 0., 'H': 0., 'I': 0.,
                       'K': 0., 'L': 0., 'M': 0., 'N': 0., 'P': 0., 'Q': 0., 'R': 0., 'S': 0., 'T': 0., 'V': 0.,
                       'W': 0., 'Y': 0.}
    # Import proteomic data into dictionnary
    proteomics = _import_proteomic(path_to_proteomic)
    for d in list_of_dict:
        # Get the coefficient from proteomics
        coeff = proteomics.get(str(list(d.keys())[0]))
        # If no protein abundance coefficient is 0.
        try:
            coeff_number = float(coeff)
        except:
            coeff_number = 0.

        # Multiply each amino acid by the coefficient
        amino_acids = list(d.values())
        for letter in AMINO_ACIDS:
            value = float(amino_acids[0].get(letter))
            # Update the normalized value
            normalized_value = value * coeff_number
            new_value = normalized_dict.get(letter) + normalized_value
            normalized_dict[letter] = new_value

    return normalized_dict

def _get_norm_sum(normalized_dict):
    # 1- Sum normalized ratios
    norm_sum = 0.
    for letter in AMINO_ACIDS:
        value = normalized_dict.get(letter)
        norm_sum = value + norm_sum

    return norm_sum

def _get_ratio(normalized_dict, norm_sum, PROTEIN_RATIO):
    # 2- Divide letter to norm_sum to get ratio of each amino acid in the cell
    # based on proteomic data
    ratio_dict = {'A': 0., 'C': 0., 'D': 0., 'E': 0., 'F': 0., 'G': 0., 'H': 0., 'I': 0.,
                  'K': 0., 'L': 0., 'M': 0., 'N': 0., 'P': 0., 'Q': 0., 'R': 0., 'S': 0., 'T': 0., 'V': 0.,
                  'W': 0., 'Y': 0.}

    # Constant for the amount of protein in the cell
    PROTEIN_WEIGHT = CELL_WEIGHT * PROTEIN_RATIO
    for letter in AMINO_ACIDS:
        value = normalized_dict.get(letter)
        ratio = value / norm_sum
        # Convert ratios to grams
        converted_ratio = ratio * PROTEIN_WEIGHT
        ratio_dict[letter] = converted_ratio

    return ratio_dict

def _convert_to_coefficient(ratio_dict, path_to_model, CELL_WEIGHT):
    model = import_model(path_to_model)
    # 3- Convert gram ratios to mmol/g Dry weight
    '''
    To verify that the normalized to grams to get to the total amount of protein
    (here everything is converted to grams instead of femto grams)
    '''
    letter_to_bigg = {'A': model.metabolites.ala__L_c, 'C': model.metabolites.cys__L_c,
                      'D': model.metabolites.asp__L_c, 'E': model.metabolites.glu__L_c,
                      'F': model.metabolites.phe__L_c,
                      'G': model.metabolites.gly_c, 'H': model.metabolites.his__L_c,
                      'I': model.metabolites.ile__L_c, 'K': model.metabolites.lys__L_c,
                      'L': model.metabolites.leu__L_c,
                      'M': model.metabolites.met__L_c, 'N': model.metabolites.asn__L_c,
                      'P': model.metabolites.pro__L_c, 'Q': model.metabolites.gln__L_c,
                      'R': model.metabolites.arg__L_c,
                      'S': model.metabolites.ser__L_c, 'T': model.metabolites.thr__L_c,
                      'V': model.metabolites.val__L_c, 'W': model.metabolites.trp__L_c,
                      'Y': model.metabolites.tyr__L_c}

    metabolites, coefficients = [],[]
    # Get number of moles from number of grams
    for letter in AMINO_ACIDS:
        metab = letter_to_bigg.get(letter)
        mol_weight = metab.formula_weight
        grams = ratio_dict.get(letter)
        mmols_per_cell = (grams / mol_weight) * 1000
        mmols_per_gDW = mmols_per_cell / CELL_WEIGHT
        coefficients.append(mmols_per_gDW)
        metabolites.append(letter_to_bigg.get(letter))

    Protein_biomass_coefficients = dict(zip(metabolites,coefficients))
    return Protein_biomass_coefficients


def generate_coefficients(path_to_genbank, path_to_model, path_to_proteomic, CELL_WEIGHT=280, PROTEIN_RATIO=0.55):
    """

    Generates a dictionary of metabolite:coefficients for the 20 amino acids contained in proteins from the organism's
    GenBank annotated file, total Protein weight percentage and proteomic data.

    :param path_to_genbank: a path to the GenBank annotation file of the organism, format should be compatible with BioPython SeqIO

    :param path_to_model: a path to the model, format supported are json and xml

    :param path_to_proteomic: a two column pandas dataframe (protein_id, abundance)

    :param CELL_WEIGHT: experimentally measured cell weight in femtograms, float

    :param PROTEIN_RATIO: the ratio of DNA in the entire cell

    :return: a dictionary of metabolites and coefficients
    """
    # Operations
    # 1- Parse the genome, extract protein sequence, count and store amino acid composition of each protein
    seq_dict = _get_protein_sequence(path_to_genbank)
    list_of_dict = _get_aa_composition(seq_dict)
    normalized_dict = _normalize_aa_composition(list_of_dict,path_to_proteomic)

    # 2- Get coefficients from experimental proteomics data
    # Proteomics data should come in a 2 columns standard format protein_id:abundance
    norm_sum = _get_norm_sum(normalized_dict)
    ratio_dict = get_ratio(normalized_dict, norm_sum, PROTEIN_RATIO)
    biomass_coefficients = convert_to_coefficient(ratio_dict,path_to_model, CELL_WEIGHT)

    return biomass_coefficients

'''
The option to update the coefficients of the metabolites in the biomass objective function is left to the user
'''
def update_biomass_coefficients(dict_of_coefficients,model):
    """

    Updates the biomass coefficients given the input metabolite:coefficient dictionary.

    :param dict_of_coefficients: dictionary of metabolites and coefficients

    :param model: model to update

    :return: The biomass objective function is updated.
    """
    from BOFdat import update
    update.update_biomass(dict_of_coefficients,model)