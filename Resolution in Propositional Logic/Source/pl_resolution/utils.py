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

def print_clauses(clauses):
    for clause in clauses:
        if len(clause) >0:
            clause_to_print = ''
            for v in clause:
                if v < 0:
                    clause_to_print += '-'
                if v != clause[-1]:
                    clause_to_print += chr(abs(v)) + ' OR '
                else:
                    clause_to_print += chr(abs(v))
        else:
            clause_to_print = clause
        print(clause_to_print)