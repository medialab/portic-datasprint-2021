-- Christine Plumejeaud, 06 aril 2021


-- import du fichier https://docs.google.com/spreadsheets/d/1wtgGQ3sHlQWs0shdJRsyWxd2VR48DX5Eu-3lsckviaI/edit#gid=410838707
-- onglet bdd_origin.csv

SELECT * FROM ports.toflit18_bdd_origin_bdd_origin_csv

alter table ports.toflit18_bdd_origin_bdd_origin_csv rename column france to state_1789_fr
alter table ports.toflit18_bdd_origin_bdd_origin_csv add column substate_1789_fr text

SELECT origin, origin_norm_ortho, pp.toponyme, pp.toponyme_standard_fr, pp.province , pp.substate_1789_fr , pp.state_1789_fr 
FROM ports.toflit18_bdd_origin_bdd_origin_csv toflit, ports.port_points pp 
where origin = pp.toponyme

update ports.toflit18_bdd_origin_bdd_origin_csv  toflit
set state_1789_fr = pp.state_1789_fr, substate_1789_fr=pp.substate_1789_fr, province = pp.province 
from ports.port_points pp
where toflit.origin = pp.toponyme

SELECT origin, origin_norm_ortho, pp.toponyme, pp.toponyme_standard_fr, pp.province , pp.substate_1789_fr , pp.state_1789_fr 
FROM ports.toflit18_bdd_origin_bdd_origin_csv toflit, ports.port_points pp 
where origin_norm_ortho  = pp.toponyme_standard_fr and toflit.province is null


update ports.toflit18_bdd_origin_bdd_origin_csv  toflit
set state_1789_fr = pp.state_1789_fr, substate_1789_fr=pp.substate_1789_fr, province = pp.province 
from ports.port_points pp
where origin_norm_ortho  = pp.toponyme_standard_fr and toflit.province is null


SELECT origin, origin_norm_ortho
FROM ports.toflit18_bdd_origin_bdd_origin_csv toflit
where  toflit.province is null and state_1789_fr is null


SELECT distinct origin, origin_norm_ortho, pp.substate_1789_fr
FROM ports.toflit18_bdd_origin_bdd_origin_csv toflit, ports.port_points pp 
where  toflit.province is null and toflit.state_1789_fr is null and origin_norm_ortho % pp.substate_1789_fr

Isles Amerique
Isles francaises
Isles

Isle françaises -- colonies françaises d''Amérique
îles d''Amérique -- colonies françaises d''Amérique
Indes colonies françaises -- colonies françaises en Asie
Colonies françaises de l''Amérique  -- colonies françaises d''Amérique
Colonies françaises  -- colonies françaises d''Amérique 
-- et ? 
-- colonies françaises en Afrique
-- colonies françaises en Asie
Colonies Espagnoles -- colonies espagnoles d'Amérique

-- Colonies ?
Amérique ?
Amérique espagnole -- colonies espagnoles d'Amérique

SELECT distinct  origin_norm_ortho, pp.substate_1789_fr
FROM ports.toflit18_bdd_origin_bdd_origin_csv toflit, ports.port_points pp 
where  toflit.province is null and toflit.substate_1789_fr is null and origin_norm_ortho % pp.substate_1789_fr

update ports.toflit18_bdd_origin_bdd_origin_csv  toflit
set substate_1789_fr = 'colonies françaises d''Amérique'
where origin_norm_ortho  in ('Isle françaises', 'îles d''Amérique', 'Colonies françaises de l''Amérique')  and toflit.substate_1789_fr is null

update ports.toflit18_bdd_origin_bdd_origin_csv  toflit
set substate_1789_fr = 'colonies espagnoles d''Amérique'
where origin_norm_ortho  in ('Amérique espagnole', 'Colonies Espagnoles')  and toflit.substate_1789_fr is null

-- 
update ports.toflit18_bdd_origin_bdd_origin_csv  toflit
set substate_1789_fr = 'colonies françaises en Asie'
where origin_norm_ortho  in ('Indes colonies françaises')  and toflit.substate_1789_fr is null;

