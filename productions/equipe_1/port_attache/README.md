ici on s'occupe des navires qui sortent de DLFR vers l'Etranger
pointcall_province in ('Aunis', 'Saintonge', 'Poitou') pour le pointcall de départ

# Fichier sorties_navires_vers_etranger.csv

-- vers l'étranger
-- extraction des ports d'attache (homeport_*) 
-- avec le tonnage des navires (tonnage)

select p1.toponyme_fr as port_depart, p1.outdate_fixed , p2.toponyme_fr as port_destination, 
p1.homeport_state_1789_fr , p1.homeport_toponyme_fr, p1.homeport_province ,
p1.commodity_standardized_fr , p1.commodity_standardized2_fr, p1.commodity_standardized3_fr , p1.commodity_standardized4_fr,
p1.taxe_amount01 , p1.taxe_amount02 , p1.taxe_amount03 , 
p1.tonnage , p1.tonnage_unit , p1.tonnage_class 
from 
navigoviz.pointcall p1, navigoviz.pointcall p2 where
(p1.pointcall_action = 'Out' or p1.pointcall_action = 'In-Out' )
and p1.pointcall_province in ('Aunis', 'Saintonge', 'Poitou')
and extract(year from p1.outdate_fixed) = 1789
and p2.state_1789_fr != 'France' and (p2.pointcall_action = 'In' or p2.pointcall_action = 'In-Out') 
and p1.source_doc_id  = p2.source_doc_id


-- vers l'étranger et les colonies françaises.
-- on garde aussi les pavillons (ship_flag_standardized_fr)

select p1.toponyme_fr as port_depart, p1.outdate_fixed , p2.toponyme_fr as port_destination, p2.substate_1789_fr as substate_destination,
p1.homeport_state_1789_fr , p1.homeport_toponyme_fr, p1.homeport_province ,
p1.commodity_standardized_fr , p1.commodity_standardized2_fr, p1.commodity_standardized3_fr , p1.commodity_standardized4_fr,
p1.taxe_amount01 , p1.taxe_amount02 , p1.taxe_amount03 , 
p1.tonnage , p1.tonnage_unit , p1.tonnage_class , p1.ship_flag_standardized_fr 
from 
navigoviz.pointcall p1, navigoviz.pointcall p2 where
(p1.pointcall_action = 'Out' or p1.pointcall_action = 'In-Out' )
and p1.pointcall_province in ('Aunis', 'Saintonge', 'Poitou')
and extract(year from p1.outdate_fixed) = 1789
and (p2.state_1789_fr != 'France' or p2.substate_1789_fr like 'colonies%') 
and (p2.pointcall_action = 'In' or p2.pointcall_action = 'In-Out') 
and p1.source_doc_id  = p2.source_doc_id 

# Fichier sorties_navires_vers_france_horsDFLR.csv

-- les sorties de DFLR vers la France, hors DFLR
-- extraction des ports d'attache (homeport_*) et des pavillons (ship_flag_standardized_fr)
-- avec le tonnage des navires (tonnage)
select p1.toponyme_fr as port_depart, p1.outdate_fixed , 
p2.toponyme_fr as port_destination, p2.pointcall_admiralty as amiraute_destination, p2.pointcall_province as province_destination, p2.substate_1789_fr as substate_destination,
p1.homeport_state_1789_fr , p1.homeport_toponyme_fr, p1.homeport_province ,
p1.commodity_standardized_fr , p1.commodity_standardized2_fr, p1.commodity_standardized3_fr , p1.commodity_standardized4_fr,
p1.taxe_amount01 , p1.taxe_amount02 , p1.taxe_amount03 , 
p1.tonnage , p1.tonnage_unit , p1.tonnage_class , p1.ship_flag_standardized_fr 
from 
navigoviz.pointcall p1, navigoviz.pointcall p2 where
(p1.pointcall_action = 'Out' or p1.pointcall_action = 'In-Out' )
and p1.pointcall_province in ('Aunis', 'Saintonge', 'Poitou')
and extract(year from p1.outdate_fixed) = 1789
and (p2.state_1789_fr = 'France' and p2.pointcall_province not in ('Aunis', 'Saintonge', 'Poitou')) 
and (p2.pointcall_action = 'In' or p2.pointcall_action = 'In-Out') 
and p1.source_doc_id  = p2.source_doc_id 
  
