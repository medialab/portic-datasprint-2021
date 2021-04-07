#!/usr/bin/env python

import os
import sys
import json
from pprint import pprint
from collections import Counter
from poitousprint import Portic, Toflit, get_pointcalls_commodity_purposes_as_toflit_product
from slugify import slugify

portic = Portic()
#toflit = Toflit()

CACHEDIR = ".cache"
if not os.path.exists(CACHEDIR):
    os.makedirs(CACHEDIR)

def get_navigo_products_by_port(port, year, filter_only_out=True):
    cachedata = os.path.join(CACHEDIR, "portic_pointcalls_%s_%s.json" % (year, slugify(port)))
    try:
        with open(cachedata) as  f:
            pointcalls = json.load(f)
    except:
        pointcalls = portic.get_pointcalls(year=year, pointcall_admiralty=port)
        with open(cachedata, "w") as f:
            json.dump(pointcalls, f)
    pointcalls_as_toflit = get_pointcalls_commodity_purposes_as_toflit_product(pointcalls, product_classification='product_simplification')
    products = Counter()
    standardized = Counter()
    toflitproducts = Counter()
    for pc in pointcalls_as_toflit:
        if filter_only_out and pc["pointcall_action"].lower() != "out":
            continue
        for c in pc["commodity_purposes"]:
            if not c["commodity_purpose"]:
                continue
            products[c["commodity_purpose"]] += 1
            standardized[c["commodity_standardized_fr"]] += 1
            toflitproducts[c["commodity_as_toflit"]] += 1
    pprint(products)
    pprint(standardized)
    pprint(toflitproducts)
    print("%s product names, %s standardized, %s as toflit" % (len(products), len(standardized), len(toflitproducts)))


if __name__ == "__main__":
    # La Rochelle, Marennes, Sables-d'Olonnes
    port = "La Rochelle"
    if len(sys.argv) > 1:
        port = sys.argv[1]
    year = 1789
    if len(sys.argv) > 2:
        year = int(sys.argv[2])
    get_navigo_products_by_port(port, year)
