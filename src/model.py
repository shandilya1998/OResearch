import ortools
from ortools.linear_solver import pywraplp
from src.constants import *

class MILP:
    def __init__(self, params, solver = None):
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
                    v = self.params['num_vehicles'], 
                    c = self.params['num_customers']
                )
            )

    def build(self):
        print('Building Variables.......')
        self.s = [
            [ 
                self.solver.IntVar(
                    0.0, 
                    self.infinity, 
                    'start time product `{i}` batch `{j}`'.format(i=i, j=j)
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
            ] for j in range(self.params['num_customers']+2)
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
            ] for j in range(self.params['num_customers']+2)
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
            ] for j in range(self.params['num_customers']+2)
        ]

        self.x = [
            [
                self.solver.BoolVar(
                    'production transition from product {p} to product {q}'.format(p = p, q = q)
                ) for q in range(self.params['num_products'])
            ] for p in range(self.params['num_products']) 
        ]

        self.b = [
            [
                self.solver.BoolVar(
                    'order production customer {c} batch {f}'
                ) for f in range(self.params['num_customers'])
            ] for c in range(self.params['num_customers'] + 2)
        ]

        self.d = [
            self.solver.BoolVar(
                'batch activity {f}'.format(f=f)
            ) for f in range(self.params['num_customers'])
        ]

        self.g = [
            [
                self.solver.BoolVar(
                    'production transition from batch {p} to batch {q}'.format(p = p, q = q)
                ) for q in range(self.params['num_customers'])
            ] for p in range(self.params['num_customers'])
        ]

        self.t = [
            [ 
                [   
                    self.solver.BoolVar(
                        'batch {b} trip {t} vehicle {v} map'.format(
                            b = b, 
                            t = t, 
                            v = v
                        )
                    ) for b in range(self.params['num_customers'])
                ] for t in range(self.params['num_customers'])
            ] for v in range(self.params['num_vehicles'])
        ]

        self.u = [
            [
                [
                    self.solver.BoolVar(
                        'customer {i} visit trip {t} vehicle {v}'.format(
                            i = i,
                            t = t,
                            v = v
                        )
                    ) for i in range(self.params['num_customers']+2)
                ] for t in range(self.params['num_customers'])
            ] for v in range(self.params['num_vehicles'])
        ]

        self.y = [
            [
                [
                    [
                        self.solver.BoolVar(
                            'customer delivery transition from customer {i} to customer {j} trip {t} vehicle {v} '.format(
                                i = i,
                                j = j,
                                t = t,
                                v = v
                            )
                        ) for i in range(self.params['num_customers']+2)
                    ] for j in range(self.params['num_customers']+2)
                ] for t in range(self.params['num_customers'])
            ] for v in range(self.params['num_vehicles'])
        ]

        self.w = [
            self.solver.BoolVar(
                'vehicle {v} usage'.format(v=v)
            ) for v in range(self.params['num_vehicles'])
        ]

        print('Building Constraints.....')
        for c in range(1, self.params['num_customers']+1):
            self.solver.Add(sum([sum(u_)] for u_ in self.u[:][:][c]) == 1)

        for j in range(self.params['num_customers']+2):
            for h in range(self.params['num_customers']):
                for v in range(self.params['num_customers']):
                    self.solver.Add(self.u[v][h][0] >= u[j][h][v])

        for v in range(self.params['num_vehicles']):
            for h in range(self.params['num_customers']):
                self.solver.Add(
                    sum([
                        sum(
                            self.params['demand'][j][p]*u[j+1][v][h]
                        ) for p in range(
                            self.params['num_products']
                        )
                    ] for j in range( 
                            self.params['num_customers']
                        )
                    ) <= self.params['vehicle_capacity'][v]
                )

        for i in range(1, self.params['num_customers']+1):
            for j in range(1, self.params['num_customers']+1):
                for h in range(self.params['num_customers']):
                    for v in range(self.params['num_vehicles']):
                        self.solver.Add(
                            self.y[v][h][i][0] + \
                            self.y[v][h][j][0] + \
                            self.u[v][h][i] + \
                            self.u[v][h][j] <= 3
                        )

       for j in range(1, self.params['num_customers']+1):
            for h in range(self.params['num_customers']):
                for v in range(self.params['num_vehicles']):
                    self.solver.Add(
                        self.u[v][h][j] == sum(
                            [
                                self.y[v][h][j][i] if i!= 0 \
                                else 0.0 \
                                for i in range(self.params['self.num_customers']+1) 
                            ]
                        )
                    )

        for j in range(1, self.params['num_customers']+1):
            for h in range(self.params['num_customers']):
                for v in range(self.params['num_vehicles']):
                    self.solver.Add(
                        self.u[v][h][j] == sum(
                            [
                                self.y[v][h][i][j] if i!= 0 \
                                else 0.0 \
                                for i in range(1, self.params['self.num_customers']+2)
                            ]
                        )
                    )

        for i in range(1, self.params['num_customers']+1):
            for j in range(1, self.params['num_customers']+1):
                for h in range(self.params['num_customers']):
                    for v in range(self.params['num_vehicles']):
                        self.solver.Add(
                            self.u[v][h][i] >= self.y[v][h][j][i] + self.u[v][h][j] - 1
                        )

        for i in range(1, self.params['num_customers']+1):
            for j in range(1, self.params['num_customers']+1):
                for h in range(self.params['num_customers']):
                    for v in range(self.params['num_vehicles']):
                        self.solver.Add(
                            self.u[v][h][j] >= self.y[v][h][j][i] + self.u[v][h][i] - 1
                        )

        for v in range(self.params['num_vehicles']):
            for h in range(self.params['num_customers'] - 1):
                self.solver.Add(
                    self.params['M']*sum([
                        self.u[v][h][j] for j in range(
                            1,
                            self.params['num_customers'] + 1
                        )
                    ]) >= sum([
                        self.u[v][h+1][j] for j in range(
                            1,
                            self.params['num_customers'] + 1
                        )
                    ])
                )

        for v in range(self.params['num_vehicles']):
            for h in range(self.params['num_customers']):
                self.solver.Add(
                    self.u[v][h][0] >= self.w[v]
                )

        for p in range(self.params['num_products']):
            self.solver.Add(
                sum([
                    self.x[p][q] \
                    if p != q else 0 \
                    for q in range(self.params['num_products'])
                ]) == 1
            )

        for q in range(self.params['num_products']):
            self.solver.Add(
                sum([
                    self.x[p][q] \
                    if p != q else 0 \
                    for p in range(self.params['num_products'])
                ])
            )

        for p in range(self.params['num_products']):
            for q in range(self.params['num_prodcuts']):
                self.solver.Add(
                    self.x[p][q] <= 1 - self.x[q][p]
                )

        self.solver.Add(
            sum([
                sum([
                        self.u[v][h][0] for h in range(
                            self.params['num_customers']
                        )
                    ]) for v in range(self.params['num_vehicles'])
            ]) == sum(
                [self.d[f] for f in range(self.params['num_customers']
            )])
        )

        for f in range(self.params['num_customers']-1):
            self.solver.Add(
                self.d[f] >= self.d[f+1]
            )

        for v in range(self.params['num_vehicles']):
            for h in range(self.params['num_customers']):
                self.solver.Add(
                    sum([
                        self.t[f][h][v] for f in range(self.params['num_customers'])
                    ]) == self.u[v][h][0]
                )

        for f in range(self.params['num_customers']):
            self.solver.Add(
                self.d[f] == sum([
                    sum([
                        self.t[f][h][v] for h in range(self.params['num_customers'])
                    ]) for v in range(self.params['num_vehicles'])
                ])
            )

        for j in range(self.params['num_customers']+2):
            self.solver.Add(
                sum([
                    self.b[j][f] for f in range(self.params['num_customers'])
                ]) == 1
            )

        for f in range(self.params['num_customers']):
            for j in range(1, self.params['num_customers']+1):
                for h in range(self.params['num_customers']):
                    for v in range(self.params['num_vehicles']):
                        self.solver.Add(
                            self.b[j][f] + 1 >= self.u[v][h][j] + self.t[f][h][v]
                        )

        for f in range(self.params['num_customers']):
            for j in range(1, self.params['num_customers']+1):
                for h in range(self.params['num_customers']):
                    for v in range(self.params['num_vehicles']):
                        self.solver.Add(
                            self.t[f][h][v] + 1 >= self.b[j][f] + self.u[v][h][j]
                        )

        for f in range(self.params['num_customers']):
            self.solver.Add(
                sum([
                    self.g[f_][f] for f_ in range(self.params['num_customers'])
                ]) == self.d[f]
            )

        for p in range(self.params['num_products']):
            for f in range(self.params['num_customers']):
                self.solver.Add(
                    sum([
                        sum([
                            self.params['setup_time']*self.x[p_][q_] \
                            for q_ in range(self.params['num_products'])
                        ]) for p_ in range(self.params['num_products'])
                    ]) + sum([
                        sum([
                            self.params['process_time'][p_] * \
                            self.params['demand'][j][p_] * \
                            self.b[j+1][f] \
                            for j in range(self.params['num_customers'])
                        ]) for p_ in range(self.params['num_products'])
                    ]) - self.params['M'] * (1- self.g[0][f]) <= self.c[p][f]
                )

        for p in range(self.params['num_products']):
            for f in range(self.params['num_customers']):
                for f_ in range(self.params['num_customers']):
                    self.solver.Add(
                        self.s[p][f] + sum([
                            sum([
                                self.params['setup_time']*self.x[p_][q_] \
                                for q_ in range(self.params['num_products'])
                            ]) for p_ in range(self.params['num_products'])
                        ]) + sum([
                            sum([
                                self.params['process_time'][p_] * \ 
                                self.params['demand'][j][p_] * \ 
                                self.b[j+1][f] \
                                for j in range(self.params['num_customers'])
                            ]) for p_ in range(self.params['num_products'])
                        ]) - self.params['M'] * (1- self.g[f][f_]) <= self.c[p][f_]
                    )

        for i in range(1, self.params['num_customers']+1):
            for j in range(1, self.params['num_customers']+1):
                for h in range(self.params['num_customers']):
                    for v in range(self.params['num_vehicles']):
                        self.solver.Add(
                            self.a[j][v][h] == self.st[v][h] + \
                                self.params['service_time'] + \
                                self.params['travel_time'] - \
                                self.params['M'] * (1 - self.u[v][h][j])
                        )

                        self.solver.Add(
                            self.a[j][v][h] >= self.a[i][v][h] + \
                                self.params['service_time'][i] + \
                                self.params['travel_time'][i][j] - \
                                self.params['M'] * (1 - self.y[v][h][j][i])
                        )

        for p in range(self.params['num_products']):
            for v in range(self.params['num_vehicles']):
                for f in range(self.params['num_customers']):
                    self.solver.Add(
                        self.st[v][1] >= self.c[p][f] + \
                            self.params['service_time'][0] - \
                            self.params['M'] * ( self.t[v][1][f])
                    )

        for p in range(self.params['num_products']):
            for f in range(self.params['num_customers']):
                for v in range(self.params['num_vehicles'):
                    for h in range(self.params['num_customers'] - 1):
                        self.solver.Add(
                            self.st[v][h+1] >= self.a[
                                self.params['num_customers'] + 1
                            ][v][h] + self.params['service_time'][
                                self.params['num_customers'] + 1
                            ] and self.a[
                                self.params['num_customers']+1
                            ][v][h] < self.c[p][f]
                        )
    
                        self.solver.Add(
                            self.st[v][h+1] >= self.c[p][f] + \
                                self.params['service_time'][0] - \
                                self.params['M'] * (1 - self.t[v][h+1][f])
                        )

        for j in range(1, self.params['num_customers'] + 1):
            for v in range(self.params['num_vehicles']):
                for h in range(self.params['num_customers']):
                    self.solver.Add(
                        self.e[j][v][h] >= self.params[
                            'time_windows'
                        ][j][0] - self.a[j][v][h]
                    )

                    self.solver.Add(
                        self.l[j][v][h] >= self.a[j][v][h] - self.params[
                            'time_windows'
                        ][j][0]
                    ) 
        
        print('Building Objective.......')
        raise NotImplementedError

    def num_variables(self):
        return self.solver.NumVariables()

    def set_objective(self):
        raise NotImplementedError

    def solve(self):
        status = self.solver.Solve()
        return status
