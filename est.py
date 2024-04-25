import json

# RUN QUERIES

queries = []
combs = json.loads(open('queries.json', 'r+').read())

for comb in combs:
    comb_string = ""
    for c in comb:
        comb_string += comb[c] + ' and '
    if comb_string[-5:] == ' and ':
        comb_string = comb_string[:-5]
    queries.append(comb_string)

open('actual_queries.json', 'w+').write(json.dumps(queries))






