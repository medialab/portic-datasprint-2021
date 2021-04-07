ici on s'occupe des navires qui sortent de DLFR vers l'Etranger

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
  
