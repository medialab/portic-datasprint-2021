#!/bin/bash

xsv search "Poitou|Aunis|Saintonge|Normandie|Guyenne|Flandre|Bretagne|Picardie" -s departure_province travels_1787.csv | xsv select departure_province,departure_fr,destination_fr,tonnage | sort > tonnage.csv
python process_tonnage.py
