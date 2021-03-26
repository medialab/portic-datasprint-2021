Datasprint PORTIC 2021
===

Ce répertoire contient à la fois un ensemble de ressources et les productions des participants du datasprint PORTIC 2021 qui se tiendra les 6, 7, 8 et 9 avril 2021.

# Installation

Prérequis : installer [git](https://git-scm.com/), python et pip, puis éventuellement créez votre environnement virtuel.

Puis dans votre terminal, lancer les commandes suivantes :

```
git clone git@github.com:medialab/portic-datasprint-2021.git
cd portic-datasprint-2021
./install.sh
```

# Mise à jour des données

Si les données de base venaient à être mises à jour en cours de datasprint, une commande permet de les mettre à jour sur votre copie locale du répertoire (dans le dossier `data`) :

```
./load_data.sh
```

# Contenus du répertoire

- `data` -> données à plat proposées pour le datasprint
- `preliminary_inquiry` -> notebooks de l'analyse préliminaire effectuée par le médialab, à utiliser pour prendre connaissance de la base et du contexte
- `productions` -> les productions du datasprint, à organiser et réorganiser par équipes de travail
- `examples` -> exemples de mobilisation de la bibliothèque seule et avec différentes technologies associées à des notebooks jupyter
- `lib` -> la bibliothèque créée spécifiquement pour le datasprint. Elle pourra éventuellement être améliorée pendant le datasprint

# Documentation de la bibliothèque
Voir :
[doc en ligne](https://medialab.github.io/portic-datasprint-2021/).
[doc en jupyter notebook](https://github.com/medialab/portic-datasprint-2021/blob/main/documentation_lib.ipynb)

Cette bibliothèque propose une abstraction permettant de manipuler les données avec une API unifiée, ainsi qu'une série d'utilitaires. Elle a vocation à être potentiellement enrichie pendant le datasprint.

Les données de base sont disponibles à :

* pour toflit18 : sur le répertoire [`medialab/toflit18_data/base courante.zip`](https://github.com/medialab/toflit18_data/blob/master/base/bdd%20courante.csv.zip) et via le [datascape](http://toflit18.medialab.sciences-po.fr/#/home)
* pour PORTIC : à [http://data.portic.fr/api/](http://data.portic.fr/api/) (documentation originale [ici](https://gitlab.huma-num.fr/portic/porticapi))

## Importer la bibliothèque

La bibliothèque est installée localement par le script `install.sh` (ou via `pip install -e lib`) puis est accessible sous le nom de `poitousprint`.
Ne pas oublier de la réinstaller après un git pull si besoin.

Elle est constituée de deux clients web (un pour chaque base) et d'une série de fonctions utilitaires dédiées à la simplification des données, aux croisements ou à la préparation de visualisations et analyses :

```python
from poitousprint import Portic, Toflit, nest_toflit18_flow, nest_portic_pointcall, build_cooccurence_graph
```