update ports.toflit18_bdd_origin_bdd_origin_csv  toflit
set state_1789_fr = 'Grande-Bretagne'
where origin_norm_ortho  in ('Irlande et Angleterre')  and toflit.substate_1789_fr is null;


update ports.toflit18_bdd_origin_bdd_origin_csv  toflit
set state_1789_fr = 'Etats-Unis d''Amérique'
where origin_norm_ortho  in ('Caroline')  and toflit.substate_1789_fr is null;

update ports.toflit18_bdd_origin_bdd_origin_csv  toflit
set state_1789_fr = 'Russie'
where origin_norm_ortho  in ('Russie')  and toflit.substate_1789_fr is null;


alter table ports.toflit18_bdd_origin_bdd_origin_csv add column doutes text

update ports.toflit18_bdd_origin_bdd_origin_csv set doutes = 'colonies espagnoles d''Amérique;colonies britanniques d''Amérique;colonies françaises d''Amérique'
where origin_norm_ortho = 'Amérique';

update ports.toflit18_bdd_origin_bdd_origin_csv set doutes = 'Caroline du Nord;Caroline du Sud'
where origin_norm_ortho = 'Caroline';

update ports.toflit18_bdd_origin_bdd_origin_csv set doutes = 'Caroline du Nord;Caroline du Sud'
where origin_norm_ortho = 'Caroline';

update  ports.toflit18_bdd_origin_bdd_origin_csv t set state_1789_fr = pp.state_1789_fr 
from port_points pp
where t.substate_1789_fr is not null and t.state_1789_fr is null and pp.substate_1789_fr = t.substate_1789_fr 

alter table ports.toflit18_bdd_origin_bdd_origin_csv add column partner_balance_1789 text;
alter table ports.toflit18_bdd_origin_bdd_origin_csv add column partner_balance_supp_1789 text;

update  ports.toflit18_bdd_origin_bdd_origin_csv t 
set partner_balance_1789 = pp.partner_balance_1789 
from port_points pp
where origin_norm_ortho = pp.partner_balance_1789

update  ports.toflit18_bdd_origin_bdd_origin_csv t 
set partner_balance_supp_1789 = pp.partner_balance_supp_1789 
from port_points pp
where origin_norm_ortho = pp.partner_balance_supp_1789

SELECT distinct  origin_norm_ortho, pp.substate_1789_fr, pp.partner_balance_supp_1789, toflit.*
FROM ports.toflit18_bdd_origin_bdd_origin_csv toflit, ports.port_points pp 
where  (toflit.partner_balance_1789 is null or toflit.partner_balance_supp_1789 is null) and origin_norm_ortho % pp.partner_balance_supp_1789

update ports.toflit18_bdd_origin_bdd_origin_csv t 
set partner_balance_supp_1789 = 'colonies françaises'
from port_points pp
where origin_norm_ortho in ('Colonies', 'Colonies françaises', 'Colonies françaises de l''Amérique', 'Îles françaises', 'Indes colonies françaises', 'Indes commerce français');

update ports.toflit18_bdd_origin_bdd_origin_csv t 
set partner_balance_supp_1789 = 'Etranger'
from port_points pp
where origin_norm_ortho = 'Étranger'


update ports.toflit18_bdd_origin_bdd_origin_csv  
set partner_balance_1789 = 'Espagne', partner_balance_supp_1789='Etranger'
where origin_norm_ortho  in ('Amérique espagnole', 'Colonies Espagnoles')  

update ports.toflit18_bdd_origin_bdd_origin_csv  
set state_1789_fr = 'France', partner_balance_supp_1789='France'
where origin_norm_ortho  in ('France')  

update ports.toflit18_bdd_origin_bdd_origin_csv  
set state_1789_fr = 'France', partner_balance_supp_1789='France'
where origin_norm_ortho  in ('Île de France')

