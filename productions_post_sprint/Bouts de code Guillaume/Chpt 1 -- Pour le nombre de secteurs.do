use "/Users/guillaumedaudin/Documents/Recherche/Commerce International Français XVIIIe.xls/Balance du commerce/Retranscriptions_Commerce_France/Données Stata/bdd courante.dta", clear
codebook product_revolutionempire if year==1750 & best_guess_national_region ==1 & customs_region=="La Rochelle" & partner_grouping !="France"
codebook product_revolutionempire if year==1789 & best_guess_national_region ==1 & customs_region=="La Rochelle" & partner_grouping !="France"
