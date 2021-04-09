import os
import csv
import sys
from collections import defaultdict, Counter

with open("data/tonnage.csv") as f:
    flows = list(csv.DictReader(f))

ports = defaultdict(set)
for f in flows:
    ports[f["departure_province"]].add(f["departure_fr"])


provinces = ["Poitou", "Aunis", "Saintonge", "Normandie", "Guyenne", "Flandre", "Bretagne", "Picardie"]
tons = {
    "externe": {},
    "local": {}
}

for f in flows:
    try:
        tonnage = int(f["tonnage"])
    except:
        continue
    destination = "externe"
    if f["destination_fr"] in ports[f["departure_province"]]:
        destination = "local"
    if f["departure_province"] not in tons[destination]:
        tons[destination][f["departure_province"]] = {}
    if f["departure_fr"] not in tons[destination][f["departure_province"]]:
        tons[destination][f["departure_province"]][f["departure_fr"]] = 0
    tons[destination][f["departure_province"]][f["departure_fr"]] += tonnage

with open(os.path.join("data", "provinces_ports_tonnage_1787.csv"), "w", newline='') as csvf:
    writer = csv.writer(csvf, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['province', 'port', 'destination', 'tonnage'])
    for destination, provinces in sorted(tons.items()):
        for province, ports in sorted(provinces.items()):
            for port, tonnage in sorted(ports.items()):
                writer.writerow([province,port,destination,tonnage])

