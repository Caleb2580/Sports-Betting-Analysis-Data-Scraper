import itertools
import json


def generate_query_combinations(query_dict):
    keys = query_dict.keys()
    values = query_dict.values()
    combinations = []
    for combination in itertools.product(*values):
        combinations.append(dict(zip(keys, combination)))
    return combinations


def generate_combinations(items):
    all_combinations = []
    # for length in range(1, len(items)+1):
    for length in range(1, 4):
        for combination in itertools.combinations(items, length):
            all_combinations.append(combination)
    return all_combinations


eq = ['<=', '>=', '=']

ps = {'runs': (0, 20), 'strike outs': (2, 15)}

gr = [
    'p:', 'pp:', 'ppp:',  # 'pppp:', 'ppppp:', 'op:', 'opp:', 'oppp:', 'opppp:', 'oppppp:', 'P:', 'PP:', 'PPP:', 'PPPP:', 'PPPPP:',
]

new_list = {}
for g in gr:
    cur_list = []
    for p in ps:
        for e in eq:
            for q in range(ps[p][0], ps[p][1]):
                cur_list.append(g + p + e + str(q))
    new_list[g] = cur_list.copy()


# for comb in new_list:
#     print(comb)

print('Generating combos')
combs = generate_query_combinations(new_list)

# print(combs)

# lists = 'eq = ' + json.dumps(eq) + '\n\n\nps = ' + json.dumps(ps) + '\n\n\ngr = ' + json.dumps(gr) + '\n\n\nnew_list = ' + json.dumps(new_list) + '\n\n\ncombs = ' + json.dumps(combs)

# print(len(combs))
#
# for comb in combs:
#     print(str(comb) + '\n\n\n')
#
#
open('queries.json', 'w+').write(json.dumps(combs))




















