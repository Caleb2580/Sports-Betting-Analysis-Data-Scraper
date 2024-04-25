import requests
import pandas as pd
import json


def get_data(que):
    pre_link = 'https://killersports.com/mlb/query'

    # '=' = '%3D'
    # '<' = '%3C'
    # '>' = '%3E'
    # '!' = '%21'

    replace_dict = {
        '=': '%3D',
        '<': '%3C',
        '>': '%3E',
        '!': '%21',
        ':': '%3A',
        ';': '%3B',
        '?': '%3F',
        '@': '%40',
        ' ': '+',
    }

    payload = {
        'output': 'default',
        'sdql': que,
        'submit': '  S D Q L!',
    }

    # Encode to html
    for key in payload:
        for to_replace in replace_dict:
            payload[key] = payload[key].replace(to_replace, replace_dict[to_replace])

    # Create final link
    final_link = pre_link + '?'
    for key in payload:
        final_link += key + '=' + payload[key] + '&'

    # Get result
    r = requests.get(final_link)

    html = r.text

    # # Write html to file
    open('index.html', 'w+', encoding='utf-8').write(html)

    # Shorten to correct table
    html = html[html.find('<script>'):]
    # html = html[html.find('<table>'):]

    # Find betting html
    tf_betting_start = '<!--Start Records Row--><TR><TD>\n'
    tf_betting_end = '</TD></TR><!--End Records Row-->'
    try:
        betting_html = html[html.find(tf_betting_start) + len(tf_betting_start):html.find(tf_betting_end)]
    except:
        betting_html = None

    open('btext.txt', 'w+', encoding='utf-8').write(betting_html)

    b_i = None

    if betting_html is not None:
        b_i = pd.read_html(betting_html)

    # Find stats html
    tf_stats_start = '<!--Start Stats Row--><TR><TD>\n'
    tf_stats_end = '</TD></TR><!--End Stats Row-->'
    try:
        stats_html = html[html.find(tf_stats_start) + len(tf_stats_start):html.find(tf_stats_end)]
    except:
        stats_html = None

    open('stext.txt', 'w+', encoding='utf-8').write(stats_html)

    s_i = None

    if stats_html is not None:
        s_i = pd.read_html(stats_html)

    return b_i[0], s_i[0]


# queries = ['season>=2017 and p:runs=-1',
#             'season>=2017 and p:runs=0',
#             'season>=2017 and p:runs=1',
#             'season>=2017 and p:runs=2',
#             'season>=2017 and p:runs=3',
#             'season>=2017 and p:runs=4',
#             # add up to 20 queries here
# ]

# queries = []
# combs = json.loads('queries.json')
# print(combs[0])

queries = json.loads(open('actual_queries.json', 'r+').read())


# Use get_data() method for each query and display the results
for i, raw_query in enumerate(queries):
    query = 'season >= 2017 and ' + raw_query
    print(f"\nQuery {i+1}\n-------------\n{query}")
    try:
        betting_info, stats_info = get_data(query)
        ona = betting_info.at[1, 3]
        ona = ona.replace(',', '')
        ou = betting_info.at[2, 3]
        ou = ou.replace(',', '')
        ona_pos_ind = ona.find('+')
        ou_pos_ind = ou.find('+')
        ona_pos_val = None
        ou_pos_val = None
        if ona_pos_ind >= 0:
            ona_pos_val = ona[ona_pos_ind+2:]
            try:
                ona_pos_val = ona_pos_val[:ona_pos_val.find(' /')]
            except Exception as e:
                pass
            ona_pos_val = int(ona_pos_val)
        if ou_pos_ind >= 0:
            ou_pos_val = ou[ou_pos_ind+2:]
            try:
                ou_pos_val = ou_pos_val[:ou_pos_val.find(' ')]
            except Exception as e:
                pass
            ou_pos_val = int(ou_pos_val)
        if ona_pos_val is not None and ona_pos_val > 2000:
            print('!!!!!!!!!!!!!!!!!!!!!!')
            print(query + ' || ' + str(ona_pos_val))
            print('!!!!!!!!!!!!!!!!!!!!!!')
            doc = open('best_queries.txt', 'r+').read()
            doc += '\n' + query + ' || ' + str(ona_pos_val)
            open('best_queries.txt', 'w+').write(doc)
        elif ona_pos_val is not None and ona_pos_val > 100:
            print(query + ' || ' + str(ona_pos_val))
        if ou_pos_val is not None and ou_pos_val > 2000:
            print('!!!!!!!!!!!!!!!!!!!!!!')
            print(query + ' || ' + str(ou_pos_val))
            print('!!!!!!!!!!!!!!!!!!!!!!')
            doc = open('best_queries.txt', 'r+').read()
            doc += '\n' + query + ' || ' + str(ou_pos_val)
            open('best_queries.txt', 'w+').write(doc)
        elif ou_pos_val is not None and ou_pos_val > 100:
            print(query + ' || ' + str(ou_pos_val))
        # print('\nBetting Info\n-------------\n', betting_info)
        # print('\nStats Info\n-------------\n', stats_info)
    except Exception as e:
        print(f"Error occurred while processing query {i+1}: {e}")