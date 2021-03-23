
import networkx as nx
import requests
import csv
from poitousprint import Toflit

toflit_client = Toflit()

def nest_toflit18_flow(flow):
  """
  Cette information organise un flux toflit18 tel que reçu depuis les données en csv
  sous la forme d'un ensemble d'un ensemble de clés thématiques qui contiennent chacun les propriétés correspondantes.
  """
  model = {
    "flow": [
      "year",
      "export_import"
    ],
    "source": [
      "source_type",
      "best_guess_national_prodxpart",
      "best_guess_national_partner",
      "best_guess_national_product",
      "best_guess_region_prodxpart",
      "best_guess_national_region",
      "nbr_obs",
      "imprimatur",
      "filepath",
      "source",
      "sheet"
    ],
    "product_origin": [
      "origin",
      "origin_origin",
      "customs_region_origin",
      "details_provenance"
    ],
    "product_quantity_and_value": [
      "value",
      "quantity",
      "computed_value",
      "value_as_reported",
      "computed_value_per_unit",
      "computed_quantity",
      "value_minus_unit_val_x_qty",
      "quantities_metric",
      "unit_price_metric",
      "conv_simplification_to_metric",
      "quantity_unit_metric",
      "quantity_unit_simplification",
      "value_minus_un_source",
      "value_total",
      "value_sub_total_1",
      "value_sub_total_2",
      "value_sub_total_3",
      "quantity_unit",
      "quantity_unit_orthographic",
      "value_per_unit"
    ],
    "product_denomination": [
      "product",
      "product_orthographic",
      "product_simplification",
      "product_sitc",
      "peche",
      "product_medicinales",
      "product_RE_aggregate",
      "product_threesectors",
      "product_threesectorsM",
      "product_hamburg",
      "product_canada",
      "product_edentreaty",
      "product_grains",
      "product_coton",
      "product_ulrich",
      "product_coffee",
      "product_porcelaine",
      "product_v_glass_beads",
      "product_revolutionempire",
      "product_beaver",
      "product_type_textile",
      "product_luxe_dans_type",
      "product_luxe_dans_SITC",
      "product_sitc_FR",
      "product_sitc_EN",
      "product_sitc_simplEN",
    ],
    "partner": [
      "partner",
      "partner_orthographic",
      "partner_simplification",
      "partner_grouping",
      "partner_obrien",
      "partner_sourcename",
      "partner_wars",
      "partner_africa"
    ],
    "localization": {
      "customs_region_grouping",
      "customs_region",
      "customs_office"
    },
    "duty": [
      "duty_quantity",
      "duty_quantity_unit",
      "duty_by_unit",
      "duty_total",
      "duty_part_of_bundle",
      "duty_remarks"
    ],
    "other_props": [
      "line_number",
      "needs_more_details",
      "absurd_observation",
      "obsolete"
    ]
  }
  output = {}
  for key, props in model.items():
    output[key] = {}
    for column in props:
      output[key][column] = flow[column]

  return output


