import spacy
import pandas as pd
from collections import defaultdict

name_date = defaultdict(lambda: {'dates': [], 'types': [], 'links': []})
new_path = 'D:/myCodeP/LearnBasic/design_team_info1.txt'

nlp = spacy.load('en_core_web_sm')

with open('D:/myCodeP/LearnBasic/design_team_info.txt', 'r', encoding='utf-8') as file:
    text = file.read()

paragraphs = text.strip().split('\n\n')


with open(new_path, 'w', encoding='utf-8') as upfile:
    for p in paragraphs:
        doc = nlp(p)

        lines = p.strip().split('\n')
        team_name = lines[0]
        team_type = lines[1]
        team_link = lines[-1]

        date_entities = [ent.text for ent in doc.ents if ent.label_ == 'DATE']
        
        if date_entities:
            updated_paragraph = p + f" [DATE: {', '.join(date_entities)}]"

        else:
            updated_paragraph = p

        name_date[team_name]['dates'].extend(date_entities)
        type_list = [t.strip() for t in team_type.split(',')]
        name_date[team_name]['types'].extend(type_list)
        upfile.write(updated_paragraph + '\n\n')
        name_date[team_name]['links'].append(team_link)

excel_rows = []
for team, info in name_date.items():
    row = {
        'Team Name': team,
        'Dates': ', '.join(set(info['dates'])),
        'Types': ', '.join(set(info['types'])),
        'Links': ', '.join(set(info['links']))
    }
    print(info['types'])
    excel_rows.append(row)

df = pd.DataFrame(excel_rows)
df.to_excel('D:/myCodeP/LearnBasic/name_time.xlsx', index=False)






