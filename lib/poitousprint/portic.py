from poitousprint.base import Client


class Portic(Client):
  """
  Utilitaire permettant de requêter l'API à un haut niveau d'abstraction, et d'accéder facilement à la documentation pour chaque endpoint.

  Sommaire des méthodes exposées :

  * get_fieldnames
  * get_pointcalls
  * get_travels
  * get_departures_details
  * get_destinations_aggregated
  * get_flows
  * get_ports
  """
  BASE_URL = 'http://data.portic.fr/api'

  def get_fieldnames(self, **kwargs):
    """
    Synopsis:
    Récupère les noms des variables des données.
    ---
    Paramètres (la valeur entre *étoiles* est la valeur par défaut si le paramètre de requête n'est pas défini):

    * API = pointcalls | travels | any # réduire à une API particulière

    * params : *all* | liste de noms longs des attributs à renvoyer (e.g. 'params=id,departure,destination')
    * format : *json* | csv # format de la réponse
    # permet de raccourcir les noms des attributs et donc d'alléger la taille du JSON téléchargé.
    * shortenfields : true | *false*
    # permet de récupérer les données concernant l'arrivée d'un voyage en plus des données du départ (données par défaut).
    * both_to : true | *false*
    * date : YYYY | *1787* # pour filtrer les données sur une année donnée. L'année de la date d'arrivée ou de la date de départ doit commencer par ces 4 digits : 1787 ou  1789 par exemple. Exemple : http://data.portic.fr/api/pointcalls/?format=json&date=1789
    * zipped : true | *false*

    """
    response = self.api('/fieldnames', params=kwargs)
    return response

  def get_pointcalls(self, **kwargs):
    """
    Synopsis:
    Retourne les données d'observation à chaque escale des navires.
    ---
    Paramètres de filtrage :
    * voir $.get_fieldnames(API="pointcalls") pour voir toutes les valeurs filtrables : vous pouvez donner une chaîne unique ou une liste de chaîne pour filtrer plusieurs valeurs possibles

    Paramètres de requête généraux (la valeur entre *étoiles* est la valeur par défaut si le paramètre de requête n'est pas défini):

    * params : *all* | liste de noms longs des attributs (e.g. 'params=id,departure,destination')
    * format : *json* | csv # format de la réponse
    # permet de raccourcir les noms des attributs et donc d'alléger la taille du JSON téléchargé.
    * shortenfields : true | *false*
    # permet de récupérer les données concernant l'arrivée d'un voyage en plus des données du départ (données par défaut).
    * both_to : true | *false*
    * year : YYYY | *1787* # pour filtrer les données sur une année donnée. L'année de la date d'arrivée ou de la date de départ doit commencer par ces 4 digits : 1787 ou  1789 par exemple. Exemple : http://data.portic.fr/api/pointcalls/?format=json&date=1789
    * zipped : true | *false*

    Paramètres de requête spécifiques :

    * API = pointcalls | travels | any # réduire à une API particulière
    * [tous les noms de propriétés des pointcalls] : string ou liste de string définissant les valeurs à filtrer
    """
    # distingue les params qui peuvent être donnés directement à l'api et ceux qui doivent être filtrés après la requête
    API_PARAMS = ['params', 'format',
    'shortenfields', 'both_to', 'year', 'zipped']
    consumable_params = {}
    filter_params = {}

    for key, value in kwargs.items():
      if key in API_PARAMS:
        consumable_params[key] = value
      else:
        filter_params[key] = value
    
    # test de la validité des paramètres
    # si on a start_year et pas end_year ou le contraire -> renvoyer une erreur
    if 'start_year' not in filter_params and 'end_year' in filter_params:
        raise TypeError("You must put an end year")
    elif 'end_year' not in filter_params and 'start_year' in filter_params:
        raise TypeError("You must put a start year")

    # si on start_year ou end_year et par ailleurs year -> year l'emporte
    if ('start_year' in filter_params or 'end_year' in filter_params) and 'year' in consumable_params:
        del filter_params['start_year']
        del filter_params['end_year']
    
    # harmonisation de l'API avec toflit18 -> on prend year en input mais on donne "date" à l'api
    if 'year' in consumable_params:
      consumable_params['date'] = consumable_params['year']
      del consumable_params['year']

    response = []
    # traitement des années multiples : on itère dans toutes les années entre la start_year et la end_year
    if 'start_year' in filter_params and 'end_year' in filter_params:
      for year in [y + filter_params['start_year'] for y in range(int(filter_params['end_year'] - int(filter_params['start_year'])))]:
        that_year = self.api('/pointcalls', params={**consumable_params, "date": year})
        response = response + that_year
      del filter_params['start_year']
      del filter_params['end_year']
    # traitement d'une seule année
    else :
      response = self.api('/pointcalls', params=consumable_params)

    # on filtre si nécessaire les résultats en fonction des paramètres résiduels qui n'ont pas pu être "consommés" par l'API
    results = []
    for item in response:
      #pour chaque filtre (sauf filtre timespan et filtrage des colomnes) :
      is_valid = True
      for key,filter_value in filter_params.items(): 
          
          item_value = item[key]

          # si la valeur est une liste : on caste en string ses membres
          if isinstance(filter_value, list):
              filter_value = [str(val) for val in filter_value]
          # sinon c'est un tableau à une valeur qu'on caste en string
          else:
              filter_value = [str(filter_value)]
          # à partir de là, filter_value est une liste de strings

          #si la ligne a un attribut qui fait partie des valeurs acceptées par le filtre => on examine les autres filtres 
          if item_value not in filter_value:
              is_valid = False
              break
      if is_valid is True:
        results.append(item)
    return results
  
  def get_flows(self, **kwargs):
    """
    Synopsis:
    Retourne une liste de flux, c'est-à-dire de voyages liés à des ports spécifiques, soit en y entrant (direction "in"), soit en en sortant (direction "out"), soit en ayant navigué autour (direction "in-out")
    ---

    Paramètres de filtrage :
    * voir $.get_fieldnames(API="travels") pour voir toutes les valeurs filtrables : vous pouvez donner une chaîne unique ou une liste de chaîne pour filtrer plusieurs valeurs possibles

    Paramètres de requête généraux (la valeur entre *étoiles* est la valeur par défaut si le paramètre de requête n'est pas défini):

    * params : *all* | liste de noms longs des attributs (e.g. 'params=id,departure,destination')
    * format : *json* | csv # format de la réponse
    * shortenfields : true | *false* # permet de raccourcir les noms des attributs et donc d'alléger la taille du JSON téléchargé.
    * both_to : true | *false* # permet de récupérer les données concernant l'arrivée d'un voyage en plus des données du départ (données par défaut). 
    * year : YYYY | *1787* # pour filtrer les données sur une année donnée. L'année de la date d'arrivée ou de la date de départ doit commencer par ces 4 digits : 1787 ou  1789 par exemple. Exemple : http://data.portic.fr/api/pointcalls/?format=json&date=1789
    * zipped : true | *false*

    Paramètres de requête spécifiques :

    * ports: [int] (UHGS_id) # liste des ids de ports à filtrer (séparés par des virgules)
    """
    # distingue les params qui peuvent être donnés directement à l'api et ceux qui doivent être filtrés après la requête
    API_PARAMS = ['params', 'format', 'shortenfields', 'both_to', 'year', 'zipped']
    
    consumable_params = {}
    filter_params = {}

    for key, value in kwargs.items():
      if key in API_PARAMS:
        consumable_params[key] = value
      else:
        filter_params[key] = value
    
    # test de la validité des paramètres
    # si on a start_year et pas end_year ou le contraire -> renvoyer une erreur
    if 'start_year' not in filter_params and 'end_year' in filter_params:
        raise TypeError("You must put an end year")
    elif 'end_year' not in filter_params and 'start_year' in filter_params:
        raise TypeError("You must put a start year")

    # si on start_year ou end_year et par ailleurs year -> year l'emporte
    if ('start_year' in filter_params or 'end_year' in filter_params) and 'year' in consumable_params:
        del filter_params['start_year']
        del filter_params['end_year']
    
    # harmonisation de l'API avec toflit18 -> on prend year en input mais on donne "date" à l'api
    if 'year' in consumable_params:
      consumable_params['date'] = consumable_params['year']
      del consumable_params['year']

    response = []
    # traitement des années multiples : on itère dans toutes les années entre la start_year et la end_year
    if 'start_year' in filter_params and 'end_year' in filter_params:
      for year in [y + filter_params['start_year'] for y in range(int(filter_params['end_year'] - int(filter_params['start_year'])))]:
        that_year = self.api('/flows', params={**consumable_params, "date": year})
        response = response + that_year
      del filter_params['start_year']
      del filter_params['end_year']
    # traitement d'une seule année
    else :
      response = self.api('/flows', params=consumable_params)

    # on filtre si nécessaire les résultats en fonction des paramètres résiduels qui n'ont pas pu être "consommés" par l'API
    results = []
    for item in response:
      #pour chaque filtre (sauf filtre timespan et filtrage des colomnes) :
      is_valid = True
      for key,filter_value in filter_params.items(): 
          
          item_value = item[key]

          # si la valeur est une liste : on caste en string ses membres
          if isinstance(filter_value, list):
              filter_value = [str(val) for val in filter_value]
          # sinon c'est un tableau à une valeur qu'on caste en string
          else:
              filter_value = [str(filter_value)]
          # à partir de là, filter_value est une liste de strings

          #si la ligne a un attribut qui fait partie des valeurs acceptées par le filtre => on examine les autres filtres 
          if item_value not in filter_value:
              is_valid = False
              break
      if is_valid is True:
        results.append(item)
    return results


  def get_travels(self, **kwargs):
    """
    Synopsis:
    Récupère les données de trajectoires calculées.
    ---
    Paramètres de requête généraux (la valeur entre *étoiles* est la valeur par défaut si le paramètre de requête n'est pas défini):

    * params : *all* | liste de noms longs des attributs (e.g. 'params=id,departure,destination')
    * format : *json* | csv # format de la réponse
    * shortenfields : true | *false* # permet de raccourcir les noms des attributs et donc d'alléger la taille du JSON téléchargé.
    * both_to : true | *false* # permet de récupérer les données concernant l'arrivée d'un voyage en plus des données du départ (données par défaut). 
    * date : YYYY | *1787* # pour filtrer les données sur une année donnée. L'année de la date d'arrivée ou de la date de départ doit commencer par ces 4 digits : 1787 ou  1789 par exemple. Exemple : http://data.portic.fr/api/pointcalls/?format=json&date=1789
    * zipped : true | *false*

    Paramètres de requête spécifiques : /
    """
    # distingue les params qui peuvent être donnés directement à l'api et ceux qui doivent être filtrés après la requête
    API_PARAMS = ['params', 'format', 'shortenfields', 'both_to', 'year', 'zipped']
    
    consumable_params = {}
    filter_params = {}

    for key, value in kwargs.items():
      if key in API_PARAMS:
        consumable_params[key] = value
      else:
        filter_params[key] = value
    
    # test de la validité des paramètres
    # si on a start_year et pas end_year ou le contraire -> renvoyer une erreur
    if 'start_year' not in filter_params and 'end_year' in filter_params:
        raise TypeError("You must put an end year")
    elif 'end_year' not in filter_params and 'start_year' in filter_params:
        raise TypeError("You must put a start year")

    # si on start_year ou end_year et par ailleurs year -> year l'emporte
    if ('start_year' in filter_params or 'end_year' in filter_params) and 'year' in consumable_params:
        del filter_params['start_year']
        del filter_params['end_year']
    
    # harmonisation de l'API avec toflit18 -> on prend year en input mais on donne "date" à l'api
    if 'year' in consumable_params:
      consumable_params['date'] = consumable_params['year']
      del consumable_params['year']

    response = []
    # traitement des années multiples : on itère dans toutes les années entre la start_year et la end_year
    if 'start_year' in filter_params and 'end_year' in filter_params:
      for year in [y + filter_params['start_year'] for y in range(int(filter_params['end_year'] - int(filter_params['start_year'])))]:
        that_year = self.api('/travels', params={**consumable_params, "date": year})
        response = response + that_year
      del filter_params['start_year']
      del filter_params['end_year']
    # traitement d'une seule année
    else :
      response = self.api('/travels', params=consumable_params)

    # on filtre si nécessaire les résultats en fonction des paramètres résiduels qui n'ont pas pu être "consommés" par l'API
    results = []
    for item in response:
      #pour chaque filtre (sauf filtre timespan et filtrage des colomnes) :
      is_valid = True
      for key,filter_value in filter_params.items(): 
          
          item_value = item[key]

          # si la valeur est une liste : on caste en string ses membres
          if isinstance(filter_value, list):
              filter_value = [str(val) for val in filter_value]
          # sinon c'est un tableau à une valeur qu'on caste en string
          else:
              filter_value = [str(filter_value)]
          # à partir de là, filter_value est une liste de strings

          #si la ligne a un attribut qui fait partie des valeurs acceptées par le filtre => on examine les autres filtres 
          if item_value not in filter_value:
              is_valid = False
              break
      if is_valid is True:
        results.append(item)
    return results
    
  def get_departures_details(self, **kwargs):
    """
    Synopsis:
    Retourne le détail des *voyages* au départ des points situés dans le voisinage (voir paramètre radius) du point requêté.
    ---
    Paramètres de requête généraux (la valeur entre *étoiles* est la valeur par défaut si le paramètre de requête n'est pas défini):

    * params : *all* | liste de noms longs des attributs (e.g. 'params=id,departure,destination')
    * format : *json* | csv # format de la réponse
    * shortenfields : true | *false* # permet de raccourcir les noms des attributs et donc d'alléger la taille du JSON téléchargé.
    * both_to : true | *false* # permet de récupérer les données concernant l'arrivée d'un voyage en plus des données du départ (données par défaut). 
    * date : YYYY | *1787* # pour filtrer les données sur une année donnée. L'année de la date d'arrivée ou de la date de départ doit commencer par ces 4 digits : 1787 ou  1789 par exemple. Exemple : http://data.portic.fr/api/pointcalls/?format=json&date=1789
    * zipped : true | *false*

    Paramètres de requête spécifiques :

    * lon: float | # longitude du centre de la zone à requêter
    * lat: float | # latitude du centre de la zone à requêter
    * radius: *100* | int # rayon en kilomètres
    """
    response = self.api('/details/departures', params=kwargs)
    return response
    
  def get_destinations_aggregated(self, **kwargs):
    """
    Synopsis:
    Retourne une agrégation des *voyages* à l'arrivée des points situés dans le voisinage (voir paramètre radius) du point requêté.
    ---
    Paramètres de requête généraux (la valeur entre *étoiles* est la valeur par défaut si le paramètre de requête n'est pas défini):

    * params : *all* | liste de noms longs des attributs (e.g. 'params=id,departure,destination')
    * format : *json* | csv # format de la réponse
    * shortenfields : true | *false* # permet de raccourcir les noms des attributs et donc d'alléger la taille du JSON téléchargé.
    * both_to : true | *false* # permet de récupérer les données concernant l'arrivée d'un voyage en plus des données du départ (données par défaut). 
    * date : YYYY | *1787* # pour filtrer les données sur une année donnée. L'année de la date d'arrivée ou de la date de départ doit commencer par ces 4 digits : 1787 ou  1789 par exemple. Exemple : http://data.portic.fr/api/pointcalls/?format=json&date=1789
    * zipped : true | *false*

    Paramètres de requête spécifiques :

    * lon: float | # longitude du centre de la zone à requêter
    * lat: float | # latitude du centre de la zone à requêter
    * radius: *100* | int # rayon en kilomètres
    """
    response = self.api('/agg/destinations', params=kwargs)
    return response

  def get_ports(self, **kwargs):
    """
    Synopsis:
    Retourne une liste de *ports_points* au format JSON
    ---
    Paramètres de requête généraux (la valeur entre *étoiles* est la valeur par défaut si le paramètre de requête n'est pas défini):

    * params : *all* | liste de noms longs des attributs (e.g. 'params=id,departure,destination')
    * format : *json* | csv # format de la réponse
    * shortenfields : true | *false* # permet de raccourcir les noms des attributs et donc d'alléger la taille du JSON téléchargé.
    * both_to : true | *false* # permet de récupérer les données concernant l'arrivée d'un voyage en plus des données du départ (données par défaut). 
    * date : YYYY | *1787* # pour filtrer les données sur une année donnée. L'année de la date d'arrivée ou de la date de départ doit commencer par ces 4 digits : 1787 ou  1789 par exemple. Exemple : http://data.portic.fr/api/pointcalls/?format=json&date=1789
    * zipped : true | *false*

    Paramètres de requête spécifiques :

    * srid: [int] # Identifiant de référence spatiale unique associé à un système de coordonnées, une tolérance et une résolution spécifiques.
    """
    response = self.api('/ports', params=kwargs)
    return response
