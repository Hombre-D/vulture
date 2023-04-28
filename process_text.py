import sqlite3

conn = sqlite3.connect('vulture.db')
c = conn.cursor()

codeblocks = c.execute("select * from codes").fetchall()
count = 0

for codeblock in codeblocks:
    
    textList = codeblock[3].split("\n")
    removeList = []

    for text in textList:
        if text.lstrip().startswith("//") or text.lstrip().startswith("/*") or text.lstrip().startswith("*") or text.lstrip().startswith("#include"):
            removeList.append(text)

    outputList = [i for i in textList if i not in removeList]
    clean_code = "\n".join(outputList)

    input = (codeblock[0], codeblock[1], codeblock[2], clean_code, codeblock[4], codeblock[5])
    c.execute("INSERT INTO clean_codes VALUES (?, ?, ?, ?, ?, ?)", input)
    conn.commit()
    count += 1
    print(count)

conn.close()