import csv
from csv import DictReader, DictWriter

# but d'avoir un dict par ligne avec 2 attributs en plus : 
"""
'partner_orthographic X origin_origin' : {
    ...
    'partner_coding': 'string',
    'origin_coding' : 'string'
}
"""

# dict de dict qui contient toutes les lignes
partner_and_origin_coding_dict = {}

partner_colonies = ['Sénégal', 'Saint-Domingue', 'Amérique']
# partner_france = []
partner_etranger = ['Étranger', 'Quatre villes hanséatiques', 'Prusse', "Etats de l'Empereur", 'Portugal', 'Hollande', 'Espagne', 'Danemark', 'Angleterre', 'Russie', 'Suède', 'États-Unis']

origins_local = ['Aunis', 'Poitou', 'Saintonge', 'Angoumois']
# origins_france = []
origins_etranger = ['Étranger']

# tableau qui contient une colonne par clé de dict 
with open('data/extraction 1789 La Rochelle toutes sources exports.csv', 'r', newline='') as csvfile:
    csv_file = csv.DictReader(csvfile, quotechar='|')
    
    for row in csv_file:
        # initialisation d'un dict vide
        partner_and_origin_coding_dict[row['partner_orthographic'] + ' X ' + row['origin_origin']] = {
            'customs_office':
            'product':
            'value'
        }

        # codage du partenaire
        if row['partner_orthographic'] in partner_colonies:
            partner_and_origin_coding_dict[row['partner_orthographic'] + ' X ' + row['origin_origin']]['partner_coding'] = 'Colonies' 
        elif row['partner_orthographic'] in partner_etranger:
            partner_and_origin_coding_dict[row['partner_orthographic'] + ' X ' + row['origin_origin']]['partner_coding'] = 'Etranger' 
        else:
            partner_and_origin_coding_dict[row['partner_orthographic'] + ' X ' + row['origin_origin']]['partner_coding'] = 'France' 

        # codage de l'origine
        if row['origin_origin'] in origins_local:
            partner_and_origin_coding_dict[row['partner_orthographic'] + ' X ' + row['origin_origin']]['origin_coding'] = 'Local' 
        elif row['partner_orthographic'] in origins_etranger:
            partner_and_origin_coding_dict[row['partner_orthographic'] + ' X ' + row['origin_origin']]['origin_coding'] = 'Etranger' 
        else:
            partner_and_origin_coding_dict[row['partner_orthographic'] + ' X ' + row['origin_origin']]['origin_coding'] = 'France' 


# tableau qui contient une colonne par clé de dict 
with open('productions/equipe_2/visualisations_deux_commerces/visualisation_partenaires_origines_codes.csv', 'w', newline='') as csvfile:
        fieldnames = ['partner_coding','origin_coding']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        for row in partner_and_origin_coding_dict: 
            writer.writerow(row)
