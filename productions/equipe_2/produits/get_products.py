#!/usr/bin/env python

import os
import sys
import json
from pprint import pprint
from collections import Counter
from poitousprint import Portic, Toflit
from slugify import slugify

portic_client = Portic()
#toflit_client = Toflit()

CACHEDIR = ".cache"
if not os.path.exists(CACHEDIR):
    os.makedirs(CACHEDIR)

def get_navigo_products_by_port(port, year):
    cachedata = os.path.join(CACHEDIR, "portic_pointcalls_%s_%s.json" % (year, slugify(port)))
    try:
        with open(cachedata) as f:
            pointcalls = json.load(f)
    except:
        pointcalls = portic_client.get_pointcalls(year=year, pointcall_admiralty=port)
        with open(cachedata, "w") as f:
            json.dump(pointcalls, f)
    products = Counter()
    products_dest = DefaultDict(set)
    standardized = Counter()
    standardized_dest = DefaultDict(set)
    for pc in pointcalls:
        products[pc["commodity_purpose"]] += 1
        products[pc["commodity_purpose2"]] += 1
        products[pc["commodity_purpose3"]] += 1
        products[pc["commodity_purpose4"]] += 1
        products_dest[pc["commodity_purpose"]].add()
        standardized[pc["commodity_standardized_fr"]] += 1
        standardized[pc["commodity_standardized2_fr"]] += 1
        standardized[pc["commodity_standardized3_fr"]] += 1
        standardized[pc["commodity_standardized4_fr"]] += 1
    if None in products:
        del(products[None])
    if None in standardized:
        del(standardized[None])
    pprint(products)
    pprint(standardized)
    print("%s product names, %s standardized" % (len(products), len(standardized)))


if __name__ == "__main__":
    # La Rochelle, Marennes, Sables-d'Olonnes
    port = "La Rochelle"
    if len(sys.argv) > 1:
        port = sys.argv[1]
    year = 1789
    if len(sys.argv) > 2:
        year = int(sys.argv[2])
    get_navigo_products_by_port(port, year)
