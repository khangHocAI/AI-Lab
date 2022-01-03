import math
from utils import print_clauses
def check_is_existed(new_clauses, list_kb):
    if new_clauses in list_kb:
        return True
    return False
def pl_resolve(clause_1, clause_2):
    resolve_position = []
    new_clause = []
    decay = 0
    for v_1 in clause_1:
        flag = False
        for v_2 in clause_2:
            if v_1 + v_2 == 0:
                resolve_position.append(v_2)
                flag = True
                break
            if v_1 == v_2:
                resolve_position.append(v_2)
                if len(clause_1) == 1:
                    decay = 2
                else:
                    decay = 1
                break
        if not flag:
            new_clause.append(v_1)
    if decay == 0:
        for v in clause_2:
            if v not in resolve_position:
                new_clause.append(v)
    elif decay ==1:
        new_clause = []
        new_clause.extend(clause_2)
    else:
        new_clause = []
        new_clause.extend(clause_1)
    return new_clause

def pl_resolution(list_kb):
    start_position = 0
    while True:
        new_kb = []    
        for i in range (0, len(list_kb)-1):
            for j in range (max(i+1, start_position), len(list_kb)):
                new_clauses = pl_resolve(list_kb[i], list_kb[j])
                new_clauses = sorted(new_clauses, key=abs)
                if len(new_clauses) == 0:
                    print(len(new_kb)+1)
                    print_clauses(new_kb)
                    print("{}")
                    return True
                elif len(list_kb[i])+len(list_kb[j])-len(new_clauses) < min(len(list_kb[i]),len(list_kb[j])):
                    continue
                elif not check_is_existed(new_clauses, list_kb) and not check_is_existed(new_clauses, new_kb):
                    new_kb.append(new_clauses)
        print(len(new_kb))
        print_clauses(new_kb)
        if len(new_kb) == 0:
            break
        start_position = len(list_kb)
        list_kb = list_kb + new_kb
    return False