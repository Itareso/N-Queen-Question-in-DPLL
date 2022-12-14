'''---------------------------
        @ DPLL solver
---------------------------'''

'''

$ Only calculate whether satisfiable
$ Only responsible for the given CNF
$ Only by introducing its negation form could the solver generate further result

'''


from sympy import symbols
from typing import *
from copy import deepcopy
##
from sympy.logic.boolalg import Not
from sympy import Symbol
##

class CNF:
    '''
    简洁化每个子句
    单位传播
    查找下一个确定赋值的文字
    (若上一步不成功) 随机查找下一个待赋值文字 (优化为先随机子句短的)
    判断是否为可满足
    '''
    def __init__(self, q):
        self.cnf = q        # 将q实例化, 后面不再使用q而是self.cnf
        self.remove_same_literal()
    
    def remove_same_literal(self):
        for clause in self.cnf:
            for literal in clause:
                if ~literal in clause:
                    self.cnf.remove(clause)
                    break
    def unit_spread(self, single_literal):
        for clause in list(self.cnf):
            if single_literal in clause:
                self.cnf.remove(clause)
            elif ~single_literal in clause:
                clause.remove(~single_literal)

    def find_single_literal(self):
        for clause in self.cnf:
            '''
            if len(clause) == 0: # 需要彻底返回 False
            '''
            if len(clause) == 1:
                return clause[0]
        else:
            return None

    def casually_return_literal(self):
        return list(self.cnf[0])[0]     # 考虑 [[p11, p12], ...] 与 [p11, ...] 两种情况

    def check(self, end_all = "off"):
        if end_all == "on":
            return False
        if self.cnf != []:        # self.cnf = [[], ...] 或 其他正常情况
            if [] in self.cnf:
                return False
            return None
        else:
            return True         # self.cnf = []


def DPLL(current_cnf: CNF):
    # current_cnf 是当前计算的类
    # current_cnf.cnf 是这个类里cnf的名字
    single_literal = current_cnf.find_single_literal()
    while single_literal != None:
        current_cnf.unit_spread(single_literal)
        single_literal = current_cnf.find_single_literal()
    check_result = current_cnf.check()
    if check_result == True:
        return True
    elif check_result == False:
        return False
    else:
        single_literal = current_cnf.casually_return_literal()
        new_cnf = CNF(deepcopy(current_cnf.cnf))
        new_cnf.unit_spread(single_literal)
        if DPLL(new_cnf) == True:
            return True
        else:
            new_cnf = CNF(deepcopy(current_cnf.cnf))
            new_cnf.unit_spread(~single_literal)
            if DPLL(new_cnf) == True:
                return True
            else:
                return False


'''

$ The following are testing with known-solution-4QueenProblem
    @ This test could run directly

$ Use 'symbol()' to transform variables into symbols
$ In order to show answer neatly
$ Following CNF of 4QueenProblem is generated by 'CNF Expansion.py'
$ The two solution are introduced artificially
$ This sample exists here only to find if the solver works 

'''

N = 8
p = [[0 for i in range(N)] for i in range(N)]
for i in range(N):
    for j in range(N):
        p[i][j] = symbols(f"p{i}{j}")