def nest_portic_pointcall(pointcall):
  """
  Cette information organise un pointcall portic tel que reçu depuis les données en csv
  sous la forme d'un ensemble d'un ensemble de clés thématiques qui contiennent chacun les propriétés correspondantes.
  """
  model = {
    "source": [
      "source_doc_id",
      "source_text",
      "source_suite",
      "source_component",
      "source_number",
      "source_other",
      "source_main_port_uhgs_id",
      "source_main_port_toponyme",
      "source_subset",
      "navigo_status",
      "source_1787_available",
      "source_1789_available",
      "record_id",
    ],
    "pointcall_dates": [
      "pointcall_in_date",
      "pointcall_out_date",
      "date_fixed",
      "pointcall_outdate_uncertainity",
      "outdate_fixed",
      "indate_fixed",
      "pointcall_in_date2",
      "pointcall_out_date2",
    ],
    "pointcall_localization": [
      "pkid",
      "pointcall",
      "pointcall_uhgs_id",
      "toponyme_fr",
      "toponyme_en",
      "latitude",
      "longitude",
      "pointcall_admiralty",
      "pointcall_province",
      "pointcall_states",
      "pointcall_substates",
      "pointcall_states_en",
      "pointcall_substates_en",
      "state_1789_fr",
      "state_1789_en",
      "substate_1789_fr",
      "substate_1789_en",
      "pointcall_point",
      "ferme_direction",
      "ferme_bureau",
      "ferme_bureau_uncertainty",
      "partner_balance_1789",
      'partner_balance_supp_1789',
      'partner_balance_1789_uncertainty',
      'partner_balance_supp_1789_uncertainty',
      'shiparea',
      'pointcall_status'
    ],
    "pointcall_characteristics": [
      "pointcall_action",
      "pointcall_uncertainity",
      "data_block_leader_marker",
      "pointcall_function"
    ],
    "ship_characteristics": [
      "ship_name",
      "ship_id",
      "tonnage",
      "tonnage_unit",
      "flag",
      "class",
      "ship_flag_id",
      "in_crew",
      "ship_flag_standardized_fr",
      "ship_flag_standardized_en",
      "flag_uncertainity",
      "tonnage_uncertainity",
      "ship_uncertainity"
    ],
    "ship_captain": [
      "captain_uncertainity",
      "shipclass_uncertainity",
      "citizenship_uncertainity",
      "birthplace_uhgs_id",
      "birthplace_uhgs_id_uncertainity",
      "birthplace_uncertainity",
      "captain_id",
      "captain_name",
      "birthplace",
      "status",
      "citizenship"
    ],
    "ship_homeport": [
      "homeport_uncertainity",
      "homeport",
      "homeport_uhgs_id",
      "homeport_toponyme_fr",
      "homeport_toponyme_en",
      "homeport_latitude",
      "homeport_longitude",
      "homeport_admiralty",
      "homeport_province",
      "homeport_states",
      "homeport_substates",
      "homeport_states_en",
      "homeport_substates_en",
      "homeport_state_1789_fr",
      "homeport_state_1789_en",
      "homeport_substate_1789_fr",
      "homeport_substate_1789_en",
      "homeport_source_1787_available",
      "homeport_source_1789_available",
      "homeport_status",
      "homeport_shiparea",
      "homeport_point",
      "homeport_ferme_direction",
      "homeport_ferme_bureau",
      "homeport_ferme_bureau_uncertainty",
      "homeport_partner_balance_1789",
      "homeport_partner_balance_supp_1789",
      "homeport_partner_balance_1789_uncertainty",
      "homeport_partner_balance_supp_1789_uncertainty",
    ],
    "purpose_and_cargo": [
      "cargo_uncertainity",
      "all_cargos"
    ],
    "tax": [
      "taxe_uncertainity",
      "all_taxes",
      "q01",
      "q01_u",
      "q02",
      "q02_u",
      "q03",
      "q03_u",
      "tax_concept",
      "payment_date",
    ],
    "other": [
      "pointcall_rankfull",
      "net_route_marker"
    ]
  }
  output = {}
  for key, props in model.items():
    output[key] = {}
    for column in props:
      output[key][column] = pointcall[column]

  output["commodity_purposes"] = []
  suffixes = ['', '2', '3', '4']
  for suffix in suffixes:
    commodity_purpose = 'commodity_purpose' + suffix
    commodity_standardized = 'commodity_standardized' + suffix
    commodity_standardized_fr = 'commodity_standardized' + suffix + '_fr'
    commodity_permanent_coding = 'commodity_permanent_coding' + suffix
    commodity_id = 'commodity_id' + suffix
    quantity = 'quantity' + suffix
    quantity_u = 'quantity_u' + suffix
    print('test', commodity_purpose, 'val:', pointcall[commodity_purpose])
    if commodity_purpose in pointcall and pointcall[commodity_purpose] is not None:
      purpose = {
        "commodity_purpose": pointcall[commodity_purpose] if commodity_purpose in pointcall else None,
        "commodity_standardized": pointcall[commodity_standardized] if commodity_standardized in pointcall else None,
        "commodity_standardized_fr": pointcall[commodity_standardized_fr] if commodity_standardized_fr in pointcall else None,
        "commodity_permanent_coding": pointcall[commodity_permanent_coding] if commodity_permanent_coding in pointcall else None,
        "commodity_id": pointcall[commodity_id] if commodity_id in pointcall else None,
        "quantity": pointcall[quantity] if quantity in pointcall else None,
        "quantity_u": pointcall[quantity_u] if quantity_u in pointcall else None
      }
      output["commodity_purposes"].append(purpose)

  return output



