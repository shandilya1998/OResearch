import numpy as np
import ortools
from ortools.linear_solver import pywraplp
from ortools.sat.python import cp_model

class Model:
    def __init__(self, params, solver='MILP'):
        self.params = params
        if solver == 'MILP':
            print('Creating MILP solver')
            self.solver = pywraplp.Solver.CreateSolver('SCIP')
            self.Var = self.solver.IntVar
        elif solver == 'LP':
            print('Creating LP solver')
            self.solver = pywraplp.Solver.CreateSolver('GLOP')
            self.Var = self.solver.NumVar
        else:
            raise ValueError('Expected one of MILP or LP solvers\
                , but got {s}'.format(s = solver))
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
        self.status = 'SOLVING NOT STARTED'

    def get_solution(self):
        solution = {
            's' : [
                [
                    self.s[p][f].solution_value() \
                    for f in range(self.params['num_batches'])
                ] for p in range(self.params['num_products'])
            ],
            'c' : [
                [
                    self.c[p][f].solution_value() \
                    for f in range(self.params['num_batches'])
                ] for p in range(self.params['num_products'])
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
                    for p in range(self.params['num_products'])
                ] for q in range(self.params['num_products'])
            ],
            'b' : [
                [
                    self.b[j][f].solution_value() \
                    for f in range(self.params['num_batches'])
                ] for j in range(self.params['num_customers'] + 2)
            ],
            'd' : [
                self.d[f].solution_value() \
                for f in range(self.params['num_batches'])
            ],
            'g' : [
                [
                    self.g[f][f_].solution_value() \
                    for f_ in range(self.params['num_batches'])
                ] for f in range(self.params['num_batches'])
            ],
            't' : [
                [
                    [
                        self.t[f][v][h].solution_value() \
                        for h in range(self.params['num_trips'])
                    ] for v in range(self.params['num_vehicles'])
                ] for f in range(self.params['num_batches'])
            ],
            'u' : [
                [
                    [
                        self.u[j][v][h].solution_value() \
                        for h in range(self.params['num_trips'])
                    ] for v in range(self.params['num_vehicles'])
                ] for j in range(self.params['num_customers'] + 2)
            ],
            'y' : [
                [
                    [
                        [
                            self.y[i][j][v][h].solution_value() \
                            for h in range(self.params['num_trips'])
                        ] for v in range(self.params['num_vehicles'])
                    ] for j in range(self.params['num_customers'] + 2)
                ] for i in range(self.params['num_customers'] + 2)
            ],
            'w' : [
                self.w[v].solution_value() \
                for v in range(self.params['num_vehicles'])
            ],
            'objective' : self.solver.Objective().Value(),
            'solving_time' : self.solver.wall_time(),
            'solving_iterations' : self.solver.iterations(),
            'status' : self.status
        }
        return solution

    def build(self):
        print('Building Variables.')
        self.s = np.array([
            [
                self.Var(
                    0.0,
                    self.infinity,
                    'start time product `{p}` batch `{f}`'.format(
                        p = p, 
                        f = f
                    )
                ) for f in range(self.params['num_batches'])
            ] for p in range(self.params['num_products'])
        ])
        self.c = np.array([
            [
                self.Var(
                    0.0,
                    self.infinity,
                    'completion time product {p} batch {f}'.format(
                        p = p, 
                        f = f
                    )
                ) for f in range(self.params['num_batches'])
            ] for p in range(self.params['num_products'])
        ])
        self.st = np.array([
            [
                self.Var(
                    0.0,
                    self.infinity,
                    'delivery start time vehicle {v} trip {h}'.format(
                        v=v, 
                        h=h
                    )
                ) for h in range(self.params['num_trips'])
            ] for v in range(self.params['num_vehicles'])
        ])
        self.a = np.array([
            [
                [
                    self.Var(
                        0.0,
                        self.infinity,
                        'delivery arrival time \
                            customer {j} \
                            vehicle {v} \
                            trip {h}'.format(
                            j=j, v=v, h=h)
                    ) for h in range(self.params['num_trips'])
                ] for v in range(self.params['num_vehicles'])
            ] for j in range(self.params['num_customers'] + 2)
        ])
        self.e = np.array([
            [
                [
                    self.Var(
                        0.0,
                        self.infinity,
                        'early delivery time \
                            customer {j} \
                            vehicle {v} \
                            trip {h}'.format(
                            j=j, v=v, h=h)
                    ) for h in range(self.params['num_trips'])
                ] for v in range(self.params['num_vehicles'])
            ] for j in range(self.params['num_customers'] + 2)
        ])
        self.l = np.array([
            [
                [
                    self.Var(
                        0.0,
                        self.infinity,
                        'late delivery time \
                            customer {j} \
                            vehicle {v} \
                            trip {h}'.format(
                            j=j, v=v, h=h)
                    ) for h in range(self.params['num_trips'])
                ] for v in range(self.params['num_vehicles'])
            ] for j in range(self.params['num_customers'] + 2)
        ])
        self.x = np.array([
            [
                self.solver.BoolVar(
                    'production transition from \
                        product {p} \
                        to product {q}'.format(
                        p=p, q=q)
                ) for q in range(self.params['num_products'])
            ] for p in range(self.params['num_products'])
        ])
        self.b = np.array([
            [
                self.solver.BoolVar(
                    'order production customer {j} batch {f}'.format(
                        j = j,
                        f = f
                    )
                ) for f in range(self.params['num_batches'])
            ] for j in range(self.params['num_customers'] + 2)
        ])
        self.d = np.array([
            self.solver.BoolVar(
                'batch activity {f}'.format(f=f)
            ) for f in range(self.params['num_batches'])
        ])
        self.g = np.array([
            [
                self.solver.BoolVar(
                    'production transition from batch {f} to batch {f_}'.\
                        format(
                            f = f,
                            f_ = f_
                    )
                ) for f_ in range(self.params['num_batches'])
            ] for f in range(self.params['num_batches'])
        ])
        self.t = np.array([
            [
                [
                    self.solver.BoolVar(
                        'batch {f} vehicle {v} trip {h} map'.format(
                            f = f,
                            h = h,
                            v = v
                        )
                    ) for h in range(self.params['num_trips'])
                ] for v in range(self.params['num_vehicles'])
            ] for f in range(self.params['num_batches'])
        ])
        self.u = np.array([
            [
                [
                    self.solver.BoolVar(
                        'customer {j} visit vehicle {v} trip {h}'.format(
                            j = j,
                            v = v,
                            h = h
                        )
                    ) for h in range(self.params['num_trips'])
                ] for v in range(self.params['num_vehicles'])
            ] for j in range(self.params['num_customers'] + 2)
        ])
        self.y = np.array([
            [
                [
                    [
                        self.solver.BoolVar(
                            'customer delivery transition from \
                                customer {i} to \
                                customer {j} \
                                vehicle {v} \
                                trip {h}'.format(
                                i = i,
                                j = j,
                                v = v,
                                h = h
                            )
                        ) for h in range(self.params['num_trips'])
                    ] for v in range(self.params['num_vehicles'])
                ] for j in range(self.params['num_customers'] + 2)
            ] for i in range(self.params['num_customers'] + 2)
        ])
        self.w = np.array([
            self.solver.BoolVar(
                'vehicle {v} usage'.format(v=v)
            ) for v in range(self.params['num_vehicles'])
        ])
        print('Building Constraints.')
        for j in range(1, self.params['num_customers'] + 1):
            self.solver.Add(np.sum(self.u, (1, 2))[j] == 1)
        for j in range(self.params['num_customers'] + 2):
            for h in range(self.params['num_trips']):
                for v in range(self.params['num_vehicles']):
                    self.solver.Add(self.u[0][v][h] >= self.u[j][v][h])
        for v in range(self.params['num_vehicles']):
            for h in range(self.params['num_trips']):
                self.solver.Add(
                    sum([
                        sum([
                            self.params['demand'][j][p] * \
                            self.u[j][v][h] \
                            for p in range(self.params['num_products'])
                        ]) for j in range(
                            1, 
                            self.params['num_customers'] + 1
                        )
                    ]) <= self.params['vehicle_capacity'][v]
                )
        for i in range(1, self.params['num_customers'] + 1):
            for j in range(1, self.params['num_customers'] + 1):
                for v in range(self.params['num_vehicles']):
                    for h in range(self.params['num_trips']):
                        self.solver.Add(
                            self.y[0][i][v][h] + \
                            self.y[0][j][v][h] + \
                            self.u[i][v][h] + \
                            self.u[j][v][h] <= 3
                        )
        for j in range(1, self.params['num_customers']+1):
            for v in range(self.params['num_vehicles']):
                for h in range(self.params['num_trips']):
                    self.solver.Add(
                        self.u[j][v][h] == np.sum(self.y, 0)[j][v][h] - \
                            self.y[j][j][v][h] - \
                            self.y[self.params['num_customers']+1][j][v][h]
                    )
                    self.solver.Add(
                        self.u[j][v][h] == np.sum(self.y, 0)[j][v][h] - \
                            self.y[j][j][v][h] - \
                            self.y[0][j][v][h]
                    )
        for i in range(1, self.params['num_customers']+1):
            for j in range(1, self.params['num_customers']+1):
                for v in range(self.params['num_vehicles']):
                    for h in range(self.params['num_trips']):
                        self.solver.Add(
                            self.u[i][v][h] >= self.y[i][j][v][h] + \
                                self.u[j][v][h] - 1
                        )
                        self.solver.Add(
                            self.u[j][v][h] >= self.y[i][j][v][h] + \
                                self.u[i][v][h] - 1
                        )
        for v in range(self.params['num_vehicles']):
            for h in range(self.params['num_trips'] - 1):
                self.solver.Add(
                    self.params['M']*(
                        np.sum(self.u, 0)[v][h] - \
                        self.u[0][v][h] - \
                        self.u[self.params['num_customers'] + 1][v][h]
                    ) >= np.sum(self.u, 0)[v][h + 1] - \
                        self.u[0][v][h + 1] - \
                        self.u[self.params['num_customers'] + 1][v][h + 1]
                )
        for v in range(self.params['num_vehicles']):
            for h in range(self.params['num_trips']):
                self.solver.Add(
                    self.u[0][v][h] >= self.w[v]
                )
        for p in range(self.params['num_products']):
            self.solver.Add(
                np.sum(self.x, -1)[p] - self.x[p][p] == 1 \
                and \
                np.sum(self.x, 0)[p] - self.x[p][p] == 1
            )
        for p in range(self.params['num_products']):
            for q in range(self.params['num_products']):
                self.solver.Add(
                    self.x[p][q] <= 1 - self.x[q][p]
                )
        self.solver.Add(
            np.sum(self.u, (1, 2))[0] == np.sum(self.d)
        )
        for f in range(self.params['num_batches']-1):
            self.solver.Add(
                self.d[f] >= self.d[f+1]
            )
        for v in range(self.params['num_vehicles']):
            for h in range(self.params['num_trips']):
                self.solver.Add(
                    np.sum(self.t, 0)[v][h] == self.u[0][v][h]
                )
        for f in range(self.params['num_batches']):
            self.solver.Add(
                self.d[f] == np.sum(self.t, (1, 2))[f]
            )
        for j in range(1, self.params['num_customers'] + 1):
            self.solver.Add(
                np.sum(self.b, -1)[j] == 1
            )
        for f in range(self.params['num_customers']):
            for j in range(1, self.params['num_customers']+1):
                for v in range(self.params['num_vehicles']):
                    for h in range(self.params['num_trips']):
                        self.solver.Add(
                            self.b[j][f] + 1 >= self.u[j][v][h] + \
                                self.t[f][v][h]
                        )
        for f in range(self.params['num_customers']):
            for j in range(1, self.params['num_customers']+1):
                for v in range(self.params['num_vehicles']):
                    for h in range(self.params['num_trips']):
                        self.solver.Add(
                            self.t[f][v][h] + 1 >= self.b[j][f] + \
                                self.u[j][v][h]
                        )
        for f in range(self.params['num_batches']):
            self.solver.Add(
                np.sum(self.g, 0)[f] - self.g[f][f] == self.d[f]
            )
            self.solver.Add(
                np.sum(self.g, 1)[f] - self.g[f][f] == self.d[f]
            )
        for p in range(self.params['num_products']):
            for f in range(self.params['num_batches']):
                self.solver.Add(
                    np.sum(
                        self.params['setup_time'] * self.x,
                        (0, 1)
                    ) + sum([
                        sum([
                            self.params['process_time'][q] * \
                            self.params['demand'][j][q] * \
                            self.b[j][f] \
                            for j in range(
                                1, 
                                self.params['num_customers'] + 1
                            )
                        ]) for q in range(self.params['num_products'])
                    ]) - self.params['M'] * (1- self.g[0][f]) <= \
                        self.c[p][f]
                )
                for f_ in range(self.params['num_batches']):
                    self.solver.Add(
                        self.s[p][f] + np.sum(
                            self.params['setup_time'] * self.x,
                            (0, 1)
                        ) + sum([
                            sum([
                                self.params['process_time'][q] * \
                                self.params['demand'][j][q] * \
                                self.b[j][f] \
                                for j in range(
                                    1,
                                    self.params['num_customers'] + 1
                                )
                            ]) for q in range(self.params['num_products'])
                        ]) - self.params['M'] * (1 - self.g[f][f_]) <= \
                            self.c[p][f_]
                    )
        for j in range(1, self.params['num_customers']+1):
            for v in range(self.params['num_vehicles']):
                for h in range(self.params['num_trips']):
                    self.solver.Add(
                        self.a[j][v][h] >= self.st[v][h] + \
                            self.params['service_time'][0] + \
                            self.params['travel_time'][0][j]- \
                            self.params['M'] * (1 - self.u[j][v][h])
                    )
                    for i in range(self.params['num_customers'] + 1):
                        self.solver.Add(
                            self.a[j][v][h] >= self.a[i][v][h] + \
                                self.params['service_time'][i] + \
                                self.params['travel_time'][i][j] - \
                                self.params['M'] * (1 - self.y[i][j][v][h])
                        )
        for p in range(self.params['num_products']):
            for v in range(self.params['num_vehicles']):
                for f in range(self.params['num_batches']):
                    self.solver.Add(
                        self.st[v][1] >= self.c[p][f] + \
                            self.params['service_time'][0] - \
                            self.params['M'] * (1 - self.t[f][v][1])
                    )
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
                                self.params['M'] * (1 - self.t[f][v][h+1])
                        )
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
                        ][j][1]
                    ) 
        print('Building Objective.')

        self.solver.Minimize(
            self.params['processing_cost'] * np.sum(
                self.params['process_time'] * self.params['demand']    
            ) + \
            self.params['setup_cost'] * np.sum(
                self.params['setup_time'] * self.x
            ) + \
            self.params['travel_cost'] * np.sum(
                self.params['travel_time'][1:-1, 1:-1] * \
                    np.sum(self.y[1:-1, 1:-1], (2, 3)) 
            ) + \
            np.sum(
                self.params['vehicle_cost'] * self.w
            ) + \
            self.params['early_delivery_penalty'] * np.sum(
                self.e[1:-1]
            ) + \
            self.params['late_delivery_penalty'] * np.sum(
                self.l[1:-1]
            )
        )

        self.built = True
        print('Building Done.')

    def num_variables(self):
        return self.solver.NumVariables()

    def solve(self):
        status = self.solver.Solve()
        print('Solving Done.')
        if status == pywraplp.Solver.OPTIMAL:
            self.status = 'OPTIMAL'
            print('Obtained optimal solution')
        elif status == pywraplp.Solver.FEASIBLE:
            self.status = 'FEASIBLE'
            print('The problem does has a feasible solution.')
        elif status == pywraplp.Solver.INFEASIBLE:
            self.status = 'INFEASIBLE'
            print('The problem does not have a feasible solution')
        elif status == pywraplp.Solver.NOT_SOLVED:
            self.status = 'NOT SOLVED'
            print('The problem could not be solved')
        elif status == pywraplp.Solver.UNBOUNDED:
            self.status = 'UNBOUNDED SOLUTION'
            print('The problem has unbounded solutions')
        elif status == pywraplp.Solver.ABNORMAL:
            self.status = 'ABNORMAL'
            print('The problem has an abnormal solution')
        self.solved = True
        return self.status


