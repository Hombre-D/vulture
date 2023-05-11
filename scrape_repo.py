# GSD-2022-1004215|d08e973a77d128b25e01a08c34d89593fdf222da|ffb6cc6601ec7c8fa963dcf76025df4a02f2cf5c
# https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/commit/?id=42e69521ee1fa5abf21f478d147d06bbfe6bf6a8

import requests
from bs4 import BeautifulSoup
import sqlite3
import traceback

conn = sqlite3.connect('vulture.db')
c = conn.cursor()

ids = c.execute("select fixed, id from scrapers").fetchall()
count = 0
codeIndex = 0

for id in ids:
    rootID = id[1]
    id = id[0]
    URL = "https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/commit/?id=" + id

    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find_all('a')

    # We want to read the results backwards, as the correction file / vulnerable file to scrape are in that order.
    results.reverse()
    
    count += 1
    print(count)

    try:
        for result in results:
            index = results.index(result)
            result = result.get('href')
            if id in result:
                
                nvURL = "https://git.kernel.org/" + result
                vURL = "https://git.kernel.org/" + results[index+1].get('href')

                if "tree" in nvURL and "tree" in vURL:
                    codeIndex += 1

                    nvURL = nvURL.replace("tree", "plain")
                    vURL = vURL.replace("tree", "plain")

                    page = requests.get(nvURL)
                    soup = BeautifulSoup(page.content, "html.parser")
                    nvString = soup.getText()
                    nv = (codeIndex, rootID, id, nvString, nvURL, 0)
                    c.execute("INSERT INTO codes VALUES (?, ?, ?, ?, ?, ?)", nv)

                    page = requests.get(vURL)
                    soup = BeautifulSoup(page.content, "html.parser")
                    vString = soup.getText()
                    v = (codeIndex, rootID, vURL.split("?id=")[1], vString, vURL, 1)
                    c.execute("INSERT INTO codes VALUES (?, ?, ?, ?, ?, ?)", v)
                    conn.commit()
    except:
        print("Failed to execute!")
        traceback.print_exc()

conn.close()
