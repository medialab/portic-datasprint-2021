****Pour l’étude de la diversité des produits

use "/Users/guillaumedaudin/Documents/Recherche/Commerce International Français XVIIIe.xls/Balance du commerce/Retranscriptions_Commerce_France/Données Stata/bdd courante.dta", clear

keep if year==1750 | year==1789
keep if best_guess_region_prodxpart==1

quietly levelsof product_simplification if year==1750
display "nombre de produits 1750 : `r(r)'"
local nbr_prod_1750=`r(r)'

quietly levelsof product_simplification if year==1789
display "nombre de produits 1789 : `r(r)'"
local nbr_prod_1789=`r(r)'


quietly  levelsof product_simplification if year==1750 & customs_region=="La Rochelle"
display "nombre de produits 1750 à La Rochelle : `r(r)'"
local nbr_prod_1750_LR=`r(r)'
local ratio = `nbr_prod_1750_LR'/`nbr_prod_1750'
display "Partie échangée à La Rochelle : `ratio'"

quietly levelsof product_simplification if year==1789 & customs_region=="La Rochelle"
display "nombre de produits 1789 à La Rochelle : `r(r)'"
local nbr_prod_1789_LR=`r(r)'
local ratio = `nbr_prod_1789_LR'/`nbr_prod_1789'
display "Partie échangée à La Rochelle : `ratio'"

