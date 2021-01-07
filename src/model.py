import ortools
from ortools.linear_solver import pywraplp
from src.constants import *

class MILP:
    def __init__(self, params):
        self.params = params
        self.solver = pywraplp.Solver.CreateSolver('SCIP')
        self.infinity = self.solver.infinity()        

    def set_variables(self):
        self.s = [
            [ 
                self.solver.IntVar(
                    0.0, 
                    self.infinity, 
                    'start time product {i} batch {j}'.format(i=i, j=j)
                ) for j in range(self.params['num_customers'])
            ] for i in range(self.params['num_products'])
        ]
        self.c = [ 
            [   
                self.solver.IntVar(
                    0.0, 
                    self.infinity, 
                    'completion time product {i} batch {j}'.format(i=i, j=j)
                ) for j in range(self.params['num_customers'])
            ] for i in range(self.params['num_products'])
        ]
        self.st = [ 
            [   
                self.solver.IntVar(
                    0.0, 
                    self.infinity, 
                    'delivery start time vehicle {v} trip {h}'.format(v=v, h=h)
                ) for h in range(self.params['num_customers'])
            ] for v in range(self.params['num_vehicles'])
        ]
        self.a = [
            [
                [
                    self.solver.IntVar(
                        0.0,
                        self.infinity,
                        'delivery arrival time customer {j} vehicle {v} trip {h}'.format(j=j, v=v, h=h)
                    ) for h in range(self.params['num_customers'])
                ] for v in range(self.params['num_vehicles'])
            ] for j in range(self.params['num_customers'])
        ]
        self.e = [
            [
                [
                    self.solver.IntVar(
                        0.0,
                        self.infinity,
                        'early delivery time customer {j} vehicle {v} trip {h}'.format(j=j, v=v, h=h)
                    ) for h in range(self.params['num_customers'])
                ] for v in range(self.params['num_vehicles'])
            ] for j in range(self.params['num_customers'])
        ]

        self.l = [
            [
                [
                    self.solver.IntVar(
                        0.0,
                        self.infinity,
                        'late delivery time customer {j} vehicle {v} trip {h}'.format(j=j, v=v, h=h)
                    ) for h in range(self.params['num_customers'])
                ] for v in range(self.params['num_vehicles'])
            ] for j in range(self.params['num_customers'])
        ]

        self.x = [
            [
                solver.BoolVar(
                    'production schedule from product {p} to product {q}'.format(p = p, q = q)
                ) for q in range(params['num_products'])
            ] for p in range(params['num_products']) 
        ]

        self.b = [
            [
                solver.BoolVar(
                    'order production customer {c} batch {f}'
                ) for c in range(num_customers)
            ] for f in range(num_customers)
        ]

        self.d = [
            solver.BoolVar(
                'batch activity {f}'.format(f=f)
            ) for f in range(num_customers)
        ]

        self.g = [
            [
                solver.BoolVar(
                    'production schedule from batch {p} to batch {q}'.format(p = p, q = q)
                ) for q in range(params['num_customers'])
            ] for p in range(params['num_customers'])
        ]

        self.t = 

        raise NotImplementedError

    def set_constraints(self):
        raise NotImplementedError

    def set_objective(self):
        raise NotImplementedError

    def solve(self):
        status = solver.Solve()
        return status
