#! /bin/python
"""
SAT-Solver basado en el algoritmo DPLL
Moisés González 11-10406
Fabio Suárez    12-10578
"""


class Solver(object):

    def __init__(self):
        self.clauses = []
        self.vars = []
        self.number_clauses = 0
        self.number_vars = 0

    def read(self, filename):
        tmp_clause = []

        with open(filename, 'r') as f:
            for line in f:
                if line[0] == 'c': continue
                elif line[0] == 'p':
                    self.number_vars = int(line.split(' ')[2])
                    self.number_clauses = int(line.split(' ')[3])
                    self.vars = [None for _ in range(int(self.number_vars))]
                    continue

                for lit in line.split():
                    if lit == '0':
                        self.clauses.append(tmp_clause)
                        tmp_clause = []
                        if (len(tmp_clause) == self.number_clauses):
                            return
                        continue
                    tmp_clause.append(self.__encode_lit(lit))
            else:
                if tmp_clause:
                    self.clauses.append(tmp_clause)
                    tmp_clause = []

    def evaluate_lit(self, lit):
        var_index = literal >> 1
        var_sign = literal & 1
        if self.vars[var_index] is None: return None
        return self.vars[var_index] == var_sign ^ 1

    def __encode_lit(self, lit):
        lit = int(lit)
        if lit > 0:
            sign = 0
        else:
            lit = -lit
            sign = -1
        return ((lit-1) << 1) | sign
