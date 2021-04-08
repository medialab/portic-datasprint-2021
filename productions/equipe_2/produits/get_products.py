#!/usr/bin/env python

import os
import sys
import csv
import json
from collections import Counter, defaultdict
import networkx as nx
from slugify import slugify
from poitousprint import Portic, get_pointcalls_commodity_purposes_as_toflit_product


def get_navigo_products(admiralties, year, filter_only_out=True, clear_cache=False):
    cachedata = os.path.join(CACHEDIR, "portic_pointcalls_%s_%s.json" % (year, "_".join([slugify(a) for a in sorted(admiralties)])))
    try:
        if clear_cache:
            raise
        with open(cachedata) as f:
            pointcalls = json.load(f)
            print('USING cached data from PORTIC for admiralties "%s" in %s' % (", ".join(admiralties), year))
    except:
        print('DOWNLOADING PORTIC data for admiralties "%s" in %s' % (", ".join(admiralties), year))
        portic = Portic()
        pointcalls = portic.get_pointcalls(year=year, pointcall_admiralty=admiralties)
        with open(cachedata, "w") as f:
            json.dump(pointcalls, f)

    products = {
        "portic_default": defaultdict(Counter),
        "portic_standardized_fr": defaultdict(Counter),
        "toflit_simplification": defaultdict(Counter),
        "toflit_revolution": defaultdict(Counter),
        "toflit_aggregate": defaultdict(Counter),
        "SITC_fr": defaultdict(Counter),
        "lest_vide_aggregate": defaultdict(Counter)
    }
    toflit_classifications = [
        ("toflit_simplification", "product_simplification"),
        ("toflit_revolution", "product_revolutionempire"),
        ("toflit_aggregate", "product_RE_aggregate"),
        ("SITC_fr", "product_sitc_FR")
    ]

    for idx, (key, toflit_classif) in enumerate(toflit_classifications):
        print('WORKING on PORTIC data for admiralties "%s" in %s with TOFLIT classification "%s"' % (", ".join(admiralties), year, toflit_classif))

        missing = Counter()

        for pc in get_pointcalls_commodity_purposes_as_toflit_product(pointcalls, product_classification=toflit_classif):
            if filter_only_out and pc["pointcall_action"].lower() != "out":
                continue

            port = pc["toponyme_fr"]

            for c in pc["commodity_purposes"]:
                if not idx:
                    products["portic_default"][port][c["commodity_purpose"]] += 1
                    products["portic_standardized_fr"][port][c["commodity_standardized_fr"]] += 1
                    if key == "toflit_aggregate":
                        if c["commodity_purpose"] in ['Vide', 'Vuide', 'À vide', 'A vide', 'A vuide']:
                            products["lest_vide_aggregate"][port]["Vide"] += 1
                        elif c["commodity_purpose"] in ['A son lest', 'Au lest', 'Son lest', 'Sur lest', 'Sur son lest']:
                            products["lest_vide_aggregate"][port]["Lest"] += 1
                        else:
                            products["lest_vide_aggregate"][port][c["commodity_purpose"]] += 1
                if not c["commodity_as_toflit"]:
                    missing[(c["commodity_purpose"], c["commodity_standardized_fr"], port)] += 1
                    if key == "SITC_fr":
                        products[key][port]["Divers mélangés"] += 1
                    elif "pêche" in c["commodity_purpose"].lower() and key == "toflit_aggregate":
                        products[key][port]["Pêche"] += 1
                    else:
                        # Ignore rare missing cases (concerns 2 or 3 lines per classif, mostly Bois & Canons)
                        pass
                else:
                    products[key][port][c["commodity_as_toflit"]] += 1

            # Handle cases with no commodity declared as unknown content
            if not len(pc["commodity_purposes"]):
                if not idx:
                    products["portic_default"][port]["Cargaison inconnue"] += 1
                    products["portic_standardized_fr"][port]["Cargaison inconnue"] += 1
                products[key][port]["Cargaison inconnue"] += 1

        if missing:
            print (' WARNING: some products could not be classified within %s:' % toflit_classif, file=sys.stderr)
            for (c1, c2, port), count in missing.items():
                print('  - "%s" / "%s" (%s times) for port %s' % (c1, c2, count, port), file=sys.stderr)

    return products


def write_products_csv_by_classification(products, year, filter_only_out=True):
    filtered = "_only_out" if filter_only_out else ""
    with open(os.path.join(DATADIR, "all_classifications_%s%s.csv" % (year, filtered)), "w", newline='') as csvall:
        writerall = csv.writer(csvall, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writerall.writerow(['port', 'product', 'count', 'year', 'classification'])
        for classif, ports in sorted(products.items()):
            with open(os.path.join(DATADIR, "%s_%s%s.csv" % (classif, year, filtered)), "w", newline='') as csvone:
                writerone = csv.writer(csvone, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                writerone.writerow(['port', 'product', 'count', 'year', 'classification'])
                for port, elements in sorted(ports.items()):
                    for product, count in sorted(elements.items()):
                        writerall.writerow([port, product, count, year, classif])
                        writerone.writerow([port, product, count, year, classif])


def build_bipartite_networks(products, year, filter_only_out=True):
    filtered = "_only_out" if filter_only_out else ""
    filename = os.path.join(NETWORKSDIR, "%s_%s%s.gexf" % ("%s", year, filtered))
    for classif, ports in sorted(products.items()):
        G = nx.Graph()
        for port, elements in sorted(ports.items()):
            if not G.has_node(port):
                G.add_node(port, nature="port", pointcalls=0)
            for product, count in sorted(elements.items()):
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

    clear_cache = False
    if "--clear-cache" in sys.argv:
        clear_cache = True
        sys.argv.remove("--clear-cache")

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

    products = get_navigo_products(admiralties, year, filter_only_out=filter_only_out, clear_cache=clear_cache)
    write_products_csv_by_classification(products, year, filter_only_out=filter_only_out)
    build_bipartite_networks(products, year, filter_only_out)

