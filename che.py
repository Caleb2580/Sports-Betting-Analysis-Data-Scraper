import json
import pandas as pd
import requests


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


best_queries = open('best_queries.txt', 'r+').read().splitlines()

for q in best_queries:
    betting_info, stats_info = get_data(q[:q.find(' ||')])

    ona = betting_info.at[1, 3]
    ona = ona.replace(',', '')
    ou = betting_info.at[2, 3]
    ou = ou.replace(',', '')

    ona_roi = betting_info.at[1, 4]
    ona_roi = ona_roi.replace(',', '')
    ou_roi = betting_info.at[2, 4]
    ou_roi = ou_roi.replace(',', '')

    print(ona_roi)
    print(ou_roi)

    ona_roi_val = max([float(ona_roi[5:ona_roi.find('% /')]), float(ona_roi[ona_roi.find('/ ') + 2:-1])])
    ou_roi_val = max([float(ou_roi[5:ou_roi.find('% /')]), float(ou_roi[ou_roi.find('/ ') + 2:-1])])

    ona_pos_ind = ona.find('+')
    ou_pos_ind = ou.find('+')
    ona_pos_val = None
    ou_pos_val = None
    if ona_pos_ind >= 0:
        ona_pos_val = ona[ona_pos_ind + 2:]
        try:
            if ona_pos_val.find(' /') > 0:
                ona_pos_val = ona_pos_val[:ona_pos_val.find(' /')]
        except Exception as e:
            pass
        ona_pos_val = int(ona_pos_val)
    if ou_pos_ind >= 0:
        ou_pos_val = ou[ou_pos_ind + 2:]
        try:
            if ou_pos_val.find(' /') > 0:
                ou_pos_val = ou_pos_val[:ou_pos_val.find(' /')]
        except Exception as e:
            pass
        ou_pos_val = int(ou_pos_val)

    print(q)
    print(ona_pos_val)
    print(ou_pos_val)
    query_final_string = q[:q.find(' ||')] + ''
    query_final_string += ' || ' + 'on/against = ' + str(ona_pos_val) + ', ' + str(ona_roi_val) + '% || over/under = ' + str(ou_pos_val) + ', ' + str(ou_roi_val) + '%'
    comp = open('complete_queries.txt', 'r+').read()
    comp += query_final_string + '\n'
    open('complete_queries.txt', 'w+').write(comp)



















