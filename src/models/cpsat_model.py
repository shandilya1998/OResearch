import numpy as np
import ortools
from ortools.sat.python import cp_model

class CPSATModel:
    def __init__(self, params):
        self.params = params
        self.model = cp_model.CpModel()
        self.solver = cp_model.CpSolver()
        self.infinity = self.params['large_int']
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
                    self.solver.Value(self.s[p][f]) \
                    for f in range(self.params['num_batches'])
                ] for p in range(self.params['num_products'])
            ],
            'c' : [
                [
                    self.solver.Value(self.c[p][f]) \
                    for f in range(self.params['num_batches'])
                ] for p in range(self.params['num_products'])
            ],
            'st' : [
                [
                    self.solver.Value(self.st[v][h]) \
                    for h in range(self.params['num_trips'])
                ] for v in range(self.params['num_vehicles'])
            ],
            'a' : [
                [
                    [
                        self.solver.Value(self.a[j][v][h]) \
                        for h in range(self.params['num_trips'])
                    ] for v in range(self.params['num_vehicles'])
                ] for j in range(self.params['num_nodes'])
            ],
            'e' : [
                [
                    [
                        self.solver.Value(self.e[j][v][h]) \
                        for h in range(self.params['num_trips'])
                    ] for v in range(self.params['num_vehicles'])
                ] for j in range(self.params['num_nodes'])
            ],
            'l' : [
                [
                    [
                        self.solver.Value(self.l[j][v][h]) \
                        for h in range(self.params['num_trips'])
                    ] for v in range(self.params['num_vehicles'])
                ] for j in range(self.params['num_nodes'])
            ],
            'x' : [
                [
                    self.solver.Value(self.x[p][q]) \
                    for p in range(self.params['num_products'])
                ] for q in range(self.params['num_products'])
            ],
            'b' : [
                [
                    self.solver.Value(self.b[j][f]) \
                    for f in range(self.params['num_batches'])
                ] for j in range(self.params['num_customers'])
            ],
            'd' : [
                self.solver.Value(self.d[f]) \
                for f in range(self.params['num_batches'])
            ],
            'g' : [
                [
                    self.solver.Value(self.g[f][f_]) \
                    for f_ in range(self.params['num_batches'])
                ] for f in range(self.params['num_batches'])
            ],
            't' : [
                [
                    [
                        self.solver.Value(self.t[f][v][h]) \
                        for h in range(self.params['num_trips'])
                    ] for v in range(self.params['num_vehicles'])
                ] for f in range(self.params['num_batches'])
            ],
            'u' : [
                [
                    [
                        self.solver.Value(self.u[j][v][h]) \
                        for h in range(self.params['num_trips'])
                    ] for v in range(self.params['num_vehicles'])
                ] for j in range(self.params['num_nodes'])
            ],
            'y' : [
                [
                    [
                        [
                            self.solver.Value(self.y[i][j][v][h]) \
                            for h in range(self.params['num_trips'])
                        ] for v in range(self.params['num_vehicles'])
                    ] for j in range(self.params['num_nodes'])
                ] for i in range(self.params['num_nodes'])
            ],
            'w' : [
                self.solver.Value(self.w[v]) \
                for v in range(self.params['num_vehicles'])
            ],
            'objective' : self.solver.ObjectiveValue(),
            'solving_time' : self.solver.WallTime(),
            'status' : self.status
        }
        return solution

    def build(self):
        print('Building Variables.')
        self.s = np.array([
            [
                self.model.NewIntVar(
                    0,
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
                self.model.NewIntVar(
                    0,
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
                self.model.NewIntVar(
                    0,
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
                    self.model.NewIntVar(
                        0,
                        self.infinity,
                        'delivery arrival time \
                            customer {j} \
                            vehicle {v} \
                            trip {h}'.format(
                            j=j, v=v, h=h)
                    ) for h in range(self.params['num_trips'])
                ] for v in range(self.params['num_vehicles'])
            ] for j in range(self.params['num_nodes'])
        ])
        self.e = np.array([
            [
                [
                    self.model.NewIntVar(
                        0,
                        self.infinity,
                        'early delivery time \
                            customer {j} \
                            vehicle {v} \
                            trip {h}'.format(
                            j=j, v=v, h=h)
                    ) for h in range(self.params['num_trips'])
                ] for v in range(self.params['num_vehicles'])
            ] for j in range(self.params['num_nodes'])
        ])
        self.l = np.array([
            [
                [
                    self.model.NewIntVar(
                        0,
                        self.infinity,
                        'late delivery time \
                            customer {j} \
                            vehicle {v} \
                            trip {h}'.format(
                            j=j, v=v, h=h)
                    ) for h in range(self.params['num_trips'])
                ] for v in range(self.params['num_vehicles'])
            ] for j in range(self.params['num_nodes'])
        ])
        self.x = np.array([
            [
                self.model.NewBoolVar(
                    'production transition from \
                        product {p} \
                        to product {q}'.format(
                        p=p, q=q)
                ) for q in range(self.params['num_products'])
            ] for p in range(self.params['num_products'])
        ])
        self.b = np.array([
            [
                self.model.NewBoolVar(
                    'order production customer {j} batch {f}'.format(
                        j = j,
                        f = f
                    )
                ) for f in range(self.params['num_batches'])
            ] for j in range(self.params['num_customers'])
        ])
        self.d = np.array([
            self.model.NewBoolVar(
                'batch activity {f}'.format(f=f)
            ) for f in range(self.params['num_batches'])
        ])
        self.g = np.array([
            [
                self.model.NewBoolVar(
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
                    self.model.NewBoolVar(
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
                    self.model.NewBoolVar(
                        'customer {j} visit vehicle {v} trip {h}'.format(
                            j = j,
                            v = v,
                            h = h
                        )
                    ) for h in range(self.params['num_trips'])
                ] for v in range(self.params['num_vehicles'])
            ] for j in range(self.params['num_nodes'])
        ])
        self.y = np.array([
            [
                [
                    [
                        self.model.NewBoolVar(
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
                ] for j in range(self.params['num_nodes'])
            ] for i in range(self.params['num_nodes'])
        ])
        self.w = np.array([
            self.model.NewBoolVar(
                'vehicle {v} usage'.format(v=v)
            ) for v in range(self.params['num_vehicles'])
        ])
        print('Building Constraints.')
        for j in range(1, self.params['num_nodes'] - 1):
            self.model.Add(np.sum(self.u, (1, 2))[j] == 1)
        for j in range(self.params['num_nodes']):
            for h in range(self.params['num_trips']):
                for v in range(self.params['num_vehicles']):
                    self.model.Add(self.u[0][v][h] >= self.u[j][v][h])
        for v in range(self.params['num_vehicles']):
            for h in range(self.params['num_trips']):
                self.model.Add(
                    sum([
                        sum([
                            self.params['demand'][j][p] * \
                            self.u[j][v][h] \
                            for p in range(self.params['num_products'])
                        ]) for j in range(
                            1, 
                            self.params['num_nodes'] - 1
                        )
                    ]) <= self.params['vehicle_capacity'][v]
                )
        for i in range(1, self.params['num_nodes'] - 1):
            for j in range(1, self.params['num_nodes'] - 1):
                for v in range(self.params['num_vehicles']):
                    for h in range(self.params['num_trips']):
                        self.model.Add(
                            self.y[0][i][v][h] + \
                            self.y[0][j][v][h] + \
                            self.u[i][v][h] + \
                            self.u[j][v][h] <= 3
                        )
        for j in range(1, self.params['num_nodes'] - 1):
            for v in range(self.params['num_vehicles']):
                for h in range(self.params['num_trips']):
                    self.model.Add(
                        self.u[j][v][h] == np.sum(self.y, 0)[j][v][h] - \
                            self.y[j][j][v][h] - \
                            self.y[self.params['num_nodes'] - 1][j][v][h]
                    )
                    self.model.Add(
                        self.u[j][v][h] == np.sum(self.y, 0)[j][v][h] - \
                            self.y[j][j][v][h] - \
                            self.y[0][j][v][h]
                    )
        for i in range(1, self.params['num_nodes'] - 1):
            for j in range(1, self.params['num_nodes'] - 1):
                for v in range(self.params['num_vehicles']):
                    for h in range(self.params['num_trips']):
                        self.model.Add(
                            self.u[i][v][h] >= self.y[i][j][v][h] + \
                                self.u[j][v][h] - 1
                        )
                        self.model.Add(
                            self.u[j][v][h] >= self.y[i][j][v][h] + \
                                self.u[i][v][h] - 1
                        )
        for v in range(self.params['num_vehicles']):
            for h in range(self.params['num_trips'] - 1):
                self.model.Add(
                    self.params['M']*(
                        np.sum(self.u, 0)[v][h] - \
                        self.u[0][v][h] - \
                        self.u[self.params['num_nodes'] - 1][v][h]
                    ) >= np.sum(self.u, 0)[v][h + 1] - \
                        self.u[0][v][h + 1] - \
                        self.u[self.params['num_nodes'] - 1][v][h + 1]
                )
        for v in range(self.params['num_vehicles']):
            for h in range(self.params['num_trips']):
                self.model.Add(
                    self.u[0][v][h] >= self.w[v]
                )
        for p in range(self.params['num_products']):
            self.model.Add(
                np.sum(self.x, -1)[p] - self.x[p][p] == 1 \
                and \
                np.sum(self.x, 0)[p] - self.x[p][p] == 1
            )
        for p in range(self.params['num_products']):
            for q in range(self.params['num_products']):
                self.model.Add(
                    self.x[p][q] <= 1 - self.x[q][p]
                )
        self.model.Add(
            np.sum(self.u, (1, 2))[0] == np.sum(self.d)
        )
        for f in range(self.params['num_batches']-1):
            self.model.Add(
                self.d[f] >= self.d[f+1]
            )
        for v in range(self.params['num_vehicles']):
            for h in range(self.params['num_trips']):
                self.model.Add(
                    np.sum(self.t, 0)[v][h] == self.u[0][v][h]
                )
        for f in range(self.params['num_batches']):
            self.model.Add(
                self.d[f] == np.sum(self.t, (1, 2))[f]
            )
        for j in range(1, self.params['num_nodes'] - 1):
            self.model.Add(
                np.sum(self.b, -1)[j - 1] == 1
            )
        for f in range(self.params['num_batches']):
            for j in range(1, self.params['num_nodes'] - 1):
                for v in range(self.params['num_vehicles']):
                    for h in range(self.params['num_trips']):
                        self.model.Add(
                            self.b[j - 1][f] + 1 >= self.u[j][v][h] + \
                                self.t[f][v][h]
                        )
        for f in range(self.params['num_batches']):
            for j in range(1, self.params['num_nodes'] - 1):
                for v in range(self.params['num_vehicles']):
                    for h in range(self.params['num_trips']):
                        self.model.Add(
                            self.t[f][v][h] + 1 >= self.b[j - 1][f] + \
                                self.u[j][v][h]
                        )
        for f in range(self.params['num_batches']):
            self.model.Add(
                np.sum(self.g, 0)[f] - self.g[f][f] == self.d[f]
            )
            self.model.Add(
                np.sum(self.g, 1)[f] - self.g[f][f] == self.d[f]
            )
        for p in range(self.params['num_products']):
            for f in range(self.params['num_batches']):
                self.model.Add(
                    np.sum(
                        self.params['setup_time'] * self.x,
                        (0, 1)
                    ) + sum([
                        sum([
                            self.params['process_time'][q] * \
                            self.params['demand'][j][q] * \
                            self.b[j - 1][f] \
                            for j in range(
                                1,
                                self.params['num_nodes'] - 1
                            )
                        ]) for q in range(self.params['num_products'])
                    ]) - self.params['M'] * (1- self.g[0][f]) <= \
                        self.c[p][f]
                )
                for f_ in range(self.params['num_batches']):
                    self.model.Add(
                        self.s[p][f] + np.sum(
                            self.params['setup_time'] * self.x,
                            (0, 1)
                        ) + sum([
                            sum([
                                self.params['process_time'][q] * \
                                self.params['demand'][j][q] * \
                                self.b[j - 1][f] \
                                for j in range(
                                    1,
                                    self.params['num_nodes'] - 1
                                )
                            ]) for q in range(self.params['num_products'])
                        ]) - self.params['M'] * (1 - self.g[f][f_]) <= \
                            self.c[p][f_]
                    )
        for j in range(1, self.params['num_nodes'] - 1):
            for v in range(self.params['num_vehicles']):
                for h in range(self.params['num_trips']):
                    self.model.Add(
                        self.a[j][v][h] >= self.st[v][h] + \
                            self.params['service_time'][0] + \
                            self.params['travel_time'][0][j]- \
                            self.params['M'] * (1 - self.u[j][v][h])
                    )
                    for i in range(self.params['num_nodes'] - 1):
                        self.model.Add(
                            self.a[j][v][h] >= self.a[i][v][h] + \
                                self.params['service_time'][i] + \
                                self.params['travel_time'][i][j] - \
                                self.params['M'] * (1 - self.y[i][j][v][h])
                        )
        for p in range(self.params['num_products']):
            for v in range(self.params['num_vehicles']):
                for f in range(self.params['num_batches']):
                    self.model.Add(
                        self.st[v][1] >= self.c[p][f] + \
                            self.params['service_time'][0] - \
                            self.params['M'] * (1 - self.t[f][v][1])
                    )
        for p in range(self.params['num_products']):
            for f in range(self.params['num_batches']):
                for v in range(self.params['num_vehicles']):
                    for h in range(self.params['num_trips'] - 1):
                        self.model.Add(
                            self.st[v][h+1] >= self.a[
                                self.params['num_nodes'] - 1
                            ][v][h] + self.params['service_time'][
                                self.params['num_nodes'] - 1
                            ] and self.a[
                                self.params['num_nodes'] - 1
                            ][v][h] <= self.c[p][f]
                        )
                        self.model.Add(
                            self.st[v][h+1] >= self.c[p][f] + \
                                self.params['service_time'][0] - \
                                self.params['M'] * (1 - self.t[f][v][h+1])
                        )
        for j in range(1, self.params['num_nodes'] - 1):
            for v in range(self.params['num_vehicles']):
                for h in range(self.params['num_trips']):
                    self.model.Add(
                        self.e[j][v][h] >= \
                        self.params['time_windows'][j][0] - self.a[j][v][h]
                    )

                    self.model.Add(
                        self.l[j][v][h] >= self.a[j][v][h] - self.params[
                            'time_windows'
                        ][j][1]
                    ) 
        print('Building Objective.')

        self.model.Minimize(
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

    def stats(self):
        return self.model.ModelStats()

    def response_stats(self):
        if self.solved:
            return self.solver.ResponseStats()

    def solve(self):
        status = self.solver.Solve(self.model)
        print('Solving Done.')
        if status == cp_model.OPTIMAL:
            self.status = 'OPTIMAL'
            print('Obtained optimal solution')
        elif status == cp_model.FEASIBLE:
            self.status = 'FEASIBLE'
            print('The problem does has a feasible solution.')
        elif status == cp_model.INFEASIBLE:
            self.status = 'INFEASIBLE'
            print('The problem does not have a feasible solution')
        self.solved = True
        return self.status


