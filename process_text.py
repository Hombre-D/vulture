import sqlite3

conn = sqlite3.connect('vulture.db')
c = conn.cursor()

codeblocks = c.execute("select * from codes").fetchall()

for codeblock in codeblocks:

    textList = codeblock[2].split("\n")
    removeList = []

    for text in textList:
        if text.startswith("//") or text.startswith("/*") or text.startswith(" *") or text.startswith("#include"):
            removeList.append(text)

    outputList = [i for i in textList if i not in removeList]
    clean_code = "\n".join(outputList)

    input = (codeblock[0], codeblock[1], clean_code, codeblock[3])
    c.execute("INSERT INTO clean_codes VALUES (?, ?, ?, ?)", input)
    conn.commit()

conn.close()