def build_cooccurence_graph(data, key_1, key_2, **kwargs):
    """
    Cette fonction prend un ensemble de dict et deux noms de clés.
    Elle renvoie un graphe networkx de coocurrence entre les dicts
    """
    # créer un graphe
    Graph = nx.Graph()

    # créer des dict pour les deux types de noeuds et les liens
    key1_uniq = {}
    key2_uniq = {}
    edges_uniq = {}
    default_params = {
        "color_1": "rgb(0, 255, 0)",
        "color_2": "rgb(255, 0, 0)",
        "node_min_size": 1,
        "node_max_size": 10
    }
    params = {
        *default_params,
        *kwargs
    }
    
    # remplir les dicts
    for datum in data:
        if key_1 in datum and key_2 in datum:
            value_1 = datum[key_1] if datum[key_1] is not None else "undefined"
            value_2 = datum[key_2] if datum[key_2] is not None else "undefined"
            value_1_id = key_1 + "_" + value_1
            value_2_id = key_2 + "_" + value_2
            if value_1_id in key1_uniq:
                key1_uniq[value_1_id] = {**key1_uniq[value_1_id], "size": key1_uniq[value_1_id]["size"] + 1}
            else:
               key1_uniq[value_1_id] = {
                   "type": key_1, 
                   "name": value_1, 
                   "color": params["color_1"],
                   "size": 1
               }
            if value_2_id in key2_uniq:
                key2_uniq[value_2_id] = {**key2_uniq[value_2_id], "size": key2_uniq[value_2_id]["size"] + 1}
            else:
               key2_uniq[value_2_id] = {
                   "type": key_2, 
                   "name": value_2, 
                   "color": params["color_2"],
                   "size": 1
               }
            edge_footprint = value_1_id + "-" + value_2_id
            if edge_footprint in edges_uniq:
                edges_uniq[edge_footprint]["weight"] += 1
            else:
                edges_uniq[edge_footprint] = {
                    "source": value_1_id,
                    "target": value_2_id,
                    "weight": 1
                }
    # concaténer les deux dicts de noeuds en un seul
    all_nodes = key1_uniq
    all_nodes.update(key2_uniq)
    # applatir et formatter les noeuds
    nodes = []
    for key, node in all_nodes.items():
        nodes.append((key, node))
    edges = []

    for key, edge in edges_uniq.items():
        edges.append((edge["source"], edge["target"], {"weight": edge["weight"]}))
        
    # ajuster la taille des noeuds en fonction d'un min et d'un max donnés
    domain_min_nodes_size = min([node[1]['size'] for node in nodes])
    domain_max_nodes_size = max([node[1]['size'] for node in nodes])
    range_in_nodes_size = [params["node_min_size"], params["node_max_size"]]
    nodes_size_mapping_params = [domain_min_nodes_size, domain_max_nodes_size, *range_in_nodes_size]

    for node in nodes:
        node[1]["size"] = map_value(node[1]["size"], *nodes_size_mapping_params)
        node[1]["label"] = node[1]["name"]


    Graph.add_nodes_from(nodes)
    Graph.add_edges_from(edges)

    return Graph

def get_online_csv(url):
  """
  Cette fonction permet de récupérer le contenu d'un csv en ligne.
  Pour les google spreadsheets: fichier > publier sur le web > format csv > copier le lien
  """
  results = []
  with requests.Session() as s:
      download = s.get(url)
      decoded_content = download.content.decode('utf-8')
      reader = csv.DictReader(decoded_content.splitlines(), delimiter=',')
      for row in reader:
        results.append(row)
  return results


