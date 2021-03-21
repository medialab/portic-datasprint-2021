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