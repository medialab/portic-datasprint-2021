

use "/Users/guillaumedaudin/Documents/Recherche/Commerce International Français XVIIIe.xls/Balance du commerce/Retranscriptions_Commerce_France/Données Stata/bdd courante.dta", clear
keep if year==1789
keep if product_revolutionempire=="Sel"
keep if best_guess_national_region ==1
keep if export_import=="Exports"

collapse (sum) quantities_metric value,by(customs_office quantity_unit_metric)


format quantities_metric value %12.0fc
gsort - value

br

alif
use "/Users/guillaumedaudin/Documents/Recherche/Commerce International Français XVIIIe.xls/Balance du commerce/Retranscriptions_Commerce_France/Données Stata/bdd courante.dta", clear
keep if year==1789
keep if product_revolutionempire=="Sel"
keep if best_guess_national_region ==1
keep if export_import=="Exports"
drop if partner_grouping=="France"

collapse (sum) quantities_metric value,by(customs_office quantity_unit_metric)


format quantities_metric value %12.0fc
gsort - value

br

blif

use "/Users/guillaumedaudin/Documents/Recherche/Commerce International Français XVIIIe.xls/Balance du commerce/Retranscriptions_Commerce_France/Données Stata/bdd courante.dta", clear
keep if year==1789
keep if product_revolutionempire=="Sel"
keep if best_guess_national_region ==1
keep if export_import=="Exports"


collapse (sum) quantities_metric value,by(partner_grouping quantity_unit_metric)


format quantities_metric value %12.0fc
gsort - value

br

blif
use "/Users/guillaumedaudin/Documents/Recherche/Commerce International Français XVIIIe.xls/Balance du commerce/Retranscriptions_Commerce_France/Données Stata/bdd courante.dta", clear
keep if year==1789
keep if product_revolutionempire=="Sel"
keep if best_guess_national_region ==1
keep if export_import=="Exports"
keep if customs_office=="Marennes"


collapse (sum) quantities_metric value,by(partner_grouping quantity_unit_metric)


format quantities_metric value %12.0fc
gsort - value

br
