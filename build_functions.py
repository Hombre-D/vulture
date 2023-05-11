import sqlite3

# These two amazing functions were rebuilt from what I found at:
# https://stackoverflow.com/questions/55078713/extract-function-code-from-c-sourcecode-file-with-python
# Thanks, Stack Overflow user 'user8092240'!
def get_line_number(code, func_name):
    lines = code.splitlines()
    for line in lines:
        if line.startswith(func_name):
            return lines.index(line)
    return None

def process_code(code, line_number):
    output_list = []

    count_bracket = 0

    input_lines = code.splitlines()
    lines = input_lines[line_number:]

    for line in lines:
        output_list.append(line)
        if line.count("{") > 0:
            count_bracket += line.count("{")
    
        if line.count("}") > 0:
            count_bracket -= line.count("}")

        if count_bracket == 0 and lines.index(line) > 0:
            if len(output_list) > 1:
                return '\n'.join(output_list)
            else:
                return None
        

conn = sqlite3.connect('vulture.db')
c = conn.cursor()
count = 0

# Got 19387 pairs from our scrape, hence the range.
for i in range(1, 19387):
    id_list = c.execute("select codeIndex, rootID, id, code, url, isVulnerable from clean_codes where codeIndex = ?", [i]).fetchall()
    func_list = c.execute("select distinct func_name from func_names where id = ?", [id_list[0][2]]).fetchall()
    
    for func in func_list:
        code_a = id_list[0]
        code_b = id_list[1]
        function_a = ""
        function_b = ""

        try:
            line_nbr_a = get_line_number(code_a[3], func[0])
            line_nbr_b = get_line_number(code_b[3], func[0])

            if line_nbr_a is not None and line_nbr_b is not None:
                function_a = process_code(code_a[3], line_nbr_a)
                function_b = process_code(code_b[3], line_nbr_b)
            
            if function_a.count("{") > 0 and function_b.count("{") > 0 and function_a != function_b:
                a_tuple = (code_a[0], code_a[1], code_a[2], function_a, func[0], code_a[5])
                b_tuple = (code_b[0], code_b[1], code_b[2], function_b, func[0], code_b[5])
                c.execute("insert into functions values (?, ?, ?, ?, ?, ?)", a_tuple)
                c.execute("insert into functions values (?, ?, ?, ?, ?, ?)", b_tuple)
                conn.commit()
        except:
            print("Failed")
    count += 1
    print(count)


conn.close()



