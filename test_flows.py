from client import Api

client = Api()

results = client.toflit.get_flows({
  "start_year": "1789",
  "end_year": "1790"
})

print("taille : ", len(results))
print("premier item :")
print(results[0])