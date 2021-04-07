import csv

provinces_LaRochelle = []

with open("toflit18_bdd_origin.csv", "r") as f:
    origins = csv.DictReader(f)
    origins_LaRochelle = set([o["origin_norm_ortho"] for o in origins if o["province"] in [
        "Aunis", "Poitou", "Angoumois", "Saintonge"]])
    print(origins_LaRochelle)