update ports.toflit18_bdd_origin_bdd_origin_csv  
set state_1789_fr = 'France'
where partner_balance_supp_1789 in ('France', 'colonies françaises')

select distinct ship_flag_standardized_fr from  navigoviz.pointcall p 

select distinct homeport_toponyme_fr, homeport_province, homeport_partner_balance_1789 from  navigoviz.pointcall p 

select * from 
navigoviz.pointcall p1, navigoviz.pointcall p2 where
(p1.pointcall_action = 'Out' or p1.pointcall_action = 'In-Out' )
and p1.pointcall_province in ('Aunis', 'Saintonge', 'Poitou')
and extract(year from p1.outdate_fixed) = 1789
and p2.state_1789_fr != 'France' and (p2.pointcall_action = 'In' or p2.pointcall_action = 'In-Out') 
and p1.source_doc_id  = p2.source_doc_id 

-- sorties vers l'Etranger de DFLR en 1789, excluant les colonies
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

-- avec les colonies Françaises
select distinct substate_1789_fr from navigoviz.pointcall where state_1789_fr = 'France'

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

-- les sorties de DFLR vers la France, hors DFLR, en 1789
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

SELECT DISTINCT source_subset FROM navigoviz.pointcall
-- pour les ports Francs
port_destination in ('Dunkerque', 'Marseille', 'Bayonne', 'Lorient')

-- vers les colonies uniquement
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

select distinct p.pointcall_admiralty , p.pointcall_province 
from navigoviz.pointcall p
where pointcall_province in ('Aunis', 'Saintonge', 'Poitou')
-- Sables-d’Olonne

-- les sorties de la Direction de la Ferme
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
-- p1.taxe_amount01 , p1.taxe_amount02 , p1.taxe_amount03 , 
p1.tonnage , p1.tonnage_unit , p1.tonnage_class 
from 
navigoviz.pointcall p1, navigoviz.pointcall p2 
where
(p1.pointcall_action = 'Out' or p1.pointcall_action = 'In-Out' )
and p1.pointcall_province in ('Aunis', 'Saintonge', 'Poitou')
and extract(year from p1.outdate_fixed) = 1789
--and ( p2.substate_1789_fr like '%olonies%') 
-- and (p2.pointcall_action = 'In' or p2.pointcall_action = 'In-Out') 
and p1.source_doc_id  = p2.source_doc_id 
--and p2.pointcall_province % 'Saint-Domingue'
order by p2.toponyme_fr, p1.pointcall_out_date2 


/*select p1.pointcall_out_date2, p2.pointcall_in_date, p1.record_id, 
p1.ship_id, p1.ship_name, p1.captain_name, p1.toponyme_fr as port_depart, p1.outdate_fixed , 
p2.toponyme_fr as port_destination, p2.pointcall_province,p2.substate_1789_fr as substate_destination, p2.state_1789_fr as state_destination,
p2.pointcall_admiralty as destination_admiralty,
p1.pointcall_admiralty as departure_admiralty,
p2.pointcall_province as destination_province,
p1.pointcall_province as departure_province,
p1.pointcall_action,
p1.homeport_state_1789_fr , p1.homeport_toponyme_fr, p1.homeport_province , p1.ship_flag_standardized_fr ,
p1.commodity_standardized_fr , p1.commodity_standardized2_fr, p1.commodity_standardized3_fr , p1.commodity_standardized4_fr,
-- p1.taxe_amount01 , p1.taxe_amount02 , p1.taxe_amount03 , 
p1.tonnage , p1.tonnage_unit , p1.tonnage_class 
from 
navigoviz.pointcall p1, navigoviz.pointcall p2 
where
(p1.pointcall_action = 'Out' or p1.pointcall_action = 'In-Out' )
and p1.pointcall_province in ('Aunis', 'Saintonge', 'Poitou')
and extract(year from p1.outdate_fixed) = 1789
and ( p2.substate_1789_fr like '%olonies%' or p2.toponyme_fr % 'Cote d''or') 
--and (p2.pointcall_action = 'In' or p2.pointcall_action = 'In-Out') 
and p1.source_doc_id  = p2.source_doc_id 
--and p2.pointcall_province % 'Saint-Domingue'
order by p1.ship_name , p1.pointcall_out_date2 */

