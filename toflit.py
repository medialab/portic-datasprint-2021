from base import Client
import csv

class Toflit(Client): 
    """
    Utilitaire permettant de requêter les données Toflit
    """
    BASE_URL = 'http://toflit18.medialab.sciences-po.fr/api'
    
    def _format_response(self, response):
        """
        Formatte les réponses de l'API Toflit pour renvoyer directement le payload des résultats
        """
        if response is not None:
            return response['result']
        else :
            return None
    
    def get_customs_regions(self, params=None):
        """
        Synopsis : récupère les "customs regions" (bureaux de ferme) de la base
        ---
        Paramètres : aucun
        """
        response = self.api('/regions', params=params)
        return self._format_response(response)
    
    def get_sources_types(self, params=None):
        """
        Synopsis : récupère les types de sources disponibles
        ---
        Paramètres : aucun
        """
        response = self.api('/source_types', params=params)
        return self._format_response(response)
    
    def get_product_classifications(self, params=None):
        """
        Synopsis : récupère les classifications de produits
        ---
        Paramètres : aucun
        """
        response = self.api('/classification', params=params)
        response = self._format_response(response)
        return response['product']

    def get_partner_classifications(self, params=None):
        """
        Synopsis : récupère les classifications de partenaires
        ---
        Paramètres : aucun
        """
        response = self.api('/classification', params=params)
        response = self._format_response(response)
        return response['partner']
    
    def get_classification_groups(self, classification, params=None):
        """
        Synopsis : récupère l'ensemble des catégories associées à une classification en particulier (sans le détail des valeurs)
        Paramètre classification : le nom de la classification préfixé par son type (ex. "product_simplification", ou "partner_source")
        ---
        Paramètres : aucun ?
        """
        response = self.api('/classification/' + classification + '/groups/', params=params)
        response = self._format_response(response)
        return response

    def get_classification_sliced_search(self, classification, params=None):
        """
        Synopsis : récupère le détail des groupements associés à une classification en particulier, se limite à une tranche de résultat
        Paramètre classification : le nom de la classification préfixé par son type (ex. "product_simplification", ou "partner_source")
        ---
        Paramètres : aucun ?
        """
        response = self.api('/classification/' + classification + '/search/', params=params)
        response = self._format_response(response)
        print ("Nombre de classifications trouvées dans cette tranche : ", len(response))
        return response

    # but à terme : avoir 1 seule fonction (nécessite de gérer correctement l’argument query par défaut)
    # @todo simplifier l'API de cette fonction si on se rend compte que l'utiliser est utile
    # @todo remove if not useful
    def get_classification_search(self, classification, params=None, query={"limit":"5000"}): 
        """
        Synopsis : récupère le détail des groupements associés à une classification en particulier.
        Paramètre classification : le nom de la classification préfixé par son type (ex. "product_simplification", ou "partner_source")
        Paramètre query modifiable, par défaut on récupère les résultats par tranche de 5000 classifications   
        ---
        Paramètres : aucun ?
        """

        #initialisations
        results = []
        current_query = query.copy()
        current_index = query.get('offset', 0) # on donne valeur par défaut
        current_query['offset']=current_index
        limit = query['limit']
        error = None
        length = 1 # longueur d'une tanche (initialisé à 1 pour 1er passage dans while)

        # tant que j'ai des réponses (ou pas d'erreurs) je récupère des résultats par tranches
        while length: 
            response = self.api('/classification/' + classification + '/search/', query=current_query) 
            temp_results = self._format_response(response)
            length = len(temp_results)
            # print("length of current result :", length)
            results += temp_results 
            current_query['offset'] += int(limit)

        print ("Nombre de classifications trouvées : ", len(results))
        return results 
    
    
    def get_locations(self, classification, params=None):
        """
        Synopsis : récupère le réseau des lieux (directions et partenaires) et le montant de leurs échanges
        ---
        Paramètre classification : l'id de la classification de partenaire à utiliser
        ---
        Paramètres :
        * dateMax : <int> # année de début
        * dateMin : <int> # année de fin
        * kind : total | import | export # quels flux utiliser
        * sourceType : <string> # id du type de source à utiliser
        * product : <Array<object>> # liste des produits à filtrer
        * productClassification : <string> # Classification de produit à utiliser pour le filtre
        """
        response = self.api('/viz/network/' + classification, method='post', params=None, data=params)
        return self._format_response(response)
    
    def get_time_series(self, params=None):
        """
        Synopsis : récupère des séries temporelles à propos des flux de marchandises
        ---
        Paramètres :
        * direction : <string> "$all$" | [nom de direction] # nom de la direction à filtrer
        * sourceType : <string> # id du type de source à utiliser
        * color: <string> # pas pertinent / relatif à la visualisation
        * dateMax : <int> # année de début
        * dateMin : <int> # année de fin
        * partnerClassification : <string> # le nom de la classification de partenaire à récupérer
        * partner : <Array<object>> # les partenaires commerciaux à prendre en compte (e.g. {name: 'Alsace', id: 'Alsace~partner_orthographic'})
        * kind : *total* | import | export # quels flux utiliser
        * product : <Array<object>> # liste des produits à filtrer
        * productClassification : <string> # Classification de produit à utiliser pour le filtre
        """
        response = self.api('/viz/line/', method='post', params=None, data=params)
        return self._format_response(response)
    
    # @todo remove if not useful
    def get_flows_per_year(self, type, params=None):
        """
        Synopsis : récupère les flux par année par direction ou par type de source
        ---
        Paramètre type : le type de flux 'direction' ou 'sourceType'
        ---
        Paramètres :
        * direction : <string> "$all$" | [nom de direction] # nom de la direction à filtrer
        * sourceType : <string> # id du type de source à utiliser
        * color: <string> # pas pertinent / relatif à la visualisation
        * dateMax : <int>
        * dateMin : <int>
        * partnerClassification : <string> # le nom de la classification de partenaire à récupérer
        * partner : <Array<object>> # les partenaires commerciaux à prendre en compte (e.g. {name: 'Alsace', id: 'Alsace~partner_orthographic'})
        * kind : *total* | import | export # quels flux utiliser
        * product : <Array<object>> # liste des produits à filtrer
        * productClassification : <string> # Classification de produit à utiliser pour le filtre
        """
        response = self.api('/viz/flows_per_year/' + type, method='post', params=None, data=params)
        return self._format_response(response)
    
    def get_product_terms(self, classification, params=None):
        """
        Synopsis : récupère des séries temporelles à propos des flux de marchandises
        ---
        Paramètre classification : l'id de la classification de produit à utiliser
        ---
        Paramètres :
        * direction : <string> "$all$" | [nom de direction] # nom de la direction à filtrer
        * sourceType : <string> # id du type de source à utiliser
        * color: <string> # pas pertinent / relatif à la visualisation
        * dateMax : <int>
        * dateMin : <int>
        * childClassification : <string> # le nom de la classification de produit à récupérer
        * child : <Array<object>> # les produits à filtrer (e.g. {name: 'Alsace', id: 'Alsace~partner_orthographic'})
        * partnerClassification : <string> # le nom de la classification de partenaire à récupérer
        * partner : <Array<object>> # les partenaires commerciaux à prendre en compte (e.g. {"id": "Raw_materials,_inedible,_except_fuels~product_sitc_EN", "name": "Raw materials, inedible, except fuels", "value": "Raw_materials,_inedible,_except_fuels~product_sitc_EN"})
        * kind : *total* | import | export # quels flux utiliser
        * product : <Array<object>> # liste des produits à filtrer
        * productClassification : <string> # Classification de produit à utiliser pour le filtre
        """
        response = self.api('/viz/terms/' + classification, method='post', params=None, data=params)
        return self._format_response(response)
    
    """
Brainstorming contenu des params :
- filtrage sur les colonnes : string si valeur unique, list de strings si plusieurs valeurs
- propriété "columns" avec nom des colonnes à intégrer

- "start_year": "1750"
- "end_year": "1755"

- "nest_data": True ou False
    """
    def get_flows(self, params=None):

        # préparation des params

        # mettre de côté l'éventuel liste des colonnes
        # filter_params = [ for ]
        results = []


        if params is not None:

            # test de la validité des paramètres

            # si on a start_year et pas end_year ou le contraire -> renvoyer une erreur
            if 'start_year' in params and 'end_year' not in params:
                print("You must put an end year") 
                raise
            elif 'end_year' in params and 'start_year' not in params:
                print("You must put a start year") 
                raise

            # si on start_year ou end_year et par ailleurs year -> year l'emporte
            if ('start_year' in params or 'end_year' in params) and 'year' in params:
                del params['start_year']
                del params['end_year']

        #lecture du csv avec tous les flows toflit => DictReader
        with open('data/toflit18_all_flows.csv', newline='') as csv_reader_file:
            reader = csv.DictReader(csv_reader_file, quotechar='"')

            for row in reader:
                if params is not None:
                    year = row['year'].split(".")[0]
                    #si  on a bien un strart_year et un end_year
                    if 'start_year' in params and 'end_year' in params:
                        #s'il existe : je convertis en int mes params start / end_year et je vais regarder si ma date est bien dans le bon span => si non je break (passage ligne suivante)
                        if int(year) < int(params['start_year']) or int(year) < int(params['end_year']):
                            continue

                    #pour chaque filtre (sauf break) : 
                    # for key,value in [couple for couple in params.items() if couple[0] != 'start_year' and couple[0] != 'end_year' and couple[0] != 'columns']: # year, 1789

                        #else: # autre type de filtre
                            #if filtre = string unique, on en fait une liste (caster)
                            #if row[key] != string1 | string2 | string3 (avec string1/2/3 dans la liste de filtrage) => on passe à la ligne d'après (arrète de passer dans les filtres : break)
                
                # si l'item n'a pas été défiltré, on le formatte avant de l'ajouter au résultat
                # on ne garde que les colonnes qui nous intéressent dans le résultat
                # (todo) modifier les données si nest_data est true
                results.append(row)    
        
    
        return results
    
    def get_flows_by_api(self, params=None):
        """
        Synopsis : récupère les flux au niveau de granularité maximal en fonction d'une série de paramètres
        ---
        Paramètres :
        * limit : <int> # nombre d'entrées à renvoyer
        * skip : <int> # à quel point de la liste commencer à renvoyer des éléments
        * columns : <array> | liste des colonnes à renvoyer concernant les flux
        * kind : *total* | import | export # quels flux utiliser
        * direction : <string> "$all$" | [nom de direction] # nom de la direction à filtrer
        * sourceType : <string> # id du type de source à utiliser
        * color: <string> # pas pertinent / relatif à la visualisation
        * dateMax : <int>
        * dateMin : <int>
        * partnerClassification : <string> # le nom de la classification de partenaire à récupérer
        * partner : <Array<object>> # les partenaires commerciaux à prendre en compte (e.g. {name: 'Alsace', id: 'Alsace~partner_orthographic'})
        * product : <Array<object>> # liste des produits à filtrer
        * productClassification : <string> # Classification de produit à utiliser pour le filtre
        """

        #initialisations
        results = []
        current_params = params.copy()
        current_index = params['skip'] if 'skip' in params else 0
        limit = params['limit'] if 'limit' in params else 10000
        error = None
        length = 1 # longueur d'une tanche (initialisé à 1 pour 1er passage dans while)

        # tant que j'ai des réponses (ou pas d'erreurs) je récupère des tranches de résultat
        while length: 
            # print("index courant :", current_index)
            response = self.api('/flows/', method='post', params=None, data={**current_params, "skip":current_index}) # retourne un objet json avec attribut result 
            temp_results = self._format_response(response)
            length = len(temp_results)
            # print("length of current result :", length)
            if length<limit: # si la longueur de la tranche est inférieure à la limite, on est arrivés à la dernière page d'affichage => on veut sortir du while
                length=0
            
            results += temp_results # stock global de résultats
            current_index += limit
            # print("index incrémenté :", current_index)

        print ("Nombre de flows trouvés : ", len(results))
        return results 
    