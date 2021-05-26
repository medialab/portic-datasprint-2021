use "/Users/guillaumedaudin/Documents/Recherche/TradersIntercontinentalTradeandGrowthBeforetheIndsutrialRevolution/Travail Statistique/Data/MaBasePourRegression_Cities.dta"
br cityname year u_AJR if (cityname =="LA ROCHELLE" | cityname =="BORDEAUX" | cityname =="NANTES") & year >=1700 & year <=1800