-- les sorties de la Direction de la Ferme vers les colonies et l'Afrique
select distinct pp.partner_balance_supp_1789 from port_points pp 

--Sénégal et Guinée
--colonies françaises
--Etranger
--France
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
-- p1.taxe_amount01 , p1.taxe_amount02 , p1.taxe_amount03 , 
p1.tonnage , p1.tonnage_unit , p1.tonnage_class 
from 
navigoviz.pointcall p1, navigoviz.pointcall p2 
where
(p1.pointcall_action = 'Out' or p1.pointcall_action = 'In-Out' )
and p1.pointcall_province in ('Aunis', 'Saintonge', 'Poitou')
and extract(year from p1.outdate_fixed) = 1789
and ( p2.substate_1789_fr like '%olonies%'  or p2.state_1789_fr = 'zone maritime'
	or p2.partner_balance_supp_1789='Sénégal et Guinée')
--	or  p2.toponyme_fr % 'Grand banc' or  p2.toponyme_fr % 'Grand Banc de Terre Neuve') 
--or p2.toponyme_fr % 'Cote d''or'
and p2.pointcall_action in ('In','In-Out','Sailing','Sailing around', 'Transit', 'In-out')  
and p1.source_doc_id  = p2.source_doc_id 
--and p2.pointcall_province % 'Saint-Domingue'
-- and p1.pointcall_out_date = '1789=03=17'
 order by p1.ship_name , p1.pointcall_out_date2 
 
 
 -- les sorties vers l'étranger de DFLR en 1789, avec le sous-etat du homeport
 -- pas les colonies
select 'Aunis-Saintonge-Poitou' as region_depart, p1.pointcall_admiralty as amiraute_depart, p1.toponyme_fr as port_depart, p1.outdate_fixed , 
p2.toponyme_fr as port_destination, p2.partner_balance_1789, p2.partner_balance_supp_1789,
p1.ship_id, p1.ship_name, p1.captain_name,
p1.homeport_state_1789_fr , p1.homeport_substate_1789_fr, p1.homeport_toponyme_fr, p1.homeport_province ,
p1.commodity_standardized_fr , p1.commodity_standardized2_fr, p1.commodity_standardized3_fr , p1.commodity_standardized4_fr,
p1.taxe_amount01 , p1.taxe_amount02 , p1.taxe_amount03 , 
p1.tonnage , p1.tonnage_unit , p1.tonnage_class  
from navigoviz.pointcall p1, navigoviz.pointcall p2 where
(p1.pointcall_action = 'Out' or p1.pointcall_action = 'In-Out' )
and p1.pointcall_province in ('Aunis', 'Saintonge', 'Poitou')
and extract(year from p1.outdate_fixed) = 1789
and p2.state_1789_fr != 'France' and (p2.data_block_leader_marker = 'T') 
and p1.source_doc_id  = p2.source_doc_id 
order by p1.ship_name

-- or p2.partner_balance_supp_1789='Sénégal et Guinée'

-- departs d'ailleurs que DLFR vers Etranger en 1787
select p1.pointcall_province as region_depart, p1.pointcall_admiralty as amiraute_depart, p1.toponyme_fr as port_depart, p1.outdate_fixed , 
p2.toponyme_fr as port_destination, p2.partner_balance_1789, p2.partner_balance_supp_1789,
p1.ship_id, p1.ship_name, p1.captain_name,
p1.homeport_state_1789_fr , p1.homeport_substate_1789_fr, p1.homeport_toponyme_fr, p1.homeport_province ,
p1.commodity_standardized_fr , p1.commodity_standardized2_fr, p1.commodity_standardized3_fr , p1.commodity_standardized4_fr,
p1.taxe_amount01 , p1.taxe_amount02 , p1.taxe_amount03 , 
p1.tonnage , p1.tonnage_unit , p1.tonnage_class  
from navigoviz.pointcall p1, navigoviz.pointcall p2 where
(p1.pointcall_action = 'Out' or p1.pointcall_action = 'In-Out' )
and p1.pointcall_province not in ('Aunis', 'Saintonge', 'Poitou')
and extract(year from p1.outdate_fixed) = 1787
and p2.state_1789_fr != 'France' and (p2.data_block_leader_marker = 'T') 
and p1.source_doc_id  = p2.source_doc_id 
order by p1.ship_name



