import pulp
import os
import numpy as np
from tqdm import tqdm
import pandas as pd
import os
import xlsxwriter
import json

class PuLPModel:
    def __init__(self, params):
        self.params = params
        if os.path.exists('temp'):
            os.rmdir('temp')
        os.mkdir('temp')
        self.tmp_file_dir = 'temp'
        pulp.LpSolverDefault.tmpDir = self.tmp_file_dir

    def build(self):
        print('Building Variables.')
        self.f = np.array(
            [pulp.LpVariable(
                'f{},'.format(i), lowBound = 0
            ) for j in range(self.params['num_products'])]
        )
        self.F = pulp.LpVariable('F', lowBound = 0)
        self.k = np.array([
            [
                pulp.LpVariable('k{},{}'.format(i,j)) \
                    for j in range(self.params['num_trips'])
            ] for i in range(self.params['num_vehicles'])
        ])
        self.a = np.array([
            pulp.LpVariable('a{},'.format(i), lowBound = 0) \
                for i in range(self.parmas['num_customers'])
        ])
        self.l = np.array([
            pulp.LpVariable('l{},'.format(i), lowBound = 0) \
                for i in range(self.params['num_customers'])
        ])
        self.x = np.array([
            [
                pulp.LpVariable('x{},{}'.format(p,q), cat = 'Binary') \
                    for q in range(self.params['num_products'])
            ] for p in range(self.params['num_products'])
        ])
        self.y = np.array([
            [
                [
                    pulp.LpVariable('y{},{},{}'.format(i,v,h)) \
                        for h in range(self.params['num_trips'])
                ] for v in range(self.params['num_vehicles'])
            ] for i in range(self.params['num_nodes'])
        ])
        self.z = np.array([
            [
                [
                    [
                        pulp.LpVariable('z{},{},{},{}'.format(i,j,v,h)) \
                            for h in range(self.params['num_trips'])
                    ]
                ]
            ]
        ])
        self.w = np.array([
            pulp.LpVariable('x{},'.format(i)) \
                for i in range(self.params['num_vehicles'])
        ])

        print('Building Objective.')
        self.mc_1 = pulp.LpAffineExpression(np.concatenate([
            np.array(list(zip(self.x.flatten(), self.params['setup_time'].flatten()))),
        ])
        self.mc_2 = self.params['process_cost'].flatten() * \
                self.params['process_time'].flatten() * \
                self.params['demand'].flatten()

        self.dc = pulp.LpAffineExpression(np.concatenate([
            np.array(list(zip(self.w, self.params['vehicle_cost']))),
            np.array(list(zip(self.z.flatten(), np.expand_dims(
                np.repeat(np.expand_dims(
                    self.travel_time, -1
                ), self.params['num_trips']), -1
            ), self.params['num_vehicles'])))
        ])

        self.pc = pulp.LpAffineExpression(np.array(list(zip(
            self.l, self.params['late_delivery_penalty']
        ))))
        self.model += pulp.lpSum([self.dc, self.pc, self.mc_1, self.mc_2])

        print('Building Constraint.')

        lst_constraints = [
            self.constraint1,
            self.constraint2,
            self.constraint3,
            self.constraint4,
            self.constraint6,
            self.constraint7,
            self.constraint8,
            self.constraint9,
            self.constraint10,
            self.constraint11,
            self.constraint12,
            self.constraint13,
            self.constraint14,
            self.constraint15,
            self.constraint16,
            self.constraint17,
            self.constraint18,
            self.constraint19,
            self.constraint20,
            self.constraint21,
            self.constraint22,
        ]

        for constraint in tqdm(lst_constraints):
            constraint()

    def constraint1(self):
        for p in range(self.params['num_products']):
            self.model += pulp.lpSum([
                self.x[q][p] for q in range(self.params['num_products']) if p!=q
            ]) == 1, 'ProductionSeqConstraint1,{},'.format(p)
            self.model += pulp.lpSum([
                self.x[p][q] for q in range(self.params['num_products']) if q!= p
            ]) == 1, 'ProductionSeqConstraint2,{}'.format(p)

    def constraint2(self):
        for p in range(self.params['num_products']):
            self.model += self.f[p] - pulp.lpSum(
                    self.params['process_time'] * lp.lpSum(self.params['demand'][:, p])
            ) == 0, 'ProductionFinisTimeConstraint{},'.format(p)
            for q in range(self.params['num_products']):
                if q != p:
                    self.model += self.F + self.f[p] - self.f[q] - \
                        self.params['M'] * self.x[p][q] - self.setup_time[p][q] - \
                        self.f[p] - self.params['M'], 'AllProductionCompletionTimeConstraint{},{},'.format(p,q)

    def constraint3(self):
        for i in range(self.params['num_customers']):
            self.model += pulp.lpSum(self.y[i + 1, :, :].flatten()) == 1, \
                'MandatoryCustomerVisitConstraint{},'.format(i)

    def constraint4(self):
        for i in range(1, self.params['num_nodes'] - 1):
            for v in range(self.params['num_vehicles']):
                for h in range(self.params['num_trips']):
                    self.model += self.y[0,v,h)] - \
                        self.y[(i,v,h)] >= 0, \
                        'TourDefinitionConstraint1,{},{},{},'.format(i,v,h)

                    self.model += self.y[self.params['num_trips'] - 1,v,h)] - \
                        self.y[(i,v,h)] >= 0, \
                        'TourDefinitionConstraint2,{},{},{},'.format(i,v,h)

    def constraint5(self):
        for v in range(self.params['num_vehicles']):
            for h in range(self.params['num_trips'] - 1):
                self.model += self.params['M'] * pulp.lpSum(self.y[1:-1,v,h]) - \
                    pulp.lpSum(self.y[:,v,h+1]), 'SuceedingTourConstraint{},{},'.format(v,h)

    def constraint6(self):
        for v in range(self.params['num_vehicles']):
            for h in range(self.params['num_trips']):
                self.model += pulp.lpSum(pulp.lpSum(self.params['demand'] * \
                    np.repeat(np.expand_dims(self.y[:, v, h], 1), \
                        self.params['num_products'], 1))) <= \
                        self.params['vehicle_capacity'], 'VehicleCapacityConstraint{},{},'.format(
                            v,h
                        )

    def constraint7(self):
        for i in range(self.params['num_customers']):
            for j in range(self.params['num_customers']):
                for v in range(self.params['num_vehicles']):
                    for h in range(self.params['num_trips']):
                        if i != j:
                            self.model += self.z[0,i+1,v,h] + self.z[0,j+1,v,h] + \
                                self.y[i+1,v,h] + self.y[j+1,v,h] < 3, \
                                'StartEndRoutingConstraint{},{},{},{},'.format(i,j,v,h)

        for j in range(self.params['num_customers']):
            for v in range(self.params['num_vehicles']):
                for h in range(self.params['num_trips']):
                    self.model += self.y[j+1,v,h] - pulp.lpSum(
                        self.z[:-1,j+1,v,h]
                    ) == 0, 'MiddleRoutingConstraint1,{},{},{}'.format(j,v,h)
                    self.model += self.y[j+1,v,h] - pulp.lpSum(
                        self.z[1:,j+1,v,h]
                    ) == 0, 'MiddleRoutingConstraint{},{},{}'.format(j,v,h)

    def constraint8(self):
        for v in range(self.params['num_vehicles']):
            for h in range(self.params['num_trips']):
                self.model += self.u[(0,v,h)] - self.w[(v,)] >= 0, \
                    'VehicleTripAssignmentConstraint{},{}'.format(v,h)

    def constraint9(self):
        for v in range(self.params['num_vehicles']):
            for h in range(self.params['num_trips']):
                self.model += self.k[v][h] - self.F -\
                    self.params['service_time'][0] >= 0, \
                    'StartTimeConstraint1,{},{}'.format(v,h)

    def constraint10(self):
        for j in range(self.params['num_customers']):
            for v in range(self.params['num_vehicles']):
                for h in range(self.params['num_trips']):
                    self.model += self.k[v][h + 1] - self.a[j] - \
                        self.params['service_time'][j + 1] - \
                        self.params['travel_time'][j, self.params['num_nodes'] - 1] + \
                        self.paraas['M'] * (1 - self.y[j + 1,  v, h]) >= 0, \
                        'StartTimeConstraint2,{},{},{},'.format(j,v,h)

    def constraint11(self):
        for j in range(self.params['num_customers']):
            for v in range(self.params['num_vehicles']):
                for h in range(self.params['num_trips']):
                    self.model += self.a[j] - self.k[v][h] - \
                        self.params['travel_time'][0][j] + \
                        self.params['M'] * (1 - self.y[j + 1][v][h]) >= 0, \
                        'ArrivalTimeConstraint1,{},{},{}'.format(j,v,h)

    def constraint12(self):
        for i in range(self.params['num_customers']):
            for j in range(self.params['num_customers']):
                for v in range(self.params['num_vehicles']):
                    for h in range(self.params['num_trips']):
                        if i != j:
                            self.model += self.a[j] - self.a[i] - \
                                self.params['service_time'][i] - \
                                self.params['travel_time'][i+1][j+1] + \
                                self.params['M'] * (1 - self.y[i + 1][v][h]) >=0 , \
                                'ArrivalTimeConstraint1,{},{},{},{}'.format(i,j,v,h)

    def constraint13(self):
        for i in range(self.params['num_customers']):
            self.model += self.a[i] - self.params['time_window'][i + 1][0] >= 0, \
                'ArrivalTimeConstraint3,{}'.format(i)

    def constraint14(self):
        for i in range(self.params['num_customers']):
            self.model += self.l[i] - self.a[i] + \
                self.params['time_window'][i+1][1] >= 0, \
                'TardinessConstraint{},'.format(i)

    def solve(self):
        print('Solving Problem.')
        solver = self.params['pulp_solver']
        if solver == 'GUROBI':
            solver = pulp.GUROBI_CMD()
            self.model.solve(solver)
            print("Status:", pulp.LpStatus[self.model.status])
        else:
            self.model.solve(solver)
            print("Status:", pulp.LpStatus[self.model.status])

    def get_LP(self, filename):
        self.model.writeLP(filename)

    def get_solution(self, dir_path):
        solution = {
            v.name : v.varValue \
                for v in self.model.variables()
        }
        solution.update({
            'objective' : pulp.value(self.model.objective)
        })
        jsn = open(os.path.join(dir_path, 'solution.json'), 'w')
        json.dump(solution, jsn)
        jsn.close()
        return solution

    def get_solution_as_excel(self, dir_path):
        raise NotImplementedError
        solution = self.get_solution(dir_path)
        names = self.id.keys()
        sol = {}
        jsn = open(os.path.join(dir_path, 'ref.json'), 'w')
        json.dump(self.id, jsn)
        jsn.close()
        for name in names:
            out = []
            indices, index_names = self.id[name]
            workbook = xlsxwriter.Workbook(os.path.join(dir_path, name+'.xlsx'))
            shape = tuple([index + 1 for index in indices[-1]])
            lst = np.zeros(shape = shape)
            for index in indices:
                n = name + '_('
                for i, num in enumerate(index):
                    if i == 0 :
                        n += str(num) + ','
                    elif i == len(index) - 1:
                        n += '_' + str(num)
                    else:
                        n += '_' + str(num) + ','
                n += ')'
                try:
                    lst[index] = solution[n]
                except KeyError:
                    lst[index] = 0.0
            if len(shape) == 2:
                worksheet = workbook.add_worksheet()
                for index in indices:
                    worksheet.write(index[0], index[1], lst[index[0]][index[1]])
            elif len(shape) == 3:
                shape = lst.shape
                last = shape[-1]
                for i in range(last):
                    worksheet = workbook.add_worksheet(index_names[-1]+str(i+1))
                    for j in range(shape[0]):
                        for k in range(shape[1]):
                            worksheet.write(j, k, lst[j][k][i])

            elif len(shape) == 4:
                shape = lst.shape
                last = shape[-1]
                last2 = shape[-2]
                for i in range(last):
                    for j in range(last2):
                        worksheet = workbook.add_worksheet(
                            index_names[-1]+str(i+1)+ index_names[-2]+str(j+1)
                        )
                        for k in range(shape[0]):
                            for l in range(shape[1]):
                                worksheet.write(k, l, lst[k][l][j][i])
            else:
                shape = lst.shape
            workbook.close()
