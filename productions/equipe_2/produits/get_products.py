#!/usr/bin/env python

import os
import sys
import json
from pprint import pprint
from collections import Counter, defaultdict
from poitousprint import Portic, Toflit, get_pointcalls_commodity_purposes_as_toflit_product
from slugify import slugify

portic = Portic()
#toflit = Toflit()

def get_navigo_products_by_admiralty(admiralty, year, filter_only_out=True, products=None):
    cachedata = os.path.join(CACHEDIR, "portic_pointcalls_%s_%s.json" % (year, slugify(admiralty)))
    try:
        with open(cachedata) as  f:
            pointcalls = json.load(f)
    except:
        pointcalls = portic.get_pointcalls(year=year, pointcall_admiralty=admiralty)
        with open(cachedata, "w") as f:
            json.dump(pointcalls, f)
    if not products:
        products = {
            "portic_default": defaultdict(Counter),
            "portic_standardized_fr": defaultdict(Counter),
            "toflit_simplification": defaultdict(Counter),
            "toflit_revolution": defaultdict(Counter)
        }
    toflit_classifications = [
        ("toflit_simplification", "product_simplification"),
        ("toflit_revolution", "product_revolutionempire"),
        ("toflit_aggregate", "product_RE_aggregate"),
    ]
    for idx, classif in enumerate(toflit_classifications):
        key, toflit_classif = classif
        print('WORKING on PORTIC data for admiralty "%s" in %s with TOFLIT classification "%s"' % (admiralty, year, toflit_classif))
        pointcalls_as_toflit = get_pointcalls_commodity_purposes_as_toflit_product(pointcalls, product_classification=toflit_classif)
        for pc in pointcalls_as_toflit:
            if filter_only_out and pc["pointcall_action"].lower() != "out":
                continue
            port = pc["toponyme_fr"]
            for c in pc["commodity_purposes"]:
                if not c["commodity_purpose"]:
                    continue
                if not idx:
                    products["portic_default"][port][c["commodity_purpose"]] += 1
                    products["portic_standardized_fr"][port][c["commodity_standardized_fr"]] += 1
                products[key][port][c["commodity_as_toflit"]] += 1
    return products

def write_products_csv_by_classification(products, year, filter_only_out=True):
    filtered = "_only_out" if filter_only_out else ""
    for classif, ports in products.items():
        with open(os.path.join(DATADIR, "%s_%s%s.csv" % (classif, year, filtered)), "w") as f:
            print("port,product,count,year,classification", file=f)
            for port, elements in ports.items():
                for product, count in elements.items():
                    print("%s,%s,%s,%s,%s" % (port, product, count, year, classif), file=f)


if __name__ == "__main__":
    admiralties = ["La Rochelle", "Marennes", "Sables-d'Olonnes"]
    year = 1789
    if len(sys.argv) > 1:
        year = sys.argv[1]
    filter_only_out = True

    CACHEDIR = ".cache"
    if not os.path.exists(CACHEDIR):
        os.makedirs(CACHEDIR)
    DATADIR = "data"
    if not os.path.exists(DATADIR):
        os.makedirs(DATADIR)

    products = None
    for a in admiralties:
        products = get_navigo_products_by_admiralty(a, year, filter_only_out=filter_only_out, products=products)
    write_products_csv_by_classification(products, year, filter_only_out=filter_only_out)
