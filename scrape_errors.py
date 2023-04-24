import requests
from bs4 import BeautifulSoup
import sqlite3

# id = "2c19945ce8095d065df550e7fe350cd5cc40c6e6"
id = "2c8aeffc7c586d53e1d380f010bdca4f710f2480"

URL = "https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/commit/?id=" + id

page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")

results = soup.find_all('a')
results.reverse()
# results = soup.find_all("div", {"class":"hunk"})
# results2 = soup.find_all("div", {"class":"del"})

for result in results:
    print(result)

# for result in results2:
#     print(result)