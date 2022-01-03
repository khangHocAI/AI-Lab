def to_numeric_clauses(kb_list):
    list_clauses = []
    for kb in kb_list:
        sign = 1
        number = 0
        i = 0
        clauses = []
        while i<len(kb):
            if kb[i] == '-':
                sign = -1
                i+=1
            elif (kb[i] == 'O' and i+1<len(kb)-1 and kb[i+1] == 'R') or kb[i] =='\n':
                clauses.append(number)
                i+=2
            elif kb[i] == ' ':
                i+=1
            else:
                number = ord(kb[i])
                number *=sign
                sign = 1
                i+=1
                if i == len(kb):
                    clauses.append(number)
        list_clauses.append(clauses)
    list_clauses[-1][0] *= -1
    return list_clauses

def get_list_symbol(list_kb):
    list_symbols = []
    for kb in list_kb:
        for num in kb:
            symbol = abs(num)
            if symbol not in list_symbols:
                list_symbols.append(symbol)
    return sorted(list_symbols)


