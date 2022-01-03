from utils import to_numeric_clauses, get_list_symbol
from davis_putnam import dp, print_clauses
import time
f = open("test_5.txt", 'r')
query = f.readline()
num_kbs = int(f.readline())
list_kb = []
for _ in range (num_kbs):
    list_kb.append(f.readline())
list_kb.append(query)
print(list_kb)
list_kb = to_numeric_clauses(list_kb)
print(list_kb)
list_symbols = get_list_symbol(list_kb)
model = {}
start_time = time.time()
if dp(list_kb, list_symbols):
    print("YES")
else:
    print('NO')
print('Time runs: ', time.time()-start_time, " (second)")