-------------

-- Jeudi matin
-- les sorties vers l'étranger de DFLR en 1789, avec le sous-etat du homeport
 -- pas les colonies
select 'Aunis-Saintonge-Poitou' as region_depart, 
p1.pointcall_admiralty as amiraute_depart, p1.toponyme_fr as port_depart, p1.outdate_fixed , 
p2.toponyme_fr as port_destination, p2.partner_balance_1789, p2.partner_balance_supp_1789,
p2.pointcall_province,p2.substate_1789_fr as substate_destination, p2.state_1789_fr as state_destination,
p1.ship_id, p1.ship_name, p1.captain_name,
p1.homeport_state_1789_fr , p1.homeport_substate_1789_fr, p1.homeport_toponyme_fr, p1.homeport_province ,
p1.commodity_standardized_fr , p1.commodity_standardized2_fr, p1.commodity_standardized3_fr , p1.commodity_standardized4_fr,
p1.taxe_amount01 , p1.taxe_amount02 , p1.taxe_amount03 , 
p1.tonnage , p1.tonnage_unit , p1.tonnage_class, p1.ship_flag_standardized_fr   
from navigoviz.pointcall p1, navigoviz.pointcall p2 where
(p1.pointcall_action = 'Out' or p1.pointcall_action = 'In-Out' )
and p1.pointcall_province in ('Aunis', 'Saintonge', 'Poitou')
and extract(year from p1.outdate_fixed) = 1789
and p2.state_1789_fr != 'France' and (p2.data_block_leader_marker = 'T') 
and p1.source_doc_id  = p2.source_doc_id 
UNION
-- departs d'ailleurs que DLFR vers Etranger en 1787
(select p1.pointcall_province as region_depart, p1.pointcall_admiralty as amiraute_depart, p1.toponyme_fr as port_depart, p1.outdate_fixed , 
p2.toponyme_fr as port_destination, p2.partner_balance_1789, p2.partner_balance_supp_1789,
p2.pointcall_province,p2.substate_1789_fr as substate_destination, p2.state_1789_fr as state_destination,
p1.ship_id, p1.ship_name, p1.captain_name,
p1.homeport_state_1789_fr , p1.homeport_substate_1789_fr, p1.homeport_toponyme_fr, p1.homeport_province ,
p1.commodity_standardized_fr , p1.commodity_standardized2_fr, p1.commodity_standardized3_fr , p1.commodity_standardized4_fr,
p1.taxe_amount01 , p1.taxe_amount02 , p1.taxe_amount03 , 
p1.tonnage , p1.tonnage_unit , p1.tonnage_class, p1.ship_flag_standardized_fr   
from navigoviz.pointcall p1, navigoviz.pointcall p2 where
(p1.pointcall_action = 'Out' or p1.pointcall_action = 'In-Out' )
and p1.pointcall_province not in ('Aunis', 'Saintonge', 'Poitou')
and extract(year from p1.outdate_fixed) = 1787
and p2.state_1789_fr != 'France' and (p2.data_block_leader_marker = 'T') 
and p1.source_doc_id  = p2.source_doc_id 
)

-------------

-- pour vendredi matin,

-- les sorties vers l'étranger de DFLR en 1787, avec le sous-etat du homeport
 -- excluant les colonies françaises et  la pêche vers Terre-Neuve (zone maritime)
 