q = [[p[0][0], p[0][1], p[0][2], p[0][3]], [p[1][0], p[1][1], p[1][2], p[1][3]], [p[2][0], p[2][1], p[2][2], p[2][3]], [p[3][0], p[3][1], p[3][2], p[3][3]], [~p[0][0], ~p[0][1]], [~p[0][0], ~p[0][2]], [~p[0][0], ~p[0][3]], [~p[0][1], ~p[0][2]], [~p[0][1], ~p[0][3]], [~p[0][2], ~p[0][3]], [~p[1][0], ~p[1][1]], [~p[1][0], ~p[1][2]], [~p[1][0], ~p[1][3]], [~p[1][1], ~p[1][2]], [~p[1][1], ~p[1][3]], [~p[1][2], ~p[1][3]], [~p[2][0], ~p[2][1]], [~p[2][0], ~p[2][2]], [~p[2][0], ~p[2][3]], [~p[2][1], ~p[2][2]], [~p[2][1], ~p[2][3]], [~p[2][2], ~p[2][3]], [~p[3][0], ~p[3][1]], [~p[3][0], ~p[3][2]], [~p[3][0], ~p[3][3]], [~p[3][1], ~p[3][2]], [~p[3][1], ~p[3][3]], [~p[3][2], ~p[3][3]], [~p[0][0], ~p[1][0]], [~p[0][0], ~p[2][0]], [~p[0][0], ~p[3][0]], [~p[1][0], ~p[2][0]], [~p[1][0], ~p[3][0]], [~p[2][0], ~p[3][0]], [~p[0][1], ~p[1][1]], [~p[0][1], ~p[2][1]], [~p[0][1], ~p[3][1]], [~p[1][1], ~p[2][1]], [~p[1][1], ~p[3][1]], [~p[2][1], ~p[3][1]], [~p[0][2], ~p[1][2]], [~p[0][2], ~p[2][2]], [~p[0][2], ~p[3][2]], [~p[1][2], ~p[2][2]], [~p[1][2], ~p[3][2]], [~p[2][2], ~p[3][2]], [~p[0][3], ~p[1][3]], [~p[0][3], ~p[2][3]], [~p[0][3], ~p[3][3]], [~p[1][3], ~p[2][3]], [~p[1][3], ~p[3][3]], [~p[2][3], ~p[3][3]], [~p[1][0], ~p[0][1]], [~p[1][1], ~p[0][2]], [~p[1][2], ~p[0][3]], [~p[2][0], ~p[1][1]], [~p[2][0], ~p[0][2]], [~p[2][1], ~p[1][2]], [~p[2][1], ~p[0][3]], [~p[2][2], ~p[1][3]], [~p[3][0], ~p[2][1]], [~p[3][0], ~p[1][2]], [~p[3][0], ~p[0][3]], [~p[3][1], ~p[2][2]], [~p[3][1], ~p[1][3]], [~p[3][2], ~p[2][3]], [~p[0][0], ~p[1][1]], [~p[0][0], ~p[2][2]], [~p[0][0], ~p[3][3]], [~p[0][1], ~p[1][2]], [~p[0][1], ~p[2][3]], [~p[0][2], ~p[1][3]], [~p[1][0], ~p[2][1]], [~p[1][0], ~p[3][2]], [~p[1][1], ~p[2][2]], [~p[1][1], ~p[3][3]], [~p[1][2], ~p[2][3]], [~p[2][0], ~p[3][1]], [~p[2][1], ~p[3][2]], [~p[2][2], ~p[3][3]]]

test_cnf = CNF(q)
print("Whether have one solution: ", DPLL(test_cnf))
'''
$ Factually, two solutions here
$ True
'''

q.append([p[1][1], p[3][1], p[3][0], ~p[1][3], p[2][3], p[1][0], ~p[0][1], p[0][0], p[3][3], ~p[3][2], p[0][3], p[2][1], ~p[2][0], p[1][2], p[2][2], p[0][2]])
print("Whether have another solution: ", DPLL(test_cnf))
'''
$ Factually, still one
$ True
'''

q.append([p[1][2], p[2][0], p[1][3], p[1][1], p[0][3], ~p[0][2], p[2][2], p[3][3], ~p[3][1], ~p[1][0], p[0][0], p[2][1], ~p[2][3], p[3][0], p[0][1], p[3][2]])
print("Whether have another solution: ", DPLL(test_cnf))
'''
$ Factually, no solution else
$ False
'''


'''output test 
print(test_cnf.cnf, test_cnf.check())
print(test_cnf.casually_return_literal())
new_cnf = CNF([[p[0][0], p[0][2]], [~p[0][0], ~p[0][2]]])
new_cnf.unit_spread(p[0][0])
print(new_cnf.cnf)
'''



