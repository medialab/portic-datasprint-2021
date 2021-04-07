#!/usr/bin/env python

import os
import sys
import csv
import json
from pprint import pprint
from collections import Counter, defaultdict
import networkx as nx
from slugify import slugify
from poitousprint import Portic, Toflit, get_pointcalls_commodity_purposes_as_toflit_product

portic = Portic()
#toflit = Toflit()

def get_navigo_products(admiralties, year, filter_only_out=True, products=None):
    cachedata = os.path.join(CACHEDIR, "portic_pointcalls_%s_%s.json" % (year, "_".join([slugify(a) for a in sorted(admiralties)])))
    try:
        with open(cachedata) as f:
            pointcalls = json.load(f)
            print('USING cached data from PORTIC for admiralties "%s" in %s' % (", ".join(admiralties), year))
    except:
        print('DOWNLOADING PORTIC data for admiralties "%s" in %s' % (", ".join(admiralties), year))
        pointcalls = portic.get_pointcalls(year=year, pointcall_admiralty=admiralties)
        with open(cachedata, "w") as f:
            json.dump(pointcalls, f)
    if not products:
        products = {
            "portic_default": defaultdict(Counter),
            "portic_standardized_fr": defaultdict(Counter),
            "toflit_simplification": defaultdict(Counter),
            "toflit_revolution": defaultdict(Counter),
            "toflit_aggregate": defaultdict(Counter)
        }
    toflit_classifications = [
        ("toflit_simplification", "product_simplification"),
        ("toflit_revolution", "product_revolutionempire"),
        ("toflit_aggregate", "product_RE_aggregate"),
    ]
    for idx, classif in enumerate(toflit_classifications):
        key, toflit_classif = classif
        print('WORKING on PORTIC data for admiralties "%s" in %s with TOFLIT classification "%s"' % (", ".join(admiralties), year, toflit_classif))
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
    with open(os.path.join(DATADIR, "all_classifications_%s%s.csv" % (year, filtered)), "w", newline='') as csvall:
        writerall = csv.writer(csvall, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writerall.writerow(['port', 'product', 'count', 'year', 'classification'])
        for classif, ports in products.items():
            with open(os.path.join(DATADIR, "%s_%s%s.csv" % (classif, year, filtered)), "w", newline='') as csvone:
                writerone = csv.writer(csvone, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                writerone.writerow(['port', 'product', 'count', 'year', 'classification'])
                for port, elements in ports.items():
                    for product, count in elements.items():
                        if not product:
                            continue
                        writerall.writerow([port, product, count, year, classif])
                        writerone.writerow([port, product, count, year, classif])


def build_bipartite_networks(products, year, filter_only_out=True):
    filtered = "_only_out" if filter_only_out else ""
    filename = os.path.join(NETWORKSDIR, "%s_%s%s.gexf" % ("%s", year, filtered))
    for classif, ports in products.items():
        G = nx.Graph()
        for port, elements in ports.items():
            if not G.has_node(port):
                G.add_node(port, nature="port", pointcalls=0)
            for product, count in elements.items():
                if not product:
                    continue
                if not G.has_node(product):
                    G.add_node(product, nature="product", pointcalls=0)
                G.nodes[port]['pointcalls'] += count
                G.nodes[product]['pointcalls'] += count
                if not G.has_edge(port, product):
                    G.add_edge(port, product, weight=0)
                G[port][product]['weight'] += count
        nx.write_gexf(G, filename % classif)


if __name__ == "__main__":
    admiralties = ["La Rochelle", "Marennes", "Sables-d’Olonne"]
    year = 1789
    if len(sys.argv) > 1:
        year = sys.argv[1]
    filter_only_out = True
    if len(sys.argv) > 2:
        filter_only_out = False

    CACHEDIR = ".cache"
    DATADIR = "data"
    NETWORKSDIR = "networks"
    for d in [CACHEDIR, DATADIR, NETWORKSDIR]:
        if not os.path.exists(d):
            os.makedirs(d)

    products = get_navigo_products(admiralties, year, filter_only_out=filter_only_out)
    write_products_csv_by_classification(products, year, filter_only_out=filter_only_out)
    build_bipartite_networks(products, year, filter_only_out)

