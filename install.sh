#!/bin/bash
echo "creating data folder"
mkdir data
echo "fetching latest toflit18 data"
curl -o toflit18_bdd.zip "https://raw.githubusercontent.com/medialab/toflit18_data/master/base/bdd%20courante.csv.zip"
unzip toflit18_bdd.zip -d "data"
rm -f toflit18_bdd.zip
mv "data/bdd courante.csv" "data/toflit18_all_flows.csv"
# créer toflit18_sprint_corpus.csv
echo "fetching latest toflit18 schema"
curl -o data/toflit18_sources_schema.json "https://raw.githubusercontent.com/medialab/toflit18_data/master/csv_sources_schema.json"
echo "fetching latest navigo pointcalls data"
curl -o data/navigo_all_pointcalls_1789.csv "data.portic.fr/api/pointcalls/?date=1789&format=csv"
echo "fetching latest navigo flows data"
curl -o data/navigo_all_flows_1789.csv "data.portic.fr/api/flows/?date=1789&format=csv"
echo "fetching latest navigo pointcalls schema"
curl -o data/portic_pointcalls_descriptions.json "http://data.portic.fr/api/fieldnames/?API=pointcalls"
echo "fetching latest navigo flows schema"
curl -o data/portic_flows_descriptions.json "http://data.portic.fr/api/fieldnames/?API=travels"
echo "installing python dependencies"
pip install -U pip
pip install -e lib
pip install -r requirements.txt
echo "preparing derivated datasets"
python prepare_data.py
echo "ensuring notebook config is ok"
pip install --upgrade notebook  # need jupyter_client >= 4.2 for sys-prefix below
jupyter nbextension install --sys-prefix --py vega  # not needed in notebook >= 5.3
jupyter nbextension enable --py --sys-prefix ipyleaflet  # can be skipped for notebook 5.3 and above
jupyter nbextension enable --py --sys-prefix ipysigma

jupyter nbextension install --py --sys-prefix keplergl # can be skipped for notebook 5.3 and above
jupyter nbextension enable --py --sys-prefix keplergl # can be skipped for notebook 5.3 and above
echo "all done ! good datasprinting ;)"
