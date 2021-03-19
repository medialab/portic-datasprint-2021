from poitousprint import Toflit

toflit_client = Toflit()

results = toflit_client.get_product_terms()['data']

print(len(results), results[0:10])