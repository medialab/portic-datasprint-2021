
import networkx as nx

def print_classification(input, classification, displace):
    if 'name' in classification:
        input += displace + '- ' + classification['name'] + '(' + classification['slug'] + ')' + '\n'
    else:
        print('oups', classification)
    if 'children' in classification:
        input += ''.join(map(lambda c : print_classification('', c, displace + '  '), classification['children']))
    return input;

def nest_toflit18_flow(flow):
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