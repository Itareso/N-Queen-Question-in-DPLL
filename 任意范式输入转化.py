from copy import deepcopy
from sympy import *


'''
$$ Note::
$ The bottom test sentences are CNF of N-Queen-Question, as README introduce
$ If other SAT problem are requied, modify the 'cnf' in 'transform()'
$$
'''


N = 8
dots=[[0 for i in range(N)] for i in range(N)]
for i in range(N):
    for j in range(N):
        dots[i][j] = symbols(f"p[{i}][{j}]")
#print("dots = \n", dots, end='\n\n')
'''
$ dots[i][j] 将所有命题名称符号化
$ p[i][j] 才可以作为命题输入 DPLL Solver.py
'''


q = []
def transform(q: list, cnf: list[str]):
    '''
    q :: 输出的/用于被添加子句的CNF
    cnf :: 自然语言/非展开的CNF
    '''
    lens = len(cnf)
    tmp = []
    if cnf[0] == 'a':
        for j in range(eval(cnf[2]),eval(cnf[3])+1):
            tmp = deepcopy(cnf)
            for k in range(4,lens):
                tmp[k] = tmp[k].replace(cnf[1],str(j))
                #print(tmp)
            transform(q,tmp[4:lens])
    elif cnf[0] == 'e':
        tmplens = len(q)
        q.append(deepcopy([]))
        for j in range(eval(cnf[2]),eval(cnf[3])+1):
            tmp = deepcopy(cnf)
            for k in range(4,lens):
                tmp[k] = tmp[k].replace(cnf[1],str(j))
                #print(tmp)
            transform(q[tmplens],tmp[4:lens])
    elif cnf[0] == '+':
        q.append(dots[eval(cnf[1])-1][eval(cnf[2])-1])
    elif cnf[0] == '-':
        q.append(~dots[eval(cnf[1])-1][eval(cnf[2])-1])
    elif cnf[0] == 'v':
        tmplens = len(q)
        q.append(deepcopy([]))
        transform(q[tmplens],cnf[1:4])
        transform(q[tmplens],cnf[4:7])



'''------------------------------------------------------------

$ As N = 8, following test-q may generate expaned CNF
$ The output is set as <class 'sympy.core.symbol.Symbol'>
$ So it can be directly used in DPLL Solver.py
'''
transform(q,['a','i','1','N','e','j','1','N','+','i','j'])
transform(q,['a','i','1','N','a','j','1','N-1','a','k','j+1','N','v','-','i','j','-','i','k'])
transform(q, ['a', 'j', '1', 'N', 'a', 'i', '1', 'N-1', 'a', 'k', 'i+1', 'N', 'v', '-', 'i', 'j', '-', 'k', 'j'])
transform(q, ['a', 'I', '2', 'N', 'a', 'j', '1', 'N-1', 'a', 'k', '1', "min(I-1, N-j)", "v", "-", "I", "j", "-", "I-k", "j+k"])
transform(q, ['a', 'I', '1', 'N', 'a', 'j', '1', 'N-1', 'a', 'k', '1', "min(N-I, N-j)", "v", "-", "I", "j", "-", "I+k", "j+k"])
#print(q)
'''
$$ Q1 \wedge Q2 \wedge Q3 \wedge Q4 \wedge Q5
------------------------------------------------------------'''
