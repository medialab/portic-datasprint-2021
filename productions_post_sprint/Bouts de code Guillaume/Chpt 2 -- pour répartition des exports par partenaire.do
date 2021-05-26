
*initial : 
use "/Users/guillaumedaudin/Documents/Recherche/Commerce International Français XVIIIe.xls/Balance du commerce/Retranscriptions_Commerce_France/Données Stata/bdd courante.dta", clear
keep if year==1789
keep if customs_office=="La Rochelle"
keep if best_guess_national_region ==1
tab partner_simplification if partner_grouping=="Monde"
tab best_guess_national_region
collapse (sum) value, by (partner_grouping)
egen total = total(value)
gen pcrt = value/total
br



blif







use "/Users/guillaumedaudin/Documents/Recherche/Commerce International Français XVIIIe.xls/Balance du commerce/Retranscriptions_Commerce_France/Données Stata/bdd courante.dta", clear
keep if year==1789
keep if customs_region=="La Rochelle"
keep if export_import =="Exports"
keep if best_guess_national_region ==1
*tab partner_simplification if partner_grouping=="Monde »
collapse (sum) value, by (partner_grouping)
egen total = total(value)
gen pcrt = value/total
format total %12.0fc
format value %12.0fc
format pcrt %3.2fc
br

blif

use "/Users/guillaumedaudin/Documents/Recherche/Commerce International Français XVIIIe.xls/Balance du commerce/Retranscriptions_Commerce_France/Données Stata/bdd courante.dta", clear
keep if year==1789
keep if customs_region=="La Rochelle"
keep if best_guess_national_region ==1
drop if product_reexportations=="Réexportation"
drop if partner_grouping =="France"
keep if export_import =="Exports"
*tab partner_simplification if partner_grouping=="Monde »
collapse (sum) value, by (partner_grouping)
egen total = total(value)
gen pcrt = value/total
format total %12.0fc
format value %12.0fc
format pcrt %3.2fc
br
