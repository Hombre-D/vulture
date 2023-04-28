import requests
from bs4 import BeautifulSoup
import sqlite3

conn = sqlite3.connect('vulture.db')
c = conn.cursor()

ids = c.execute("select id, fixed from scrapers").fetchall()
count = 0
for id in ids:

    try:
        count += 1
        print(count)

        rootId = id[0]
        id = id[1]

        URL = "https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/commit/?id=" + id

        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")


        results = soup.find_all("div", {"class":"hunk"})

        for result in results:
            input = (rootId, id, result.getText().split("@@ ")[2])

            c.execute("INSERT INTO func_names VALUES (?, ?, ?)", input)
            conn.commit()
    
    except:
        print("Failed")

conn.close()
