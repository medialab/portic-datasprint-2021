
use "/Users/guillaumedaudin/Documents/Recherche/Commerce International Français XVIIIe.xls/Balance du commerce/Retranscriptions_Commerce_France/Données Stata/bdd courante.dta", clear

keep if year==1789 & best_guess_national_region ==1 & customs_region=="La Rochelle" & export_import=="Exports"
collapse (sum) value,by(customs_office)

format value %9.0fc

egen total=total(value)

format total %12.0fc
br

blif

use "/Users/guillaumedaudin/Documents/Recherche/Commerce International Français XVIIIe.xls/Balance du commerce/Retranscriptions_Commerce_France/Données Stata/bdd courante.dta", clear

keep if year==1789 & best_guess_national_region ==1 & customs_region=="La Rochelle"
collapse (sum) value,by(customs_office)

format value %9.0fc

egen total=total(value)

format total %12.0fc
br


use "/Users/guillaumedaudin/Documents/Recherche/Commerce International Français XVIIIe.xls/Balance du commerce/Retranscriptions_Commerce_France/Données Stata/bdd courante.dta", clear

keep if year==1789 & best_guess_national_region ==1 & customs_region=="La Rochelle" & export_import=="Exports" & partner_grouping!="France"
collapse (sum) value,by(customs_office)

format value %9.0fc

egen total=total(value)

format total %12.0fc
br

blif

use "/Users/guillaumedaudin/Documents/Recherche/Commerce International Français XVIIIe.xls/Balance du commerce/Retranscriptions_Commerce_France/Données Stata/bdd courante.dta", clear

keep if year==1789 & best_guess_national_region ==1 & customs_region=="La Rochelle" & partner_grouping!="France"
collapse (sum) value,by(customs_office)

format value %9.0fc

egen total=total(value)

format total %12.0fc
br
