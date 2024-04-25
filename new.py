import math
import re
from time import sleep

def get_other_indexes(ns, n):
    rs = []
    for i in range(0, len(ns)):
        if i is not n:
            rs.append(i)
    return rs


# print(get_other_indexes(numbers, 1))


def get_results_with_repetition(ns, rep_num):
    res = []

    for i in ns:
        res.append([i])

    for w in range(0, rep_num-1):
        new_res = []
        for i in res:
            for q in ns:
                nw = i.copy()
                nw.append(q)
                new_res.append(nw)
        res = new_res.copy()

    return res


def get_results_without_repetition(ns):
    res_ids = []

    for i in range(0, len(ns)):
        res_ids.append([i])

    for i in range(0, len(ns)):
        for q in range(0, len(ns)):
            if q is not i:
                nw = [i, q]
                if nw not in res_ids:
                    res_ids.append(nw)

    for i in range(1, len(ns)):
        for q in range(0, len(res_ids)):
            if i not in res_ids[q]:
                for ind_to_try in range(0, len(res_ids[q])):
                    nw = res_ids[q][0:ind_to_try].copy()
                    nw.append(i)
                    nw = nw + res_ids[q][ind_to_try:].copy()
                    if nw not in res_ids:
                        res_ids.append(nw)
                nw_e = res_ids[q].copy()
                nw_e.append(i)
                if nw_e not in res_ids:
                    res_ids.append(nw_e)

    res = []

    for i in res_ids:
        new = []
        for q in i:
            new.append(ns[q])
        res.append(new)

    return res, res_ids


def get_results(ns):
    ress, ress_ids = get_results_without_repetition(ns)

    final_ress = {}

    symbols_ids = [0, 1, 2, 3]

    print('-')
    ind = 0
    for res in ress:
        if len(res) == 1:
            if res[0] in final_ress.keys():
                final_ress[res[0]].append(list([ress_ids[ind], [-1]]))
            else:
                final_ress[res[0]] = list([[ress_ids[ind], [-2]]])
        elif len(res) > 1:
            rep_ress = get_results_with_repetition(symbols_ids, len(res) - 1)
            for rep_res in rep_ress:
                res_to_use = res.copy()
                calc_str = ''
                for i in range(0, len(res_to_use)-1):
                    sym = ''
                    if rep_res[i] == 0:
                        sym = '+'
                    elif rep_res[i] == 1:
                        sym = '-'
                    elif rep_res[i] == 2:
                        sym = '*'
                    elif rep_res[i] == 3:
                        sym = '/'
                    calc_str += str(res_to_use[i]) + sym
                calc_str += str(res_to_use[-1])
                calc_arr = re.split('\+|\-|\*|\/', calc_str)
                print('c', calc_str)
                print('ca', str(calc_arr))
                o = 0
                stop = False
                if len(calc_arr) > 1:
                    while True:
                        print('cccaaa', calc_arr)
                        print('cccsss', calc_str)
                        if o < len(calc_arr):
                            sym = calc_str[calc_str.find(calc_arr[o])-1:calc_str.find(calc_arr[o])]
                            print('sym', sym)
                            if sym == '*':
                                new_val = float(calc_arr[o-1]) * float(calc_arr[o])
                                if 100000000 <= new_val or new_val <= .0001:
                                    stop = True
                                    break
                                print('ccccc', calc_arr)
                                to_find = str(calc_arr[o-1]) + '*' + str(calc_arr[o])
                                print(to_find)
                                calc_str = calc_str[:calc_str.find(to_find)] + str(new_val) + calc_str[calc_str.find(to_find) + len(to_find):]
                                calc_arr[o - 1] = new_val
                                calc_arr.pop(o)
                                print(new_val)
                            elif sym == '/':
                                new_val = float(calc_arr[o - 1]) / float(calc_arr[o])
                                if 100000000 <= new_val or new_val <= .0001:
                                    stop = True
                                    break
                                to_find = str(calc_arr[o - 1]) + '/' + str(calc_arr[o])
                                print(new_val)
                                calc_str = calc_str[:calc_str.find(to_find)] + str(new_val) + calc_str[calc_str.find(to_find) + len(to_find):]
                                calc_arr[o - 1] = new_val
                                calc_arr.pop(o)
                            else:
                                o += 1
                            print(calc_str)
                        else:
                            break

                print(calc_str)

                sum_res = eval(calc_str)

                # sleep(.2)

                if not stop:
                    if sum_res in final_ress.keys():
                        final_ress[sum_res].append([ress_ids[ind], rep_res])
                    else:
                        final_ress[sum_res] = [ress_ids[ind], rep_res]
        ind += 1

    # for s in final_ress:
    #     print(s, final_ress[s])

    return final_ress


def get_res(ns, f, s):

    res_to_use = []

    for y in f:
        res_to_use.append(ns[y])

    calc_str = ''
    for i in range(0, len(res_to_use) - 1):
        sym = ''
        if s[i] == 0:
            sym = '+'
        elif s[i] == 1:
            sym = '-'
        elif s[i] == 2:
            sym = '*'
        elif s[i] == 3:
            sym = '/'
        calc_str += str(res_to_use[i]) + sym
    calc_str += str(res_to_use[-1])
    print(calc_str)
    sum_res = eval(calc_str)

    return sum_res


# numbers = [5500000, .06, 102.3, 2, 10]

numbers = [4000000, .05, 1.01023, 2, 10, 1]

results = get_results(numbers)

print(results)

true_res = 165000

print('-\n-\n-\n-\n-\n-\n-\n-\n-\n-\n-\n-\n-\n-\n-\n')

# print(results[true_res])

print('-')

ar = [[[1, 0, 3], [2, 3]], [[0, 1, 3], [2, 3]], [[0, 3, 1], [3, 2]], [[1, 3, 0], [3, 2]]]

for a in ar:
    print(a, get_res(numbers, a[0], a[1]))

# print(get_res(numbers, [1, 0, 3], [2, 3]))
#
# print(get_res(numbers, [1, 0, 3], [2, 3]))


















