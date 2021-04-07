ici on s'occupe des navires qui sortent de DLFR vers l'Etranger en 1789 : 
**pointcall_province** in ('Aunis', 'Saintonge', 'Poitou') pour le pointcall de départ

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

select p1.toponyme_fr as port_depart, p1.outdate_fixed , 
p2.toponyme_fr as port_destination, p2.substate_1789_fr as substate_destination, p2.state_1789_fr as state_destination,
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

# Fichier sorties_navires_vers_colonies.csv

-- vers les colonies et l'Afrique (traite négrière) en 1789

select p1.record_id, p1.ship_id, p1.ship_name, p1.captain_name, p1.toponyme_fr as port_depart, p1.outdate_fixed , 
p2.toponyme_fr as port_destination, p2.substate_1789_fr as substate_destination, p2.state_1789_fr as state_destination,
p1.homeport_state_1789_fr , p1.homeport_toponyme_fr, p1.homeport_province ,
p1.commodity_standardized_fr , p1.commodity_standardized2_fr, p1.commodity_standardized3_fr , p1.commodity_standardized4_fr,
p1.taxe_amount01 , p1.taxe_amount02 , p1.taxe_amount03 , 
p1.tonnage , p1.tonnage_unit , p1.tonnage_class , p1.ship_flag_standardized_fr 
from 
navigoviz.pointcall p1, navigoviz.pointcall p2 
where
(p1.pointcall_action = 'Out' or p1.pointcall_action = 'In-Out' )
and p1.pointcall_province in ('Aunis', 'Saintonge', 'Poitou')
and extract(year from p1.outdate_fixed) = 1789
and ( p2.substate_1789_fr like '%olonies%' 
	or p2.partner_balance_supp_1789='Sénégal et Guinée') 
-- and (p2.pointcall_action = 'In' or p2.pointcall_action = 'In-Out') 
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


 
# Flux en 1789

- Regarder pointcalls et pas flows

## Fichier sorties_navires_vers_colonies_pour_Thierry.csv

Attention : 
p2.substate_1789_fr like '%olonies%'  or p2.state_1789_fr = 'zone maritime' 	or p2.partner_balance_supp_1789='Sénégal et Guinée'
p2.pointcall_action in (**'In','In-Out','Sailing','Sailing around', 'Transit', 'In-out'**)  
  
-- les sorties de la Direction de la Ferme de la Rochelle vers les colonies en 1789

select p1.pointcall_out_date2, p2.pointcall_in_date, p1.record_id, 
p1.ship_id, p1.ship_name, p1.captain_name, p1.toponyme_fr as port_depart, p1.outdate_fixed , 
p2.toponyme_fr as port_destination, p2.pointcall_province, 
p2.substate_1789_fr as substate_destination, p2.state_1789_fr as state_destination,
p2.pointcall_admiralty as destination_admiralty,
p1.pointcall_admiralty as departure_admiralty,
p2.pointcall_province as destination_province,
p1.pointcall_province as departure_province,
p1.pointcall_action, p2.pointcall_action,
p1.homeport_state_1789_fr , p1.homeport_toponyme_fr, p1.homeport_province , p1.ship_flag_standardized_fr ,
p1.commodity_standardized_fr , p1.commodity_standardized2_fr, p1.commodity_standardized3_fr , p1.commodity_standardized4_fr,
p1.tonnage , p1.tonnage_unit , p1.tonnage_class 
from 
navigoviz.pointcall p1, navigoviz.pointcall p2 
where
(p1.pointcall_action = 'Out' or p1.pointcall_action = 'In-Out' )
and p1.pointcall_province in ('Aunis', 'Saintonge', 'Poitou')
and extract(year from p1.outdate_fixed) = 1789
and ( p2.substate_1789_fr like '%olonies%'  or p2.state_1789_fr = 'zone maritime'
	or p2.partner_balance_supp_1789='Sénégal et Guinée')
and p2.pointcall_action in ('In','In-Out','Sailing','Sailing around', 'Transit', 'In-out')  
and p1.source_doc_id  = p2.source_doc_id 
 order by p1.ship_name , p1.pointcall_out_date2 

## Fichier sorties_navires_de_DFLR.csv

-- les sorties de la Direction de la Ferme en 1789

select p1.pointcall_out_date2, p2.pointcall_in_date, p1.record_id, 
p1.ship_id, p1.ship_name, p1.captain_name, p1.toponyme_fr as port_depart, p1.outdate_fixed , 
p2.toponyme_fr as port_destination, p2.pointcall_province,p2.substate_1789_fr as substate_destination, p2.state_1789_fr as state_destination,
p2.pointcall_admiralty as destination_admiralty,
p1.pointcall_admiralty as departure_admiralty,
p2.pointcall_province as destination_province,
p1.pointcall_province as departure_province,
p1.pointcall_action,
p1.homeport_state_1789_fr , p1.homeport_toponyme_fr, p1.homeport_province , p1.ship_flag_standardized_fr ,
p1.commodity_standardized_fr , p1.commodity_standardized2_fr, p1.commodity_standardized3_fr , p1.commodity_standardized4_fr,
p1.tonnage , p1.tonnage_unit , p1.tonnage_class 
from 
navigoviz.pointcall p1, navigoviz.pointcall p2 
where
(p1.pointcall_action = 'Out' or p1.pointcall_action = 'In-Out' )
and p1.pointcall_province in ('Aunis', 'Saintonge', 'Poitou')
and extract(year from p1.outdate_fixed) = 1789 
and p1.source_doc_id  = p2.source_doc_id 
order by p2.toponyme_fr, p1.pointcall_out_date2 