def build_toflit18_classif_multimap(classification="product_simplification"):
  classification_type = classification.split('_')[0]
  # construire le chemin vers la classification visée à partir de source
  current_classification_id = classification_type + '_source'
  # récupérer l'arborescence des classifications TOFLIT18
  current_classification = None
  if classification_type == 'product':
    current_classification = toflit_client.get_product_classifications()
  else:
    current_classification = toflit_client.get_partner_classifications()

  # construire le chemin à parcourir dans les classifications depuis source vers la classification cible
  classification_path = []
  while current_classification_id != classification:
    children = current_classification['children']
    if len(children) == 1:
      current_classification = children[0]
    for child in children:
      if child['id'] == classification:
        current_classification = child
        break
    current_classification_id = current_classification['id']
    classification_path.append(current_classification_id)
  # créer un dict dont chaque clé sera une des classifications à parcourir,
  # et chaque valeur un dict dont les clés sont les formes parentes et les valeurs les formes enfant
  classif_multi_dict = {}
  prev_classif = classification_type + '_source'
  for classif in classification_path:
    classif_multi_dict[classif] = {}
    # on créée un dict alternatif avec les valeurs en lowercase pour parer à d'éventuels problèmes liés à la casse
    classif_multi_dict[classif + '_lower'] = {}
    # récupérer le csv à jour de la classification sur le repo toflit18_data
    toflit18_csv_url = 'https://raw.githubusercontent.com/medialab/toflit18_data/master/base/classification_' + classif + '.csv'
    # télécharger le csv depuis toflit18_data
    classif_data = get_online_csv(toflit18_csv_url)
    prev_key = prev_classif.split(classification_type + '_')[1]
    current_key = classif.split(classification_type + '_')[1]
    for row in classif_data:
      # nom de la classification "parent" : e.g. "orthographic"
      parent_value = row[prev_key]
      # nom de la classification "enfant" : e.g. "simplification"
      child_value = row[current_key]
      classif_multi_dict[classif][parent_value] = child_value
      # gérer les problèmes de casse en stockant dans le dict alternatif la valeur originale et la valeur en lower
      classif_multi_dict[classif + '_lower'][parent_value.lower()] = {
        "original": child_value,
        "lower" : child_value.lower()
      }
    prev_classif = classif
  return (classification_path, classif_multi_dict)

def get_pointcalls_commodity_purposes_as_toflit_product(pointcalls, product_classification="product_simplification"):
  """
  Cette fonction prend en entrée une liste de pointcalls et un nom de classification
  Elle renvoie en sortie la liste des dict de pointcalls enrichis avec une propriété "commodity_purposes"
  qui ont les propriétés existantes de PORTIC pour commodity_purpose[2,3,4] + une propriété "commodity_as_toflit qui donne la valeur correspondante dans toflit18.
  """
  # créer un dict dont chaque clé sera une des classifications à parcourir,
  # et chaque valeur un dict dont les clés sont les formes parentes et les valeurs les formes enfant
  classification_path, classif_multi_dict = build_toflit18_classif_multimap(product_classification)
  prev_classif = 'product_source'
  for classif in classification_path:
    classif_multi_dict[classif] = {}
    # on créée un dict alternatif avec les valeurs en lowercase pour parer à d'éventuels problèmes liés à la casse
    classif_multi_dict[classif + '_lower'] = {}
    # récupérer le csv à jour de la classification sur le repo toflit18_data
    toflit18_csv_url = 'https://raw.githubusercontent.com/medialab/toflit18_data/master/base/classification_' + classif + '.csv'
    # télécharger le csv depuis toflit18_data
    classif_data = get_online_csv(toflit18_csv_url)
    prev_key = prev_classif.split('product_')[1]
    current_key = classif.split('product_')[1]
    for row in classif_data:
      # nom de la classification "parent" : e.g. "orthographic"
      parent_value = row[prev_key]
      # nom de la classification "enfant" : e.g. "simplification"
      child_value = row[current_key]
      classif_multi_dict[classif][parent_value] = child_value
      # gérer les problèmes de casse en stockant dans le dict alternatif la valeur originale et la valeur en lower
      classif_multi_dict[classif + '_lower'][parent_value.lower()] = {
        "original": child_value,
        "lower" : child_value.lower()
      }
    prev_classif = classif

  # créer une fonction de mapping qui transforme les pointcalls en leur ajoutant une propriété "commodity_purposes"
  def enrich_pointcall(pointcall):
    # cette liste contiendra tous les commodity_purpose[2,3,4] transformés et enrichis avec leur forme toflit18
    # dans la classification visée
    purposes = []
    # on itère dans commodity_purpose['2,3,4]
    suffixes = ['', '2', '3', '4']
    for suffix in suffixes:
      # on génère les propriétés PORTIC correspondant à chaque suffixe pour décrire les commodity_purposes multiples
      commodity_purpose = 'commodity_purpose' + suffix
      commodity_standardized = 'commodity_standardized' + suffix
      commodity_standardized_fr = 'commodity_standardized' + suffix + '_fr'
      commodity_permanent_coding = 'commodity_permanent_coding' + suffix
      commodity_id = 'commodity_id' + suffix
      quantity = 'quantity' + suffix
      quantity_u = 'quantity_u' + suffix
      # la valeur PORTIC commodity_purpose correspond au niveau "source" des classifications TOFLIT18
      source_name = pointcall[commodity_purpose]
      translated_name = None
      if source_name is not None:
        # on stocke dans une valeur courante la traduction TOFLIT18 (qui va par exemple correspondre successivement à source -> orthographic -> simplification)
        translated_name = source_name
        # parcourir les classifs pour trouver la bonne valeur
        for classif in classification_path:
          # si la valeur est dans le dict de la classif toflit18 courante on le traduit
          if translated_name is not None and translated_name in classif_multi_dict[classif]:
            translated_name = classif_multi_dict[classif][translated_name]
          # si la valeur matche en lowercase on la traduit aussi
          elif translated_name is not None and translated_name.lower() in classif_multi_dict[classif + '_lower']:
            translated_name = classif_multi_dict[classif + '_lower'][translated_name.lower()]["original"]
          # si pas de valeur trouvée => alignement impossible, besoin de màj côté toflit18 pour intégrer cette forme
          else:
            translated_name = None
      # formalisation d'un dict avec les infos portic+toflit18
      if commodity_purpose in pointcall and pointcall[commodity_purpose] is not None:
        purpose = {
          # cette valeur est celle qui permet l'alignement
          "commodity_as_toflit": translated_name,
          # les valeurs suivantes sont les valeurs originales du pointcall
          "commodity_purpose": pointcall[commodity_purpose] if commodity_purpose in pointcall else None,
          "commodity_standardized": pointcall[commodity_standardized] if commodity_standardized in pointcall else None,
          "commodity_standardized_fr": pointcall[commodity_standardized_fr] if commodity_standardized_fr in pointcall else None,
          "commodity_permanent_coding": pointcall[commodity_permanent_coding] if commodity_permanent_coding in pointcall else None,
          "commodity_id": pointcall[commodity_id] if commodity_id in pointcall else None,
          "quantity": pointcall[quantity] if quantity in pointcall else None,
          "quantity_u": pointcall[quantity_u] if quantity_u in pointcall else None
        }
        purposes.append(purpose)
    # on ajoute au pointcall une nouvelle propriété "commodity_purposes" (noter le S à la fin ;))
    pointcall["commodity_purposes"] = purposes
    return pointcall
  # on transforme tous les pointcalls donnés en argument
  return [enrich_pointcall(pointcall) for pointcall in pointcalls]

