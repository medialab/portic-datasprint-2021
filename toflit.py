from base import Client

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
    
    def get_directions(self, params=None):
        """
        Synopsis : récupère les directions de la base
        ---
        Paramètres : aucun
        """
        response = self.api('/directions', params=params)
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
    
    def get_flows(self, params=None):
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
        current_index = params['skip']
        limit = params['limit']
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
    