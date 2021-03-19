from poitousprint import Toflit

toflit_client = Toflit()

results = toflit_client.get_flows({
  "start_year": "1789",
  "end_year": "1798", 
  "product_orthographic":"vin",
  # 'customs_region':'La Rochelle',
  "columns":['year', 'customs_region', 'product_orthographic', 'partner_orthographic','partner_grouping']
})

print("taille : ", len(results))
print("premier item :")
print(results[0])