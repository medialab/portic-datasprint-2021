use "/Users/guillaumedaudin/Documents/Recherche/Commerce International Français XVIIIe.xls/Balance du commerce/Retranscriptions_Commerce_France/Données Stata/bdd courante.dta", clear

keep if year == 1750 | year==1789

keep if (customs_region=="La Rochelle" & best_guess_region_prodxpart==1 & partner_grouping != "France") | /*
*/ best_guess_national_partner==1

collapse (sum) value, by(export_import customs_region year)

replace customs_region="France" if customs_region==""
replace customs_region="LaRochelle" if customs_region=="La Rochelle"

reshape wide value, i(year export_import) j(customs_region) string


gen share = valueLaRochelle/valueFrance
format share %4.3f
list

collapse (sum) valueLaRochelle valueFrance, by(customs_region year)
gen share = valueLaRochelle/valueFrance
format share %4.3f
list
