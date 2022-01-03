
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
            clause_to_print = "{}"
        print(clause_to_print)
                
def compare(clause_1, clause_2):
    if len(clause_1) != len(clause_2):
        return False
    for i in range (len(clause_1)):
        if clause_1[i] != clause_2[i]:
            return False
    return True
def join_two_clauses(clause_1, clause_2):
    result = []
    result.extend(clause_1)
    result.extend(clause_2)
    set_result = set(result)
    return list(set_result)

def tautology(clause):
    for symbol in clause:
        if -symbol in clause:
            return True
    return False
def update_clauses(clauses, symbol):
    result = []
    for clause in clauses:
        if symbol in clause or -symbol in clause:
            continue
        else:
            result.append(clause)
    for i in range (len(result)-1):
        for j in range (i+1, len(result)):
            if compare(result[i], result[j]):
                result.remove(result[i])
                break
    return result

def extend_clauses(clauses, new_clauses):
    result = clauses
    for new_clause in new_clauses:
        is_existed = False
        for clause in clauses:
            if compare(new_clause, clause):
                is_existed = True
                break
        if not is_existed:
            result.append(new_clause)
    return result        
        

def dp(clauses, symbols):
    for symbol in symbols:
        new_clauses = []
        for i in range (len(clauses)-1):
            for j in range (i+1, len(clauses)):
                new_clause = []
                flag = False
                if symbol in clauses[i] and -symbol in clauses[j]:
                    clauses[i].remove(symbol)
                    clauses[j].remove(-symbol)
                    new_clause = join_two_clauses(clauses[i], clauses[j])
                    flag = True
                elif -symbol in clauses[i] and symbol in clauses[j]:
                    clauses[i].remove(-symbol)
                    clauses[j].remove(symbol)
                    new_clause = join_two_clauses(clauses[i], clauses[j])
                    flag = True
                if flag and not tautology(new_clause):
                    new_clauses.append(new_clause)
        clauses = update_clauses(clauses, symbol)
        clauses= extend_clauses(clauses, new_clauses)
        print('resolved by symbol ', symbol)
        if len(clauses) > 0:
            print(len(clauses))
            print_clauses(clauses)
            for clause in clauses:
                if len(clause) == 0:
                    return True                   
    return False