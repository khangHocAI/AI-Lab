from utils import to_numeric_clauses, print_clauses
from pl_resolution import pl_resolution
import time
f = open("test_5.txt", 'r')
query = f.readline()
num_kbs = int(f.readline())
list_kb = []
for _ in range (num_kbs):
    list_kb.append(f.readline())
list_kb.append(query)
list_kb = to_numeric_clauses(list_kb)
print_clauses(list_kb)
start_time = time.time()
if pl_resolution(list_kb):
    print('YES')
else:
    print('NO')
print("Time runs: ", time.time()-start_time, " (second)")
# pl_resolve(list_kb[0], list_kb[2])