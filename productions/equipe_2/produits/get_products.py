#!/usr/bin/env python

import os
import sys
import csv
import json
from collections import Counter, defaultdict
import networkx as nx
from slugify import slugify
from poitousprint import Portic, get_pointcalls_commodity_purposes_as_toflit_product


def get_navigo_pointcalls(admiralties, year, clear_cache=False):
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
    return pointcalls


def get_products(admiralties, year, filter_only_out=True, clear_cache=False):
    pointcalls = get_navigo_pointcalls(admiralties, year, clear_cache=clear_cache)

    boats = defaultdict(Counter)
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
    emptiness = defaultdict(list)

    for idx, (key, toflit_classif) in enumerate(toflit_classifications):
        print('WORKING on PORTIC data for admiralties "%s" in %s with TOFLIT classification "%s"' % (", ".join(admiralties), year, toflit_classif))

        missing = Counter()

        for pc in get_pointcalls_commodity_purposes_as_toflit_product(pointcalls, product_classification=toflit_classif):
            if filter_only_out and pc["pointcall_action"].lower() != "out":
                continue

            port = pc["toponyme_fr"]
            empties = 0
            boat_classif = "Charg??"

            for c in pc["commodity_purposes"]:
                check = c["commodity_purpose"].lower()
                if not idx:
                    products["portic_default"][port][c["commodity_purpose"]] += 1
                    products["portic_standardized_fr"][port][c["commodity_standardized_fr"]] += 1
                elif key == "toflit_aggregate":
                    if check in ['vide', 'vuide', '?? vide', 'a vide', 'a vuide']:
                        products["lest_vide_aggregate"][port]["Vide"] += 1
                        empties += 1
                        boat_classif = "Vide"
                    elif check in ['lest', 'son lest', 'a son lest', 'sur son lest', 'sur lest', 'au lest', 'en lest', 'les [lest]']:
                        products["lest_vide_aggregate"][port]["Lest"] += 1
                        boat_classif = "Lest"
                    elif not c["commodity_as_toflit"]:
                        if "p??che" in check:
                            products["lest_vide_aggregate"][port]["P??che"] += 1
                    else:
                        products["lest_vide_aggregate"][port][c["commodity_as_toflit"]] += 1
                if not c["commodity_as_toflit"]:
                    missing[(c["commodity_purpose"], c["commodity_standardized_fr"], port)] += 1
                    if key == "SITC_fr":
                        products[key][port]["Divers m??lang??s"] += 1
                    elif "p??che" in check and key == "toflit_aggregate":
                        products[key][port]["P??che"] += 1
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
                if key == "toflit_aggregate":
                    boat_classif = "Cargaison inconnue"
                    products["lest_vide_aggregate"][port]["Cargaison inconnue"] += 1

            if key == "toflit_aggregate":
                emptiness[(empties, len(pc["commodity_purposes"]))].append([c["commodity_purpose"] for c in pc["commodity_purposes"]])
                boats[port][boat_classif] += 1

        if missing:
            print (' WARNING: some products could not be classified within %s:' % toflit_classif, file=sys.stderr)
            for (c1, c2, port), count in missing.items():
                print('  - "%s" / "%s" (%s times) for port %s' % (c1, c2, count, port), file=sys.stderr)

    # TODO : add a boat classification being the main product coming from a harbor

    return products, emptiness, boats


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


def write_boats_csv(boats, year, filter_only_out=True):
    filtered = "_only_out" if filter_only_out else ""
    with open(os.path.join(DATADIR, "boats_lest_vide_%s%s.csv" % (year, filtered)), "w", newline='') as csvf:
        writer = csv.writer(csvf, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['port', 'product', 'count', 'year'])
        for port, elements in sorted(boats.items()):
            for product, count in sorted(elements.items()):
                writer.writerow([port, product, count, year])


def build_bipartite_networks(products, year, filter_only_out=True):
    filtered = "_only_out" if filter_only_out else ""
    filename = os.path.join(NETWORKSDIR, "%s_%s%s.gexf" % ("%s", year, filtered))
    for classif, ports in sorted(products.items()):
        G = nx.Graph()
        for port, elements in sorted(ports.items()):
            if not G.has_node(port):
                G.add_node(port, type="port", pointcalls=0)
            for product, count in sorted(elements.items()):
                if not G.has_node(product):
                    G.add_node(product, type="product", pointcalls=0)
                G.nodes[port]['pointcalls'] += count
                G.nodes[product]['pointcalls'] += count
                if not G.has_edge(port, product):
                    G.add_edge(port, product, weight=0)
                G[port][product]['weight'] += count
        nx.write_gexf(G, filename % classif)


if __name__ == "__main__":
    admiralties = ["La Rochelle", "Marennes", "Sables-d???Olonne"]

    clear_cache = False
    if "--clear-cache" in sys.argv:
        clear_cache = True
        sys.argv.remove("--clear-cache")

    empty_stats = False
    if "--stats-empty" in sys.argv:
        empty_stats = True
        sys.argv.remove("--stats-empty")

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

    products, emptiness, boats = get_products(admiralties, year, filter_only_out=filter_only_out, clear_cache=clear_cache)
    write_products_csv_by_classification(products, year, filter_only_out=filter_only_out)
    write_boats_csv(boats, year, filter_only_out=filter_only_out)
    build_bipartite_networks(products, year, filter_only_out)

    if empty_stats:
        print("Stats on emptiness;")
        for (empties, total), pcs in emptiness.items():
            print("- %s empties / %s declared (%s boats)" % (empties, total, len(pcs)))
            if empties > 1 or (empties and empties != total):
                stats = Counter()
                for boat in sorted(pcs):
                    stats[" / ".join(boat)] += 1
                for content, count in stats.items():
                    print("  -> %s (%s boats)" % (content, count))