def get_pointcalls_port_as_toflit_partner(pointcalls, partner_classification="partner_simplification"):
  """
  Cette fonction prend en entrée une liste de pointcalls et un nom de classification de partenaire
  Elle renvoie en sortie la liste des dict de pointcalls enrichis avec une propriété "pointcall_as_toflit_partner"
  """
  # créer un dict dont chaque clé sera une des classifications à parcourir,
  # et chaque valeur un dict dont les clés sont les formes parentes et les valeurs les formes enfant
  classification_path, classif_multi_dict = build_toflit18_classif_multimap(partner_classification)
  prev_classif = 'partner_source'
  for classif in classification_path:
    classif_multi_dict[classif] = {}
    # on créée un dict alternatif avec les valeurs en lowercase pour parer à d'éventuels problèmes liés à la casse
    classif_multi_dict[classif + '_lower'] = {}
    # récupérer le csv à jour de la classification sur le repo toflit18_data
    toflit18_csv_url = 'https://raw.githubusercontent.com/medialab/toflit18_data/master/base/classification_' + classif + '.csv'
    # télécharger le csv depuis toflit18_data
    classif_data = get_online_csv(toflit18_csv_url)
    prev_key = prev_classif.split('partner_')[1]
    current_key = classif.split('partner_')[1]
    for row in classif_data:
      # nom de la classification "parent" : e.g. "orthographic"
      parent_value = row[prev_key]
      # nom de la classification "enfant" : e.g. "simplification"
      child_value = row[current_key]
      classif_multi_dict[classif][parent_value] = child_value
      # gérer les problèmes de casse en stockant dans le dict alternatif la valeur originale et la valeur en lower
      classif_multi_dict[classif + '_lower'][parent_value.lower()] = {
        "original": child_value,
        "lower" : child_value.lower()
      }
    prev_classif = classif

  # créer une fonction de mapping qui transforme les pointcalls en leur ajoutant une propriété "partner_as_toflit"
  def enrich_pointcall(pointcall):
    pointcall['pointcall_as_toflit_partner'] = None
    partner = pointcall['partner_balance_1789']
    if partner is None:
      partner = pointcall['partner_balance_supp_1789']
    if partner is not None:
      # la valeur partner correspond au niveau "source" des classifications TOFLIT18
      translated_name = None
      if partner is not None:
        # on stocke dans une valeur courante la traduction TOFLIT18 (qui va par exemple correspondre successivement à source -> orthographic -> simplification)
        translated_name = partner
        # parcourir les classifs pour trouver la bonne valeur
        for classif in classification_path:
          # si la valeur est dans le dict de la classif toflit18 courante on le traduit
          if translated_name is not None and translated_name in classif_multi_dict[classif]:
            translated_name = classif_multi_dict[classif][translated_name]
          # si la valeur matche en lowercase on la traduit aussi
          elif translated_name is not None and translated_name.lower() in classif_multi_dict[classif + '_lower']:
            translated_name = classif_multi_dict[classif + '_lower'][translated_name.lower()]["original"]
          # si pas de valeur trouvée => alignement impossible, besoin de màj côté toflit18 pour intégrer cette forme
          else:
            translated_name = None
      if translated_name is not None:
        pointcall['pointcall_as_toflit_partner'] = translated_name
    return pointcall
  # on transforme tous les pointcalls donnés en argument
  return [enrich_pointcall(pointcall) for pointcall in pointcalls]

