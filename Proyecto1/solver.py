#! /usr/bin/python3
import sys
from collections import deque, defaultdict

class Solver(object):

    def __init__(self, *args):
        self.number_clauses = 0
        self.number_vars = 0
        self.vars = []
        self.clauses = []
        self.literals_watched = []
        self.filename = ''

        self.list_watched = []
        self.units = []
        self.unasigned = []
        self.event_queue = []

    def read(self, filename):
        tmp_clause = []
        clause_num = 0
        with open(filename, 'r') as f:
            for line in f:
                if line[0] == 'c':
                    continue
                elif line[0] == 'p':
                    self.number_vars = int(line.split()[2])
                    self.number_clauses = int(line.split()[3])
                    self.vars = [None for _ in range(int(self.number_vars))]
                    continue
                for lit in line.split():
                    if lit == '0':
                        self.clauses.append(tmp_clause)
                        clause_num += 1
                        tmp_clause = []
                        continue
                    enc_lit = self.__encode_lit(lit)
                    tmp_clause.append(enc_lit)
        self.init_watchlist()

    def init_watchlist(self):
        self.list_watched = [deque() for _ in range(2 * self.number_vars)]
        for clause_num, clause in enumerate(self.clauses):
            if len(clause) < 2:
                self.list_watched[clause[0]].append(clause_num)
                self.literals_watched.append((clause[0],clause[0]))
                self.units.append(clause_num)
                continue

            self.list_watched[clause[0]].append(clause_num)
            self.list_watched[clause[1]].append(clause_num)
            self.literals_watched.append((clause[0], clause[1]))


    # Funciones auxiliares para el backtracking
    def update_unasigned(self, assigned_list):
        for a in assigned_list:
            if a in self.unasigned:
                self.unasigned.remove(a)
                                
    def undo_assignment(self, partial_assignment):
        for i in partial_assignment:
            self.vars[i] = None

    # Propagamos sobre un literal que evalua a True.
    # Si asignamos 1=False entonces propagamos sobre -1
    def propagate(self, literal, propagation_assignments):
        negated_literal = literal ^ 1
        
        count = 0
        while (self.list_watched[negated_literal] and
               count < len(self.list_watched[negated_literal])):

            clause_num = self.list_watched[negated_literal][-1-count]
            clause = self.clauses[clause_num]
            w1, w2 = self.literals_watched[clause_num]

            # w1 debe ser el negated_literal
            if negated_literal == w2: w1, w2 = w2, w1

            if self.evaluate_lit(w2) is not True:
                found_new_watched = False
                for new_watched in clause:

                    if new_watched in (w1,w2): continue

                    if (self.evaluate_lit(new_watched)) is not False:
                        found_new_watched = True
                        del self.list_watched[negated_literal][-1-count]
                        if not (clause in self.list_watched[new_watched]):
                            self.list_watched[new_watched].append(clause_num)
                        self.literals_watched[clause_num] = (w2, new_watched)
                        break

                if not found_new_watched and self.evaluate_lit(w2) is None:
                    self.vars[w2>>1] = bool(w2&1^1)
                    propagation_assignments.append(w2>>1)
                    if self.propagate(w2, propagation_assignments) is False:
                        return False

                elif (not found_new_watched and self.evaluate_lit(w2) is False):
                    return False
            count += 1
        return True

    def solve(self):
        n = self.number_vars
        self.unasigned = list(range(n))
        state = [0] * n # Guardamos los intentos de asignar. 0=None,1=T,2=F,3=Ambos

        # Resolvemos las clausulas unitarias inciales
        propagation_assignments = []
        for clause_num in self.units:
            lit = self.clauses[clause_num][0]
            # Asignamos y propagamos
            self.vars[lit>>1] = bool(lit&1^1)
            if (lit>>1) in self.unasigned: self.unasigned.remove(lit>>1)
            if self.propagate(lit, propagation_assignments) is False:
                return False

        self.update_unasigned(propagation_assignments)


        while self.unasigned:
            v = self.unasigned.pop()

            propagation_assignments=[]

            if (state[v] == 0 or state[v] == 2):
                self.vars[v] = True
                state[v] |= 1
                no_conflict = self.propagate(v<<1, propagation_assignments) 

                if no_conflict:
                    decision_level = (v, propagation_assignments)
                    self.event_queue.append(decision_level)
                    self.update_unasigned(propagation_assignments)
                    continue
                else:
                    self.undo_assignment(propagation_assignments) 
                    propagation_assignments = []

            if (state[v] == 0 or state[v] == 1):
                self.vars[v] = False
                state[v] |= 2
                no_conflict = self.propagate(v<<1|1, propagation_assignments)

                if no_conflict:
                    decision_level = (v, propagation_assignments)
                    self.event_queue.append(decision_level)
                    self.update_unasigned(propagation_assignments)
                    continue
                else:
                    self.undo_assignment(propagation_assignments)
                    propagation_assignments = []


            if state[v] == 3:
                if not self.event_queue:
                    return False
                else:
                    # Backtracking
                    state[v] = 0
                    self.vars[v] = None
                    self.unasigned.append(v)
                    var, prop_ass = self.event_queue.pop()
                    self.undo_assignment(prop_ass)
                    self.unasigned.extend(prop_ass)
                    self.unasigned.append(var)
            
        return True


    def check_solution(self):
        truth = 0
        for c in self.clauses:
            for lit in c:
                if self.evaluate_lit(lit):
                    break
            else:
                # print(c)
                return False

        return True

    def evaluate_lit(self, encoded_lit):
        var_index = encoded_lit >> 1
        var_sign = encoded_lit & 1
        if self.vars[var_index] == None: return None

        return self.vars[var_index] == var_sign ^ 1

    # Biyeccion de Z a N.
    def __encode_lit(self, lit):
        lit = int(lit)
        if lit > 0:
            sign = 0
        else:
            lit = -lit
            sign = 1
        return ((lit-1) << 1) | sign


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
    if s.solve():
        print(s.output_dimacs())
    else:
        print("UNSAT")