select 'Aunis-Saintonge-Poitou' as region_depart, p1.pointcall_province as province_depart, 
p1.state_1789_fr as etat_depart, p1.substate_1789_fr as sousetat_depart ,
p1.pointcall_admiralty as amiraute_depart, p1.toponyme_fr as port_depart, p1.outdate_fixed , 
p2.toponyme_fr as port_destination, p2.partner_balance_1789, p2.partner_balance_supp_1789,
p2.pointcall_province,p2.substate_1789_fr as substate_destination, p2.state_1789_fr as state_destination,
p1.ship_id, p1.ship_name, p1.captain_name,
p1.homeport_state_1789_fr , p1.homeport_substate_1789_fr, p1.homeport_toponyme_fr, p1.homeport_province ,
p1.commodity_standardized_fr , p1.commodity_standardized2_fr, p1.commodity_standardized3_fr , p1.commodity_standardized4_fr,
p1.taxe_amount01 , p1.taxe_amount02 , p1.taxe_amount03 , 
p1.tonnage , p1.tonnage_unit , p1.tonnage_class, p1.ship_flag_standardized_fr   
from navigoviz.pointcall p1, navigoviz.pointcall p2 where
(p1.pointcall_action = 'Out' or p1.pointcall_action = 'In-Out' )
and p1.pointcall_province in ('Aunis', 'Saintonge', 'Poitou')
and extract(year from p1.outdate_fixed) = 1787
and p2.state_1789_fr not in ('France', 'zone maritime') and (p2.data_block_leader_marker = 'T') 
and p1.source_doc_id  = p2.source_doc_id 

UNION

-- departs d'ailleurs que DLFR vers Etranger en 1787
-- excluant les colonies françaises et  la pêche vers Terre-Neuve (zone maritime)
 
(select p1.pointcall_province as region_depart, p1.pointcall_province as province_depart, 
p1.state_1789_fr as etat_depart, p1.substate_1789_fr as sousetat_depart ,
p1.pointcall_admiralty as amiraute_depart, p1.toponyme_fr as port_depart, p1.outdate_fixed , 
p2.toponyme_fr as port_destination, p2.partner_balance_1789, p2.partner_balance_supp_1789,
p2.pointcall_province,p2.substate_1789_fr as substate_destination, p2.state_1789_fr as state_destination,
p1.ship_id, p1.ship_name, p1.captain_name,
p1.homeport_state_1789_fr , p1.homeport_substate_1789_fr, p1.homeport_toponyme_fr, p1.homeport_province ,
p1.commodity_standardized_fr , p1.commodity_standardized2_fr, p1.commodity_standardized3_fr , p1.commodity_standardized4_fr,
p1.taxe_amount01 , p1.taxe_amount02 , p1.taxe_amount03 , 
p1.tonnage , p1.tonnage_unit , p1.tonnage_class, p1.ship_flag_standardized_fr   
from navigoviz.pointcall p1, navigoviz.pointcall p2 where
(p1.pointcall_action = 'Out' or p1.pointcall_action = 'In-Out' )
and p1.pointcall_province not in ('Aunis', 'Saintonge', 'Poitou')
and extract(year from p1.outdate_fixed) = 1787
and p2.state_1789_fr not in ('France', 'zone maritime') and (p2.data_block_leader_marker = 'T') 
and p1.source_doc_id  = p2.source_doc_id 
)


select * from navigoviz.built_travels where source_entry <> 'both-to' 
and (substring(departure_out_date for 4) = '1787' or substring(destination_in_date for 4) = '1787')


select sum(tonnage::float) 
from pointcall p1 
where p1.pointcall_province in ('Aunis', 'Saintonge', 'Poitou') and extract(year from p1.outdate_fixed) = 1787
and (p1.pointcall_action = 'Out' or p1.pointcall_action = 'In-Out' )
-- 309343.0