def get_pointcalls_homeport_as_toflit_partner(pointcalls, partner_classification="partner_simplification"):
  """
  Cette fonction prend en entrée une liste de pointcalls et un nom de classification de partenaire
  Elle renvoie en sortie la liste des dict de pointcalls enrichis avec une propriété "homeport_as_toflit_partner"
  """
  # créer un dict dont chaque clé sera une des classifications à parcourir,
  # et chaque valeur un dict dont les clés sont les formes parentes et les valeurs les formes enfant
  classification_path, classif_multi_dict = build_toflit18_classif_multimap(partner_classification)
  prev_classif = 'partner_source'
  for classif in classification_path:
    classif_multi_dict[classif] = {}
    # on créée un dict alternatif avec les valeurs en lowercase pour parer à d'éventuels problèmes liés à la casse
    classif_multi_dict[classif + '_lower'] = {}
    # récupérer le csv à jour de la classification sur le repo toflit18_data
    toflit18_csv_url = 'https://raw.githubusercontent.com/medialab/toflit18_data/master/base/classification_' + classif + '.csv'
    # télécharger le csv depuis toflit18_data
    classif_data = get_online_csv(toflit18_csv_url)
    prev_key = prev_classif.split('partner_')[1]
    current_key = classif.split('partner_')[1]
    for row in classif_data:
      # nom de la classification "parent" : e.g. "orthographic"
      parent_value = row[prev_key]
      # nom de la classification "enfant" : e.g. "simplification"
      child_value = row[current_key]
      classif_multi_dict[classif][parent_value] = child_value
      # gérer les problèmes de casse en stockant dans le dict alternatif la valeur originale et la valeur en lower
      classif_multi_dict[classif + '_lower'][parent_value.lower()] = {
        "original": child_value,
        "lower" : child_value.lower()
      }
    prev_classif = classif

  # créer une fonction de mapping qui transforme les pointcalls en leur ajoutant une propriété "partner_as_toflit"
  def enrich_pointcall(pointcall):
    pointcall['homeport_as_toflit_partner'] = None
    partner = pointcall['homeport_partner_balance_1789']
    if partner is None:
      partner = pointcall['homeport_partner_balance_supp_1789']
    if partner is not None:
      # la valeur partner correspond au niveau "source" des classifications TOFLIT18
      translated_name = None
      if partner is not None:
        # on stocke dans une valeur courante la traduction TOFLIT18 (qui va par exemple correspondre successivement à source -> orthographic -> simplification)
        translated_name = partner
        # parcourir les classifs pour trouver la bonne valeur
        for classif in classification_path:
          # si la valeur est dans le dict de la classif toflit18 courante on le traduit
          if translated_name is not None and translated_name in classif_multi_dict[classif]:
            translated_name = classif_multi_dict[classif][translated_name]
          # si la valeur matche en lowercase on la traduit aussi
          elif translated_name is not None and translated_name.lower() in classif_multi_dict[classif + '_lower']:
            translated_name = classif_multi_dict[classif + '_lower'][translated_name.lower()]["original"]
          # si pas de valeur trouvée => alignement impossible, besoin de màj côté toflit18 pour intégrer cette forme
          else:
            translated_name = None
      if translated_name is not None:
        pointcall['homeport_as_toflit_partner'] = translated_name
    return pointcall
  # on transforme tous les pointcalls donnés en argument
  return [enrich_pointcall(pointcall) for pointcall in pointcalls]