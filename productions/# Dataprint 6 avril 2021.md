# 1. Dataprint 6 avril 2021

Etude la Rochelle  : le poitou en 1789

- [1. Dataprint 6 avril 2021](#1-dataprint-6-avril-2021)
  - [1.1. Point sur les données et questions scientifiques](#11-point-sur-les-données-et-questions-scientifiques)
  - [1.2. code](#12-code)

## 1.1. Point sur les données et questions scientifiques

1763 : perte du Canada très impactante pour la Rochelle (essort de cette source de revenus "propres" -> 1763).
1789 : 
    - crise frumentaire (pénurie agricole pour les céréales) - veille de la Révolution
    - traité d'Eden avec l'Angleterre, très impactant sur le textile et la Normandie

- La Rochelle, entre Nantes et Bordeaux, en rapprochement avec Bordeaux pour la traite négrière. Les Sables d'Olonne très inféodés à Nantes.
Est-ce que le commerce du Poitou (la Rochelle et Rochefort en particulier) est téléguidé de l'extérieur (cad profite à des inverstisseurs Nantais, Bordelais ou étrangers) ? Est-ce que la Rochelle se spécialise sur les produits que les autres grands ports lui laissent par défaut.
Un commerce d'entrepôt avec beaucoup de ré-exportations ? 
exemple : sucre/cacao arrive des Antilles et repart avec l'Etranger à 75 %
- Rochefort : port d'arsenal militaire avec privilège sur commerce colonial, inscrit dans une navigation de type circuiteuse (le port de Tonnay-Charente, voisin, se spécialise dans le fret retour des colonies (eau de vie de Cognac par exemple) ?)
Existence d'une solidarité entre ports moyens et grands dans le réseau : **enquète SYSTEMIQUE**. 
- Marennes : exception car beaucoup de sortie (et avec SEL), mais en baisse, au profit peut-être de LR qui aurait dévéloppé un commerce d'entrepôt du sel. 



- analyse multiscalaire port/province/sous-etats/etats en (nombre de flux, valeur de flux, volume de flux)
  - **volume de traffic** : 
    - nb de bateau
    - nb flux toflit de direction de ferme associées aux ports (origine ou destination). Attention : différentes orthographes du même produit augmentent le nombre de flux agrégés 
    - volume des navires : variables suivant les ports (sur/sous tonnage) et un navire n'est pas forcément plein à craquer
  - **valeur de traffic** :
    - taxe de sortie des navires : taxe_amount01 et taxe_amount02, payée en fonction du tonnage et de la destination
    - valeur marchande dans toflit ; prix per unit à multiplier par la quantité de marchandise (attention pb de conversion)

1. Etendue géographique
- Portic : 
    - 1787 : France métropolitaine et (vers) l'Etranger et ses colonies
    - 1789 : Poitou, Dunkerque, Marseille en sorties et (vers) l'Etranger et ses colonies
- Toflit : 
    - Toutes les Fermes de la France et ses colonies

Dans le détail : le port de La Rochelle (LR) n'indique jamais le type de produit transporté sur les navires
On ne capture pas les entrées dans les ports du Poitou en 1789 (mais en 1787 on a les sorties des autres ports de FRANCE, vers le Poitou) car la taxe n'est due qu'en sortie de port
Quand un navire fait un aller-retour entre 2 ports de la même amirauté, on ne connait pour l'instant que sa sortie première car il n'est pas obligé de déclarer son retour. Après identification des navires terminée en 1789, on pourra connaitre la date de retour au plus tard.


2. Coupe temporelle 
- Toflit : [1718-1780] + 1789 sur la Direction de la Rochelle : pas d'année 1787 et trou entre 1780 et 1789. Flux par an. [1750-1780] : niveau local et national
- Portic : analyse au jour possible (saisonnalité) sur 1787 et 1789
- cahiers de doléance : géolocalisés et plain texte.




## 1.2. code
https://github.com/medialab/portic-datasprint-2021

git clone https://github.com/medialab/portic-datasprint-2021.git

Toflit : filtres possibles
- origin_origin : provenance (par Province)
- customs_regions : Direction de la Ferme de la Rochelle
- année = 1789


