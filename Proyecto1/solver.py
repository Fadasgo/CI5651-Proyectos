#! /bin/python
"""
SAT-Solver basado en el algoritmo DPLL
Moisés González 11-10406
Fabio Suárez    12-10578
"""

import sys

class Solver(object):

    def __init__(self):
        self.clauses = []
        self.vars = []
        self.number_clauses = 0
        self.number_vars = 0
        self.list_watched = []
        self.filename = ''

    def read(self, filename):
        tmp_clause = []
        self.filename = filename

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
                        if (len(tmp_clause) >= self.number_clauses):
                            self.init_list_watched()
                            return
                        continue
                    tmp_clause.append(self.__encode_lit(lit))
            else:
                if tmp_clause:
                    self.clauses.append(tmp_clause)
                    tmp_clause = []
                    self.init_list_watched()

        self.init_list_watched()

    def evaluate_lit(self, lit):
        var_index = lit >> 1
        var_sign = lit & 1
        if self.vars[var_index] is None: return None
        return self.vars[var_index] == var_sign ^ 1

    # Biyeccion de Z a N. Para poder usar los literales como indices
    # de una lista
    def __encode_lit(self, lit):
        lit = int(lit)
        if lit > 0:
            sign = 0
        else:
            lit = -lit
            sign = 1
        return ((lit-1) << 1) | sign

    # Buscamos algun literal True en cada clausula, Si no
    # lo conseguimos, no es solucion
    def check_solution(self):
        for c in self.clauses:
            for lit in c:
                if self.evaluate_lit(lit) == True:
                    break
            else:
                return False
        return True

    def init_list_watched(self):
        self.list_watched = [[] for _ in range(2* self.number_vars)]
        for clause in self.clauses:
            self.list_watched[clause[0]].append(clause)

    def check_list_watched(self, literal):
        # Iteramos mientras hayan clausulas que observan
        # el literal
        while(self.list_watched[literal]):
            clause = self.list_watched[literal][0]

            new_watched = False

            for new_lit in clause:
                if self.evaluate_lit(new_lit) is not False:
                    new_watched = True
                    del self.list_watched[literal][0]
                    self.list_watched[new_lit].append(clause)
                    break

            if not new_watched:
                return False

        return True


    def solve(self, var_index):
        if var_index == self.number_vars:
            if self.check_solution():
                return True
            else: return False

        for v in [0,1]:
            self.vars[var_index] = v
            if self.check_list_watched((var_index <<1) | v):
                if self.solve(var_index + 1):
                    return True

        self.vars[var_index] = None

    def output_dimacs(self):
        # print("c solucion para formula CNF {}".format(self.filename))
        out = "s cnf {} {}\n".format(self.number_vars, self.number_clauses)
        if self.vars[0] is None:
            return out
        for v,s in enumerate(self.vars):
            if s > 0:
                out += "v {}\n".format(v+1)
            else:
                out += ("v {}\n".format(-(v+1)))
        return out


if __name__ == '__main__':
    s = Solver()
    s.read(sys.argv[1])
    if s.solve(0):
        s.output_dimacs()
    else:
        print("UNSAT")