select sum(tonnage::float) 
from pointcall p1 
where extract(year from p1.outdate_fixed) = 1787
and (p1.pointcall_action = 'Out' or p1.pointcall_action = 'In-Out' ) 
and p1.pointcall_province not in ('Provence', 'Languedoc', 'Roussillon' , 'Isles de Corse')
-- 1675233.0
select  309343 / 1675233.0 as part_DFLR_navigation1787


select * from pointcall p1 where pointcall_province = 'Isles de Corse' limit 1

select  DFLR.sum / Atlantique.sum as part_DFLR_navigation1787
from 
		(select sum(tonnage::float) 
		from pointcall p1 
		where p1.pointcall_province in ('Aunis', 'Saintonge', 'Poitou') and extract(year from p1.outdate_fixed) = 1787
		and (p1.pointcall_action = 'Out' or p1.pointcall_action = 'In-Out' )) 
	as DFLR,
		(select sum(tonnage::float) 
		from pointcall p1 
		where extract(year from p1.outdate_fixed) = 1787
		and (p1.pointcall_action = 'Out' or p1.pointcall_action = 'In-Out' ) 
		and p1.pointcall_province not in ('Provence', 'Languedoc', 'Roussillon' , 'Isles de Corse')) 
	as Atlantique

select  DFLR.sum / Atlantique.sum as part_DFLR_navigation1787_versEtranger
from 
		(select sum(p1.tonnage::float) 
		from pointcall p1 , navigoviz.pointcall p2 
		where p1.pointcall_province in ('Aunis', 'Saintonge', 'Poitou') and extract(year from p1.outdate_fixed) = 1787
		and (p1.pointcall_action = 'Out' or p1.pointcall_action = 'In-Out' )
		and p2.state_1789_fr not in ('France', 'zone maritime') and (p2.data_block_leader_marker = 'T') 
		and p1.source_doc_id  = p2.source_doc_id ) 
	as DFLR,
		(select sum(p1.tonnage::float) 
		from pointcall p1 , navigoviz.pointcall p2 
		where extract(year from p1.outdate_fixed) = 1787
		and (p1.pointcall_action = 'Out' or p1.pointcall_action = 'In-Out' ) 
		and p1.pointcall_province not in ('Provence', 'Languedoc', 'Roussillon' , 'Isles de Corse')
		and p2.state_1789_fr not in ('France', 'zone maritime') and (p2.data_block_leader_marker = 'T') 
		and p1.source_doc_id  = p2.source_doc_id ) 
	as Atlantique

	-- part_DFLR_navigation1787_versColoniesAfrique : Il y aura Terre-Neuve aussi
select  DFLR.sum / Atlantique.sum as part_DFLR_navigation1787_versColoniesAfrique
from 
		(select sum(p1.tonnage::float) 
		from pointcall p1 , navigoviz.pointcall p2 
		where p1.pointcall_province in ('Aunis', 'Saintonge', 'Poitou') and extract(year from p1.outdate_fixed) = 1787
		and (p1.pointcall_action = 'Out' or p1.pointcall_action = 'In-Out' )
		and p2.state_1789_fr  in ('France', 'zone maritime') and (p2.data_block_leader_marker = 'T') 
		and (p2.substate_1789_fr like '%olonies%' or p2.partner_balance_supp_1789='Sénégal et Guinée')
		and p1.source_doc_id  = p2.source_doc_id ) 
	as DFLR,
		(select sum(p1.tonnage::float) 
		from pointcall p1 , navigoviz.pointcall p2 
		where extract(year from p1.outdate_fixed) = 1787
		and (p1.pointcall_action = 'Out' or p1.pointcall_action = 'In-Out' ) 
		and p1.pointcall_province not in ('Provence', 'Languedoc', 'Roussillon' , 'Isles de Corse')
		and p2.state_1789_fr  in ('France', 'zone maritime') and (p2.data_block_leader_marker = 'T') 
		and (p2.substate_1789_fr like '%olonies%' or p2.partner_balance_supp_1789='Sénégal et Guinée')
		and p1.source_doc_id  = p2.source_doc_id ) 
	as Atlantique
	
