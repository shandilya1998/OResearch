import numpy as np
import ortools
from ortools.linear_solver import pywraplp
from src.constants import *


class MILP:
    def __init__(self, params, solver=None):
        self.params = params
        if solver is None:
            self.solver = pywraplp.Solver.CreateSolver('SCIP')
        else:
            self.solver = solver
        self.infinity = self.solver.infinity()
        self.built = False
        if self.params['num_vehicles'] > self.params['num_customers']:
            raise ValueError(
                'Expected number of vehicles less than the number of \
                customers, got number of vehicles {v} for \
                {c} customers'.format(
                    v=self.params['num_vehicles'],
                    c=self.params['num_customers']
                )
            )
        self.solved = False

    def get_solution(self):
        solution = {
            's' : [
                [
                    self.s[i][j].solution_value() \
                    for j in range(self.params['num_batches'])
                ] for i in range(self.params['num_products'])
            ],
            'c' : [ 
                [   
                    self.c[i][j].solution_value() \
                    for j in range(self.params['num_batches'])
                ] for i in range(self.params['num_products'])
            ],
            'st' : [ 
                [   
                    self.st[v][h].solution_value() \
                    for h in range(self.params['num_trips'])
                ] for v in range(self.params['num_vehicles'])
            ],
            'a' : [
                [
                    [
                        self.a[j][v][h].solution_value() \
                        for h in range(self.params['num_trips'])
                    ] for v in range(self.params['num_vehicles'])
                ] for j in range(self.params['num_customers'] + 2)
            ],
            'e' : [
                [
                    [
                        self.e[j][v][h].solution_value() \
                        for h in range(self.params['num_trips'])
                    ] for v in range(self.params['num_vehicles'])
                ] for j in range(self.params['num_customers'] + 2)
            ],
            'l' : [
                [
                    [
                        self.l[j][v][h].solution_value() \
                        for h in range(self.params['num_trips'])
                    ] for v in range(self.params['num_vehicles'])
                ] for j in range(self.params['num_customers'] + 2)
            ],
            'x' : [
                [
                    self.x[p][q].solution_value() \
                    for q in range(self.params['num_products'])
                ] for p in range(self.params['num_products'])
            ],
            'b' : [ 
                [   
                    self.b[c][f].solution_value() \
                    for f in range(self.params['num_batches'])
                ] for c in range(self.params['num_customers'] + 2)
            ],
            'd' : [
                self.d[f].solution_value() \
                for f in range(self.params['num_batches'])
            ],
            'g' : [
                [
                    self.g[p][q].solution_value()\
                    for q in range(self.params['num_batches'])
                ] for p in range(self.params['num_batches'])
            ],
            't' : [
                [
                    [
                        self.t[v][t][b].solution_value() \
                        for b in range(self.params['num_batches'])
                    ] for t in range(self.params['num_trips'])
                ] for v in range(self.params['num_vehicles'])
            ],
            'u' : [
                [
                    [
                        self.u[v][t][i].solution_value() \
                        for i in range(self.params['num_customers'] + 2)
                    ] for t in range(self.params['num_trips'])
                ] for v in range(self.params['num_vehicles'])
            ],
            'y' : [
                [
                    [
                        [
                            self.y[v][t][j][i].solution_value() \
                             for i in range(self.params['num_customers'] + 2)
                        ] for j in range(self.params['num_customers'] + 2)
                    ] for t in range(self.params['num_trips'])
                ] for v in range(self.params['num_vehicles'])
            ],
            'w' : [
                self.w[v] \
                for v in range(self.params['num_vehicles'])
            ],
            'objective_value' : self.solver.Objective().Value(),
            'solving_time' : self.solver.wall_time(),
            'solving_iterations' : self.solver.iterations(),
            'num_branch_and_bound_nodes' : self.solver.nodes()
        }
        return solution

    def build(self):
        print('Building Variables', end = '')
        self.s = np.array([
            [
                self.solver.IntVar(
                    0.0,
                    self.infinity,
                    'start time product `{i}` batch `{j}`'.format(i=i, j=j)
                ) for j in range(self.params['num_batches'])
            ] for i in range(self.params['num_products'])
        ])
        print('.', end = '')
        self.c = np.array([
            [
                self.solver.IntVar(
                    0.0,
                    self.infinity,
                    'completion time product {i} batch {j}'.format(i=i, j=j)
                ) for j in range(self.params['num_batches'])
            ] for i in range(self.params['num_products'])
        ])
        print('.', end = '')
        self.st = np.array([
            [
                self.solver.IntVar(
                    0.0,
                    self.infinity,
                    'delivery start time vehicle {v} trip {h}'.format(
                        v=v, 
                        h=h
                    )
                ) for h in range(self.params['num_trips'])
            ] for v in range(self.params['num_vehicles'])
        ])
        print('.', end = '')
        self.a = np.array([
            [
                [
                    self.solver.IntVar(
                        0.0,
                        self.infinity,
                        'delivery arrival time customer {j} vehicle {v} trip {h}'.format(
                            j=j, v=v, h=h)
                    ) for h in range(self.params['num_trips'])
                ] for v in range(self.params['num_vehicles'])
            ] for j in range(self.params['num_customers'] + 2)
        ])
        print('.', end = '')
        self.e = np.array([
            [
                [
                    self.solver.IntVar(
                        0.0,
                        self.infinity,
                        'early delivery time customer {j} vehicle {v} trip {h}'.format(
                            j=j, v=v, h=h)
                    ) for h in range(self.params['num_trips'])
                ] for v in range(self.params['num_vehicles'])
            ] for j in range(self.params['num_customers'] + 2)
        ])
        print('.', end = '')
        self.l = np.array([
            [
                [
                    self.solver.IntVar(
                        0.0,
                        self.infinity,
                        'late delivery time customer {j} vehicle {v} trip {h}'.format(
                            j=j, v=v, h=h)
                    ) for h in range(self.params['num_trips'])
                ] for v in range(self.params['num_vehicles'])
            ] for j in range(self.params['num_customers'] + 2)
        ])
        print('.', end = '')
        self.x = np.array([
            [
                self.solver.BoolVar(
                    'production transition from product {p} to product {q}'.format(
                        p=p, q=q)
                ) for q in range(self.params['num_products'])
            ] for p in range(self.params['num_products'])
        ])
        print('.', end = '')
        self.b = np.array([
            [
                self.solver.BoolVar(
                    'order production customer {c} batch {f}'
                ) for f in range(self.params['num_batches'])
            ] for c in range(self.params['num_customers'] + 2)
        ])
        print('.', end = '')
        self.d = np.array([
            self.solver.BoolVar(
                'batch activity {f}'.format(f=f)
            ) for f in range(self.params['num_batches'])
        ])
        print('.', end = '')
        self.g = np.array([
            [
                self.solver.BoolVar(
                    'production transition from batch {p} to batch {q}'.format(
                        p=p, q=q)
                ) for q in range(self.params['num_batches'])
            ] for p in range(self.params['num_batches'])
        ])
        print('.', end = '')
        self.t = np.array([
            [
                [
                    self.solver.BoolVar(
                        'batch {b} trip {t} vehicle {v} map'.format(
                            b=b,
                            t=t,
                            v=v
                        )
                    ) for b in range(self.params['num_batches'])
                ] for t in range(self.params['num_trips'])
            ] for v in range(self.params['num_vehicles'])
        ])
        print('.', end = '')
        self.u = np.array([
            [
                [
                    self.solver.BoolVar(
                        'customer {i} visit trip {t} vehicle {v}'.format(
                            i=i,
                            t=t,
                            v=v
                        )
                    ) for i in range(self.params['num_customers'] + 2)
                ] for t in range(self.params['num_trips'])
            ] for v in range(self.params['num_vehicles'])
        ])
        print('.', end = '')
        self.y = np.array([
            [
                [
                    [
                        self.solver.BoolVar(
                            'customer delivery transition from customer {i} to customer {j} trip {t} vehicle {v} '.format(
                                i=i,
                                j=j,
                                t=t,
                                v=v
                            )
                        ) for i in range(self.params['num_customers'] + 2)
                    ] for j in range(self.params['num_customers'] + 2)
                ] for t in range(self.params['num_trips'])
            ] for v in range(self.params['num_vehicles'])
        ])
        print('.', end = '')
        self.w = np.array([
            self.solver.BoolVar(
                'vehicle {v} usage'.format(v=v)
            ) for v in range(self.params['num_vehicles'])
        ])
        print('.')
        print('Building Constraints', end = '')
        for c in range(1, self.params['num_customers'] + 1):
            self.solver.Add(np.sum(self.u, (0, 1))[c] == 1)
        print('.', end = '')
        for j in range(self.params['num_customers'] + 2):
            for h in range(self.params['num_trips']):
                for v in range(self.params['num_vehicles']):
                    self.solver.Add(self.u[v][h][0] >= self.u[v][h][j])
        print('.', end = '')
        for v in range(self.params['num_vehicles']):
            for h in range(self.params['num_trips']):
                self.solver.Add(
                    sum([
                        sum([
                            self.params['demand'][p][j] * \
                            self.u[v][h][j+1] \
                            for p in range(self.params['num_products'])
                        ]) for j in range(self.params['num_customers'])
                    ]) <= self.params['vehicle_capacity'][v]
                )
        print('.', end = '')
        for i in range(1, self.params['num_customers'] + 1):
            for j in range(1, self.params['num_customers'] + 1):
                for h in range(self.params['num_trips']):
                    for v in range(self.params['num_vehicles']):
                        self.solver.Add(
                            self.y[v][h][i][0] + \
                            self.y[v][h][j][0] + \
                            self.u[v][h][i] + \
                            self.u[v][h][j] <= 3
                        )
        print('.', end = '')
        for j in range(1, self.params['num_customers']+1):
            for h in range(self.params['num_trips']):
                for v in range(self.params['num_vehicles']):
                    self.solver.Add(
                        self.u[v][h][j] == np.sum(self.y, -1)[v][h][j] - \
                            self.y[v][h][j][self.params['num_customers']]
                    )
                    self.solver.Add(
                        self.u[v][h][j] == np.sum(self.y, -1)[v][h][j] - \
                            self.y[v][h][j][0]
                    )
        print('.', end = '')
        for i in range(1, self.params['num_customers']+1):
            for j in range(1, self.params['num_customers']+1):
                for h in range(self.params['num_trips']):
                    for v in range(self.params['num_vehicles']):
                        self.solver.Add(
                            self.u[v][h][i] >= self.y[v][h][j][i] + \
                                self.u[v][h][j] - 1
                        )
        print('.', end = '')
        for i in range(1, self.params['num_customers']+1):
            for j in range(1, self.params['num_customers']+1):
                for h in range(self.params['num_trips']):
                    for v in range(self.params['num_vehicles']):
                        self.solver.Add(
                            self.u[v][h][j] >= self.y[v][h][j][i] + \
                                self.u[v][h][i] - 1
                        )
        print('.', end = '')
        for v in range(self.params['num_vehicles']):
            for h in range(self.params['num_trips'] - 1):
                self.solver.Add(
                    self.params['M']*(
                        np.sum(self.u, -1)[v][h] - \
                            self.u[v][h][0]) >= \
                            np.sum(self.u, -1)[v][h+1] - \
                            self.u[v][h+1][0]
                )
        print('.', end = '')
        for v in range(self.params['num_vehicles']):
            for h in range(self.params['num_trips']):
                self.solver.Add(
                    self.u[v][h][0] >= self.w[v]
                )
        print('.', end = '')
        for p in range(self.params['num_products']):
            self.solver.Add(
                np.sum(self.x, -1)[p] - self.x[p][p] == 1
            )
        print('.', end = '')
        for q in range(self.params['num_products']):
            self.solver.Add(
                np.sum(self.x, 0)[q] - self.x[q][q] == 1
            )
        print('.', end = '')
        for p in range(self.params['num_products']):
            for q in range(self.params['num_products']):
                self.solver.Add(
                    self.x[p][q] <= 1 - self.x[q][p]
                )
        print('.', end = '')
        self.solver.Add(
            np.sum(self.u, (0, 1))[0] == np.sum(self.d, 0)
        )
        print('.', end = '')
        for f in range(self.params['num_batches']-1):
            self.solver.Add(
                self.d[f] >= self.d[f+1]
            )
        print('.', end = '')
        for v in range(self.params['num_vehicles']):
            for h in range(self.params['num_trips']):
                self.solver.Add(
                    np.sum(self.t, -1)[v][h] == self.u[v][h][0]
                )
        print('.', end = '')
        for f in range(self.params['num_batches']):
            self.solver.Add(
                self.d[f] == np.sum(self.t, (0, 1))[f]
            )
        print('.', end = '')
        for j in range(self.params['num_customers']+2):
            self.solver.Add(
                sum([
                    self.b[j][f] for f in range(self.params['num_batches'])
                ]) == 1
            )
        print('.', end = '')
        for f in range(self.params['num_customers']):
            for j in range(1, self.params['num_customers']+1):
                for h in range(self.params['num_trips']):
                    for v in range(self.params['num_vehicles']):
                        self.solver.Add(
                            self.b[j][f] + 1 >= self.u[v][h][j] + \
                                self.t[v][h][f]
                        )
        print('.', end = '')
        for f in range(self.params['num_customers']):
            for j in range(1, self.params['num_customers']+1):
                for h in range(self.params['num_trips']):
                    for v in range(self.params['num_vehicles']):
                        self.solver.Add(
                            self.t[v][h][f] + 1 >= self.b[j][f] + \
                                self.u[v][h][j]
                        )
        print('.', end = '')
        for f in range(self.params['num_batches']):
            self.solver.Add(
                np.sum(self.g, 0)[f] == self.d[f]
            )
            self.solver.Add(
                np.sum(self.g, 1)[f] == self.d[f]
            )
        print('.', end = '')
        for p in range(self.params['num_products']):
            for f in range(self.params['num_batches']):
                self.solver.Add(
                    np.sum(
                        self.params['setup_time'] * self.x,
                        (0, 1)
                    ) + sum([
                        sum([
                            self.params['process_time'][p_] * \
                            self.params['demand'][p_][j] * \
                            self.b[j+1][f] \
                            for j in range(self.params['num_customers'])
                        ]) for p_ in range(self.params['num_products'])
                    ]) - self.params['M'] * (1- self.g[0][f]) <= self.c[p][f]
                )
        print('.', end = '')
        for p in range(self.params['num_products']):
            for f in range(self.params['num_batches']):
                for f_ in range(self.params['num_batches']):
                    self.solver.Add(
                        self.s[p][f] + np.sum(
                            self.params['setup_time'] * self.x,
                            (0, 1)
                        ) + sum([
                            sum([
                                self.params['process_time'][p_] * \
                                self.params['demand'][p_][j] * \
                                self.b[j+1][f] \
                                for j in range(self.params['num_customers'])
                            ]) for p_ in range(self.params['num_products'])
                        ]) - self.params['M'] * (1- self.g[f][f_]) <= self.c[p][f_]
                    )
        print('.', end = '')
        for i in range(1, self.params['num_customers']+1):
            for j in range(1, self.params['num_customers']+1):
                for h in range(self.params['num_trips']):
                    for v in range(self.params['num_vehicles']):
                        self.solver.Add(
                            self.a[j][v][h] >= self.st[v][h] + \
                                self.params['service_time'][0] + \
                                self.params['travel_time'] [0][j]- \
                                self.params['M'] * (1 - self.u[v][h][j])
                        )

                        self.solver.Add(
                            self.a[j][v][h] >= self.a[i][v][h] + \
                                self.params['service_time'][i] + \
                                self.params['travel_time'][i][j] - \
                                self.params['M'] * (1 - self.y[v][h][j][i])
                        )
        print('.', end = '')
        for p in range(self.params['num_products']):
            for v in range(self.params['num_vehicles']):
                for f in range(self.params['num_batches']):
                    self.solver.Add(
                        self.st[v][1] >= self.c[p][f] + \
                            self.params['service_time'][0] - \
                            self.params['M'] * ( self.t[v][1][f])
                    )
        print('.', end = '')
        for p in range(self.params['num_products']):
            for f in range(self.params['num_batches']):
                for v in range(self.params['num_vehicles']):
                    for h in range(self.params['num_trips'] - 1):
                        self.solver.Add(
                            self.st[v][h+1] >= self.a[
                                self.params['num_customers'] + 1
                            ][v][h] + self.params['service_time'][
                                self.params['num_customers'] + 1
                            ] and self.a[
                                self.params['num_customers']+1
                            ][v][h] <= self.c[p][f]
                        )
    
                        self.solver.Add(
                            self.st[v][h+1] >= self.c[p][f] + \
                                self.params['service_time'][0] - \
                                self.params['M'] * (1 - self.t[v][h+1][f])
                        )
        print('.', end = '')
        for j in range(1, self.params['num_customers'] + 1):
            for v in range(self.params['num_vehicles']):
                for h in range(self.params['num_trips']):
                    self.solver.Add(
                        self.e[j][v][h] >= \
                        self.params['time_windows'][j][0] - self.a[j][v][h]
                    )

                    self.solver.Add(
                        self.l[j][v][h] >= self.a[j][v][h] - self.params[
                            'time_windows'
                        ][j][0]
                    ) 
        print('.')
        print('Building Objective.......')

        self.solver.Minimize(
            self.params['processing_cost'] * sum([
                sum([ 
                    self.params['process_time'][p] * \
                    self.params['demand'][p][j] for p in range(
                        self.params['num_products']
                    )
                ]) for j in range(self.params['num_customers'])
            ]) + self.params['setup_cost'] * sum([
                sum([
                    self.params['setup_time'][p][q] * \
                    self.x[p][q] for q in range(self.params['num_products'])
                ]) for p in range(self.params['num_products'])
            ]) + self.params['travel_cost'] * sum([
                sum([
                    sum([
                        sum([
                            self.params['travel_time'][i][j] * \
                            self.y[v][h][j][i] for i in range(
                                1, 
                                self.params['num_customers'] + 1
                            )
                        ]) for j in range(1, self.params['num_customers']+1)
                    ]) for h in range(self.params['num_trips'])
                ]) for v in range(self.params['num_vehicles'])  
            ]) + sum([
                self.params['vehicle_cost'][v] * self.w[v] \
                for v in range(self.params['num_vehicles'])
            ]) + self.params['early_delivery_penalty'] * sum([
                sum([
                    sum([
                        self.e[j][v][h] for j in range(
                            1, 
                            self.params['num_customers'] + 1
                        )
                    ]) for h in range(self.params['num_trips'])
                ]) for v in range(self.params['num_vehicles'])
            ]) + self.params['late_delivery_penalty'] * sum([
                sum([
                    sum([
                        self.l[j][v][h] for j in range(
                            1,  
                            self.params['num_customers'] + 1 
                        )   
                    ]) for h in range(self.params['num_trips'])
                ]) for v in range(self.params['num_vehicles'])
            ])
        )

        self.built = True
        print('Building Done............')

    def num_variables(self):
        return self.solver.NumVariables()

    def solve(self):
        status = self.solver.Solve()
        print('Solving Done...........')
        if status == pywraplp.Solver.OPTIMAL:
            print('Obtained optimal solution')
        else:
            print('The problem does not have an optimal solution.')
        self.solved = True
        return status

