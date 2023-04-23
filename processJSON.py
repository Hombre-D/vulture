import json
import os
import sqlite3

base_dir = 'linux'

all_scrapers = []

for file in os.listdir(base_dir):
    if 'json' in file:
        json_path = os.path.join(base_dir, file)
        f = open(json_path)
        data = json.load(f)
        id = data['id']
        introduced = data['affected'][0]['ranges'][0]['events'][0]['introduced']
        limit = data['affected'][0]['ranges'][0]['events'][1]['limit']

        scraper = (id, introduced, limit)
        all_scrapers.append(scraper)

        f.close()

conn = sqlite3.connect('vulture.db')
c = conn.cursor()
c.executemany("INSERT INTO scrapers VALUES (?, ?, ?)", all_scrapers)
conn.commit()
conn.close()