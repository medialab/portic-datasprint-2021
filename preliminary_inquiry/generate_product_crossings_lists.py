
from poitousprint import Portic, Toflit, get_pointcalls_commodity_purposes_as_toflit_product

toflit_client = Toflit()
portic_client = Portic()

chosen_classification = 'product_revolutionempire'

# récupération des pointcalls Portic qui concernent le datasprint
pointcalls_datasprint = portic_client.get_pointcalls(
 source_subset = 'Poitou_1789'
)

# enrichissement de ces pointcalls avec la propriété 'commodity_as_toflit' qui nous donne l'équivalent des produits navigo dans Toflit18 avec la classification choisie
croisement_produits = get_pointcalls_commodity_purposes_as_toflit_product(pointcalls_datasprint, product_classification=chosen_classification)

navigo_products_for_datasprint = set()
for pointcall in croisement_produits:
    if pointcall['commodity_purposes'] is not None:
        for commodity in pointcall['commodity_purposes']:
            navigo_products_for_datasprint.add(commodity['commodity_as_toflit'])


# récupération des flows Toflit18 qui concernent le datasprint
flows = toflit_client.get_flows(
    year=1789, 
    customs_region='La Rochelle',
)

toflit_products_for_datasprint = set()
for flow in flows:
    toflit_products_for_datasprint.add(flow[chosen_classification])

result1 = toflit_products_for_datasprint.intersection(navigo_products_for_datasprint)

result2 = toflit_products_for_datasprint.difference(navigo_products_for_datasprint)

result3 = navigo_products_for_datasprint.difference(toflit_products_for_datasprint)


# écriture dans un fichier txt

# write data in a file.
fichier_texte = open('dumps/croisement_produits_datasprint_' + chosen_classification + '.txt',"w")
  
# \n is placed to indicate EOL (End of Line)
fichier_texte.write("ensemble 1 - produits qu'on retrouve à la fois dans Toflit18 et Portic :\n") 
for produit in result1:
    fichier_texte.write(str(produit)+"\n")

fichier_texte.write("\n\n\nensemble 2 - produits qu'on retrouve exclusivement dans Toflit18 :\n") 
for produit in result2:
    fichier_texte.write(str(produit)+"\n")

fichier_texte.write("\n\n\nensemble 3 - produits qu'on retrouve exclusivement dans Portic :\n") 
for produit in result3:
    fichier_texte.write(str(produit)+"\n")

fichier_texte.close() #to change file access modes