class LP:
    def __init__(self, params, solver=None):
        self.params = params
        if solver is None:
            self.solver = pywraplp.Solver.CreateSolver('GLOP')
        else:
            self.solver = solver
        self.infinity = self.solver.infinity()
        self.built = False
        if self.params['num_vehicles'] > self.params['num_customers']:
            raise ValueError(
                'Expected number of vehicles less than the number of \
                customers, got number of vehicles {v} for \
                {c} customers'.format(
                    v=self.params['num_vehicles'],
                    c=self.params['num_customers']
                )
            )
        self.solved = False

    def get_solution(self):
        solution = {
            's' : [
                [
                    self.s[i][j].solution_value() \
                    for j in range(self.params['num_batches'])
                ] for i in range(self.params['num_products'])
            ],
            'c' : [
                [
                    self.c[i][j].solution_value() \
                    for j in range(self.params['num_batches'])
                ] for i in range(self.params['num_products'])
            ],
            'st' : [
                [
                    self.st[v][h].solution_value() \
                    for h in range(self.params['num_trips'])
                ] for v in range(self.params['num_vehicles'])
            ],
            'a' : [
                [
                    [
                        self.a[j][v][h].solution_value() \
                        for h in range(self.params['num_trips'])
                    ] for v in range(self.params['num_vehicles'])
                ] for j in range(self.params['num_customers'] + 2)
            ],
            'e' : [
                [
                    [
                        self.e[j][v][h].solution_value() \
                        for h in range(self.params['num_trips'])
                    ] for v in range(self.params['num_vehicles'])
                ] for j in range(self.params['num_customers'] + 2)
            ],
            'l' : [
                [
                    [
                        self.l[j][v][h].solution_value() \
                        for h in range(self.params['num_trips'])
                    ] for v in range(self.params['num_vehicles'])
                ] for j in range(self.params['num_customers'] + 2)
            ],
            'x' : [
                [
                    self.x[p][q].solution_value() \
                    for q in range(self.params['num_products'])
                ] for p in range(self.params['num_products'])
            ],
            'b' : [
                [
                    self.b[c][f].solution_value() \
                    for f in range(self.params['num_batches'])
                ] for c in range(self.params['num_customers'] + 2)
            ],
            'd' : [
                self.d[f].solution_value() \
                for f in range(self.params['num_batches'])
            ],
            'g' : [
                [
                    self.g[p][q].solution_value()\
                    for q in range(self.params['num_batches'])
                ] for p in range(self.params['num_batches'])
            ],
            't' : [
                [
                    [
                        self.t[v][t][b].solution_value() \
                        for b in range(self.params['num_batches'])
                    ] for t in range(self.params['num_trips'])
                ] for v in range(self.params['num_vehicles'])
            ],
            'u' : [
                [
                    [
                        self.u[v][t][i].solution_value() \
                        for i in range(self.params['num_customers'] + 2)
                    ] for t in range(self.params['num_trips'])
                ] for v in range(self.params['num_vehicles'])
            ],
            'y' : [
                [
                    [
                        [
                            self.y[v][t][j][i].solution_value() \
                             for i in range(self.params['num_customers'] + 2)
                        ] for j in range(self.params['num_customers'] + 2)
                    ] for t in range(self.params['num_trips'])
                ] for v in range(self.params['num_vehicles'])
            ],
            'w' : [
                self.w[v].solution_values() \
                for v in range(self.params['num_vehicles'])
            ],
            'objective_value' : self.solver.Objective().Value(),
            'solving_time' : self.solver.wall_time(),
            'solving_iterations' : self.solver.iterations(),
            'num_branch_and_bound_nodes' : self.solver.nodes()
        }
        return solution

    def build(self):
        print('Building Variables', end = '')
        self.s = np.array([
            [
                self.solver.NumVar(
                    0.0,
                    self.infinity,
                    'start time product `{i}` batch `{j}`'.format(i=i, j=j)
                ) for j in range(self.params['num_batches'])
            ] for i in range(self.params['num_products'])
        ])
        print('.', end = '')
        self.c = np.array([
            [
                self.solver.NumVar(
                    0.0,
                    self.infinity,
                    'completion time product {i} batch {j}'.format(i=i, j=j)
                ) for j in range(self.params['num_batches'])
            ] for i in range(self.params['num_products'])
        ])
        print('.', end = '')
        self.st = np.array([
            [
                self.solver.NumVar(
                    0.0,
                    self.infinity,
                    'delivery start time vehicle {v} trip {h}'.format(
                        v=v,
                        h=h
                    )
                ) for h in range(self.params['num_trips'])
            ] for v in range(self.params['num_vehicles'])
        ])
        print('.', end = '')
        self.a = np.array([
            [
                [
                    self.solver.NumVar(
                        0.0,
                        self.infinity,
                        'delivery arrival time customer {j} vehicle {v} trip {h}'.format(
                            j=j, v=v, h=h)
                    ) for h in range(self.params['num_trips'])
                ] for v in range(self.params['num_vehicles'])
            ] for j in range(self.params['num_customers'] + 2)
        ])
        print('.', end = '')
        self.e = np.array([
            [
                [
                    self.solver.NumVar(
                        0.0,
                        self.infinity,
                        'early delivery time customer {j} vehicle {v} trip {h}'.format(
                            j=j, v=v, h=h)
                    ) for h in range(self.params['num_trips'])
                ] for v in range(self.params['num_vehicles'])
            ] for j in range(self.params['num_customers'] + 2)
        ])
        print('.', end = '')
        self.l = np.array([
            [
                [
                    self.solver.NumVar(
                        0.0,
                        self.infinity,
                        'late delivery time customer {j} vehicle {v} trip {h}'.format(
                            j=j, v=v, h=h)
                    ) for h in range(self.params['num_trips'])
                ] for v in range(self.params['num_vehicles'])
            ] for j in range(self.params['num_customers'] + 2)
        ])
        print('.', end = '')
        self.x = np.array([
            [
                self.solver.BoolVar(
                    'production transition from product {p} to product {q}'.format(
                        p=p, q=q)
                ) for q in range(self.params['num_products'])
            ] for p in range(self.params['num_products'])
        ])
        print('.', end = '')
        self.b = np.array([
            [
                self.solver.BoolVar(
                    'order production customer {c} batch {f}'
                ) for f in range(self.params['num_batches'])
            ] for c in range(self.params['num_customers'] + 2)
        ])
        print('.', end = '')
        self.d = np.array([
            self.solver.BoolVar(
                'batch activity {f}'.format(f=f)
            ) for f in range(self.params['num_batches'])
        ])
        print('.', end = '')
        self.g = np.array([
            [
                self.solver.BoolVar(
                    'production transition from batch {p} to batch {q}'.format(
                        p=p, q=q)
                ) for q in range(self.params['num_batches'])
            ] for p in range(self.params['num_batches'])
        ])
        print('.', end = '')
        self.t = np.array([
            [
                [
                    self.solver.BoolVar(
                        'batch {b} trip {t} vehicle {v} map'.format(
                            b=b,
                            t=t,
                            v=v
                        )
                    ) for b in range(self.params['num_batches'])
                ] for t in range(self.params['num_trips'])
            ] for v in range(self.params['num_vehicles'])
        ])
        print('.', end = '')
        self.u = np.array([
            [
                [
                    self.solver.BoolVar(
                        'customer {i} visit trip {t} vehicle {v}'.format(
                            i=i,
                            t=t,
                            v=v
                        )
                    ) for i in range(self.params['num_customers'] + 2)
                ] for t in range(self.params['num_trips'])
            ] for v in range(self.params['num_vehicles'])
        ])
        print('.', end = '')
        self.y = np.array([
            [
                [
                    [
                        self.solver.BoolVar(
                            'customer delivery transition from customer {i} to customer {j} trip {t} vehicle {v} '.format(
                                i=i,
                                j=j,
                                t=t,
                                v=v
                            )
                        ) for i in range(self.params['num_customers'] + 2)
                    ] for j in range(self.params['num_customers'] + 2)
                ] for t in range(self.params['num_trips'])
            ] for v in range(self.params['num_vehicles'])
        ])
        print('.', end = '')
        self.w = np.array([
            self.solver.BoolVar(
                'vehicle {v} usage'.format(v=v)
            ) for v in range(self.params['num_vehicles'])
        ])
        print('.')
        print('Building Constraints', end = '')
        for c in range(1, self.params['num_customers'] + 1):
            self.solver.Add(np.sum(self.u, (0, 1))[c] == 1)
        print('.', end = '')
        for j in range(self.params['num_customers'] + 2):
            for h in range(self.params['num_trips']):
                for v in range(self.params['num_vehicles']):
                    self.solver.Add(self.u[v][h][0] >= self.u[v][h][j])
        print('.', end = '')
        for v in range(self.params['num_vehicles']):
            for h in range(self.params['num_trips']):
                self.solver.Add(
                    sum([
                        sum([
                            self.params['demand'][p][j] * \
                            self.u[v][h][j+1] \
                            for p in range(self.params['num_products'])
                        ]) for j in range(self.params['num_customers'])
                    ]) <= self.params['vehicle_capacity'][v]
                )
        print('.', end = '')
        for i in range(1, self.params['num_customers'] + 1):
            for j in range(1, self.params['num_customers'] + 1):
                for h in range(self.params['num_trips']):
                    for v in range(self.params['num_vehicles']):
                        self.solver.Add(
                            self.y[v][h][i][0] + \
                            self.y[v][h][j][0] + \
                            self.u[v][h][i] + \
                            self.u[v][h][j] <= 3
                        )
        print('.', end = '')
        for j in range(1, self.params['num_customers']+1):
            for h in range(self.params['num_trips']):
                for v in range(self.params['num_vehicles']):
                    self.solver.Add(
                        self.u[v][h][j] == np.sum(self.y, -1)[v][h][j] - \
                            self.y[v][h][j][self.params['num_customers']]
                    )
                    self.solver.Add(
                        self.u[v][h][j] == np.sum(self.y, -1)[v][h][j] - \
                            self.y[v][h][j][0]
                    )
        print('.', end = '')
        for i in range(1, self.params['num_customers']+1):
            for j in range(1, self.params['num_customers']+1):
                for h in range(self.params['num_trips']):
                    for v in range(self.params['num_vehicles']):
                        self.solver.Add(
                            self.u[v][h][i] >= self.y[v][h][j][i] + \
                                self.u[v][h][j] - 1
                        )
        print('.', end = '')
        for i in range(1, self.params['num_customers']+1):
            for j in range(1, self.params['num_customers']+1):
                for h in range(self.params['num_trips']):
                    for v in range(self.params['num_vehicles']):
                        self.solver.Add(
                            self.u[v][h][j] >= self.y[v][h][j][i] + \
                                self.u[v][h][i] - 1
                        )
        print('.', end = '')
        for v in range(self.params['num_vehicles']):
            for h in range(self.params['num_trips'] - 1):
                self.solver.Add(
                    self.params['M']*(
                        np.sum(self.u, -1)[v][h] - \
                            self.u[v][h][0]) >= \
                            np.sum(self.u, -1)[v][h+1] - \
                            self.u[v][h+1][0]
                )
        print('.', end = '')
        for v in range(self.params['num_vehicles']):
            for h in range(self.params['num_trips']):
                self.solver.Add(
                    self.u[v][h][0] >= self.w[v]
                )
        print('.', end = '')
        for p in range(self.params['num_products']):
            self.solver.Add(
                np.sum(self.x, -1)[p] - self.x[p][p] == 1
            )
        print('.', end = '')
        for q in range(self.params['num_products']):
            self.solver.Add(
                np.sum(self.x, 0)[q] - self.x[q][q] == 1
            )
        print('.', end = '')
        for p in range(self.params['num_products']):
            for q in range(self.params['num_products']):
                self.solver.Add(
                    self.x[p][q] <= 1 - self.x[q][p]
                )
        print('.', end = '')
        self.solver.Add(
            np.sum(self.u, (0, 1))[0] == np.sum(self.d, 0)
        )
        print('.', end = '')
        for f in range(self.params['num_batches']-1):
            self.solver.Add(
                self.d[f] >= self.d[f+1]
            )
        print('.', end = '')
        for v in range(self.params['num_vehicles']):
            for h in range(self.params['num_trips']):
                self.solver.Add(
                    np.sum(self.t, -1)[v][h] == self.u[v][h][0]
                )
        print('.', end = '')
        for f in range(self.params['num_batches']):
            self.solver.Add(
                self.d[f] == np.sum(self.t, (0, 1))[f]
            )
        print('.', end = '')
        for j in range(self.params['num_customers']+2):
            self.solver.Add(
                sum([
                    self.b[j][f] for f in range(self.params['num_batches'])
                ]) == 1
            )
        print('.', end = '')
        for f in range(self.params['num_customers']):
            for j in range(1, self.params['num_customers']+1):
                for h in range(self.params['num_trips']):
                    for v in range(self.params['num_vehicles']):
                        self.solver.Add(
                            self.b[j][f] + 1 >= self.u[v][h][j] + \
                                self.t[v][h][f]
                        )
        print('.', end = '')
        for f in range(self.params['num_customers']):
            for j in range(1, self.params['num_customers']+1):
                for h in range(self.params['num_trips']):
                    for v in range(self.params['num_vehicles']):
                        self.solver.Add(
                            self.t[v][h][f] + 1 >= self.b[j][f] + \
                                self.u[v][h][j]
                        )
        print('.', end = '')
        for f in range(self.params['num_batches']):
            self.solver.Add(
                np.sum(self.g, 0)[f] == self.d[f]
            )
            self.solver.Add(
                np.sum(self.g, 1)[f] == self.d[f]
            )
        print('.', end = '')
        for p in range(self.params['num_products']):
            for f in range(self.params['num_batches']):
                self.solver.Add(
                    np.sum(
                        self.params['setup_time'] * self.x,
                        (0, 1)
                    ) + sum([
                        sum([
                            self.params['process_time'][p_] * \
                            self.params['demand'][p_][j] * \
                            self.b[j+1][f] \
                            for j in range(self.params['num_customers'])
                        ]) for p_ in range(self.params['num_products'])
                    ]) - self.params['M'] * (1- self.g[0][f]) <= self.c[p][f]
                )
        print('.', end = '')
        for p in range(self.params['num_products']):
            for f in range(self.params['num_batches']):
                for f_ in range(self.params['num_batches']):
                    self.solver.Add(
                        self.s[p][f] + np.sum(
                            self.params['setup_time'] * self.x,
                            (0, 1)
                        ) + sum([
                            sum([
                                self.params['process_time'][p_] * \
                                self.params['demand'][p_][j] * \
                                self.b[j+1][f] \
                                for j in range(self.params['num_customers'])
                            ]) for p_ in range(self.params['num_products'])
                        ]) - self.params['M'] * (1- self.g[f][f_]) <= self.c[p][f_]
                    )
        print('.', end = '')
        for i in range(1, self.params['num_customers']+1):
            for j in range(1, self.params['num_customers']+1):
                for h in range(self.params['num_trips']):
                    for v in range(self.params['num_vehicles']):
                        self.solver.Add(
                            self.a[j][v][h] >= self.st[v][h] + \
                                self.params['service_time'][0] + \
                                self.params['travel_time'] [0][j]- \
                                self.params['M'] * (1 - self.u[v][h][j])
                        )

                        self.solver.Add(
                            self.a[j][v][h] >= self.a[i][v][h] + \
                                self.params['service_time'][i] + \
                                self.params['travel_time'][i][j] - \
                                self.params['M'] * (1 - self.y[v][h][j][i])
                        )
        print('.', end = '')
        for p in range(self.params['num_products']):
            for v in range(self.params['num_vehicles']):
                for f in range(self.params['num_batches']):
                    self.solver.Add(
                        self.st[v][1] >= self.c[p][f] + \
                            self.params['service_time'][0] - \
                            self.params['M'] * ( self.t[v][1][f])
                    )
        print('.', end = '')
        for p in range(self.params['num_products']):
            for f in range(self.params['num_batches']):
                for v in range(self.params['num_vehicles']):
                    for h in range(self.params['num_trips'] - 1):
                        self.solver.Add(
                            self.st[v][h+1] >= self.a[
                                self.params['num_customers'] + 1
                            ][v][h] + self.params['service_time'][
                                self.params['num_customers'] + 1
                            ] and self.a[
                                self.params['num_customers']+1
                            ][v][h] <= self.c[p][f]
                        )
    
                        self.solver.Add(
                            self.st[v][h+1] >= self.c[p][f] + \
                                self.params['service_time'][0] - \
                                self.params['M'] * (1 - self.t[v][h+1][f])
                        )
        print('.', end = '')
        for j in range(1, self.params['num_customers'] + 1):
            for v in range(self.params['num_vehicles']):
                for h in range(self.params['num_trips']):
                    self.solver.Add(
                        self.e[j][v][h] >= \
                        self.params['time_windows'][j][0] - self.a[j][v][h]
                    )

                    self.solver.Add(
                        self.l[j][v][h] >= self.a[j][v][h] - self.params[
                            'time_windows'
                        ][j][0]
                    )
        print('.')
        print('Building Objective.......')

        self.solver.Minimize(
            self.params['processing_cost'] * sum([
                sum([
                    self.params['process_time'][p] * \
                    self.params['demand'][p][j] for p in range(
                        self.params['num_products']
                    )
                ]) for j in range(self.params['num_customers'])
            ]) + self.params['setup_cost'] * sum([
                sum([
                    self.params['setup_time'][p][q] * \
                    self.x[p][q] for q in range(self.params['num_products'])
                ]) for p in range(self.params['num_products'])
            ]) + self.params['travel_cost'] * sum([
                sum([
                    sum([
                        sum([
                            self.params['travel_time'][i][j] * \
                            self.y[v][h][j][i] for i in range(
                                1,
                                self.params['num_customers'] + 1
                            )
                        ]) for j in range(1, self.params['num_customers']+1)
                    ]) for h in range(self.params['num_trips'])
                ]) for v in range(self.params['num_vehicles'])
            ]) + sum([
                self.params['vehicle_cost'][v] * self.w[v] \
                for v in range(self.params['num_vehicles'])
            ]) + self.params['early_delivery_penalty'] * sum([
                sum([
                    sum([
                        self.e[j][v][h] for j in range(
                            1,
                            self.params['num_customers'] + 1
                        )
                    ]) for h in range(self.params['num_trips'])
                ]) for v in range(self.params['num_vehicles'])
            ]) + self.params['late_delivery_penalty'] * sum([
                sum([
                    sum([
                        self.l[j][v][h] for j in range(
                            1,
                            self.params['num_customers'] + 1
                        )
                    ]) for h in range(self.params['num_trips'])
                ]) for v in range(self.params['num_vehicles'])
            ])
        )

        self.built = True
        print('Building Done............')

    def num_variables(self):
        return self.solver.NumVariables()

    def solve(self):
        status = self.solver.Solve()
        print('Solving Done...........')
        if status == pywraplp.Solver.OPTIMAL:
            print('Obtained optimal solution')
        else:
            print('The problem does not have an optimal solution.')
        self.solved = True
        return status
