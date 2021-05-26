ssc install hhi5
use "/Users/guillaumedaudin/Documents/Recherche/Commerce International Français XVIIIe.xls/Balance du commerce/Retranscriptions_Commerce_France/Données Stata/bdd courante.dta", clear
keep if (year==1750 | year==1789) & best_guess_national_region ==1 & export_import=="Exports" & customs_region=="La Rochelle"
collapse (sum) value, by(product_revolutionempire year)
hhi5 value,by(year)
gsort year - value
br
