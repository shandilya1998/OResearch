import pulp
import os
import numpy as np
from tqdm import tqdm
import pandas as pd
import os
import xlsxwriter
import json
import itertools

class PuLPModel:
    def __init__(self, params):
        self.params = params
        if os.path.exists('temp'):
            os.rmdir('temp')
        self.tmp_file_dir = 'temp'
        pulp.LpSolverDefault.tmpDir = self.tmp_file_dir
        self.model = pulp.LpProblem("Perishable Item Delivery Model", pulp.LpMinimize)

    def build(self):
        print('Building Variables.')
        self.indices = {}
        self.id = {}
        self.f = np.array(
            [pulp.LpVariable(
                'f{},'.format(p), lowBound = 0
            ) for p in range(self.params['num_products'])]
        )
        self.id['f'] = 'ProductProductionFinishTime'
        self.indices['f']  = (self.params['num_products'],)

        self.k = np.array([
            [
                pulp.LpVariable('k{},{}'.format(v,h), lowBound = 0) \
                    for h in range(self.params['num_trips'])
            ] for v in range(self.params['num_vehicles'])
        ])
        self.id['k'] = 'VehicleTripDeliveryStartTime'
        self.indices['k'] = (self.params['num_vehicles'], self.params['num_trips'])

        self.a = np.array([
            pulp.LpVariable('a{},'.format(i), lowBound = 0) \
                for i in range(self.params['num_customers'])
        ])
        self.id['a'] = 'ArrivalAtCustomerTime'
        self.indices['a'] = (self.params['num_customers'],)

        self.l = np.array([
            pulp.LpVariable('l{},'.format(i), lowBound = 0) \
                for i in range(self.params['num_customers'])
        ])
        self.id['l'] = 'TardinessAtCustomer'
        self.indices['l'] = (self.params['num_customers'],)

        self.x = np.array([
            [
                pulp.LpVariable('x{},{}'.format(p,q), cat = 'Binary') \
                    for q in range(self.params['num_products'])
            ] for p in range(self.params['num_products'] + 1)
        ])
        self.id['x'] = 'ProductProductionSequence'
        self.indices['x'] = (self.params['num_products'], self.params['num_products'])

        self.y = np.array([
            [
                [
                    pulp.LpVariable('y{},{},{}'.format(i,v,h), cat = 'Binary') \
                        for h in range(self.params['num_trips'])
                ] for v in range(self.params['num_vehicles'])
            ] for i in range(self.params['num_nodes'])
        ])
        self.id['y'] = 'CustomerVehicleTripMap'
        self.indices['y'] = (self.params['num_nodes'], self.params['num_vehicles'], self.params['num_trips'])

        self.z = np.array([
            [
                [
                    [
                        pulp.LpVariable('z{},{},{},{}'.format(i,j,v,h), cat = 'Binary') \
                            for h in range(self.params['num_trips'])
                    ] for v in range(self.params['num_vehicles'])
                ] for j in range(self.params['num_nodes'])
            ] for i in range(self.params['num_nodes'])
        ])
        self.id['z'] = 'DeliverySequence'
        self.indices['z'] = (self.params['num_nodes'], self.params['num_nodes'], self.params['num_vehicles'], self.params['num_trips'])

        self.w = np.array([
            pulp.LpVariable('w{},'.format(i), cat = 'Binary') \
                for i in range(self.params['num_vehicles'])
        ])
        self.id['w'] = 'VehicleUsage'
        self.indices['w'] = (self.params['num_vehicles'], )

        print('Building Objective.')
        self.mc_1 = pulp.LpAffineExpression(np.concatenate([
            np.array(list(zip(self.x.flatten(), self.params['setup_time'].flatten()))),
        ]))
        self.mc_2 = self.params['processing_cost'] * \
            np.sum(self.params['process_time'].flatten() * \
            np.sum(self.params['demand'], 0).flatten())

        self.dc = pulp.LpAffineExpression(np.concatenate([
            np.array(list(zip(self.w,
                [self.params['vehicle_cost']]*self.params['num_vehicles']))),
            np.array(list(zip(self.z.flatten(), np.repeat(
                np.expand_dims(
                    np.repeat(np.expand_dims(
                        self.params['travel_time'], -1
                    ), self.params['num_vehicles']), -1
                ), self.params['num_trips']
            ).flatten())))
        ], 0))

        self.pc = np.sum(self.l * self.params['late_delivery_penalty'])
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
        ]

        for constraint in tqdm(lst_constraints):
            constraint()

    def constraint1(self):
        for p in range(self.params['num_products']):
            self.model += pulp.lpSum([
                self.x[q][p] for q in range(self.params['num_products'] + 1) if p!=q
            ]) == 1, 'ProductionSeqConstraint1,{},'.format(p)
        for p in range(self.params['num_products']):
            self.model += pulp.lpSum([
                self.x[p][q] for q in range(self.params['num_products']) if q!= p
            ]) == 1, 'ProductionSeqConstraint2,{}'.format(p)

    def constraint2(self):
        for p in range(self.params['num_products']):
            self.model += self.f[p] - self.params['process_time'][p] * \
                pulp.lpSum(self.params['demand'][:, p]) == 0, \
                'ProductionFinisTimeConstraint{},'.format(p)

    def constraint3(self):
        for i in range(self.params['num_customers']):
            self.model += pulp.lpSum(self.y[i + 1, :, :].flatten()) == 1, \
                'MandatoryCustomerVisitConstraint{},'.format(i)

    def constraint4(self):
        for i in range(1, self.params['num_nodes'] - 1):
            for v in range(self.params['num_vehicles']):
                for h in range(self.params['num_trips']):
                    self.model += self.y[0,v,h] - \
                        self.y[i,v,h] >= 0, \
                        'TourDefinitionConstraint1,{},{},{},'.format(i,v,h)

                    self.model += self.y[self.params['num_nodes'] - 1,v,h] - \
                        self.y[i,v,h] >= 0, \
                        'TourDefinitionConstraint2,{},{},{},'.format(i,v,h)

    def constraint5(self):
        for v in range(self.params['num_vehicles']):
            for h in range(self.params['num_trips'] - 1):
                self.model += self.params['M'] * pulp.lpSum(self.y[1:-1,v,h]) - \
                    pulp.lpSum(self.y[1:-1,v,h+1]) >= 0, 'SuceedingTourConstraint{},{},'.format(v,h)

    def constraint6(self):
        for v in range(self.params['num_vehicles']):
            for h in range(self.params['num_trips']):
                self.model += pulp.lpSum(self.params['demand'] * \
                    np.repeat(np.expand_dims(self.y[:, v, h], 1), \
                        self.params['num_products'], 1)) <= \
                        self.params['vehicle_capacity'][v], 'VehicleCapacityConstraint{},{},'.format(
                            v,h
                        )

    def constraint7(self):
        for i in range(self.params['num_customers']):
            for j in range(self.params['num_customers']):
                for v in range(self.params['num_vehicles']):
                    for h in range(self.params['num_trips']):
                        if i != j:
                            self.model += self.z[0,i+1,v,h] + self.z[0,j+1,v,h] + \
                                self.y[i+1,v,h] + self.y[j+1,v,h] <= 3, \
                                'StartEndRoutingConstraint0_{},{},{},{},'.format(i,j,v,h)

                            self.model += self.z[i+1,self.params['num_nodes'] - 1,v,h] + self.z[j+1,self.params['num_nodes'] - 1,v,h] + \
                                self.y[i+1,v,h] + self.y[j+1,v,h] <= 3, \
                                'StartEndRoutingConstraint1_{},{},{},{},'.format(i,j,v,h)

        for j in range(self.params['num_customers']):
            for v in range(self.params['num_vehicles']):
                for h in range(self.params['num_trips']):
                    self.model += self.y[j+1,v,h] - pulp.lpSum(
                        np.array([self.z[i,j+1,v,h] for i in range(1, self.params['num_nodes']) if i!=j+1])
                    ) == 0, 'MiddleRoutingConstraint1,{},{},{}'.format(j,v,h)
                    self.model += self.y[j+1,v,h] - pulp.lpSum(
                        np.array([self.z[i,j+1,v,h] for i in range(self.params['num_nodes'] - 1) if i!=j+1])
                    ) == 0, 'MiddleRoutingConstraint{},{},{}'.format(j,v,h)

    def constraint8(self):
        for v in range(self.params['num_vehicles']):
            for h in range(self.params['num_trips']):
                self.model += self.y[0,v,h] - self.w[v] >= 0, \
                    'VehicleTripAssignmentConstraint{},{}'.format(v,h)

    def constraint9(self):
        for v in range(self.params['num_vehicles']):
            for h in range(self.params['num_trips']):
                self.model += self.k[v][h] - pulp.lpSum(self.f) -\
                    self.params['service_time'][0] >= 0, \
                    'StartTimeConstraint1,{},{}'.format(v,h)

    def constraint10(self):
        for j in range(self.params['num_customers']):
            for v in range(self.params['num_vehicles']):
                for h in range(self.params['num_trips'] - 1):
                    self.model += self.k[v][h + 1] - self.a[j] - \
                        self.params['service_time'][j + 1] - \
                        self.params['travel_time'][j + 1, self.params['num_nodes'] - 1] + \
                        self.params['M'] * (1 - self.y[j + 1, v, h]) >= 0, \
                        'StartTimeConstraint2,{},{},{},'.format(j,v,h)

    def constraint11(self):
        for j in range(self.params['num_customers']):
            for v in range(self.params['num_vehicles']):
                for h in range(self.params['num_trips']):
                    self.model += self.a[j] - self.k[v][h] - \
                        self.params['travel_time'][0][j + 1] + \
                        self.params['M'] * (1 - self.y[j + 1][v][h]) >= 0, \
                        'ArrivalTimeConstraint1,{},{},{}'.format(j,v,h)

    def constraint12(self):
        for i in range(self.params['num_customers']):
            for j in range(self.params['num_customers']):
                for v in range(self.params['num_vehicles']):
                    for h in range(self.params['num_trips']):
                        if i != j:
                            self.model += self.a[j] - self.a[i] - \
                                self.params['service_time'][i+1] - \
                                self.params['travel_time'][i+1][j+1] + \
                                self.params['M'] * (1 - self.z[i + 1][j + 1][v][h]) >=0 , \
                                'ArrivalTimeConstraint1,{},{},{},{}'.format(i,j,v,h)

    def constraint13(self):
        for i in range(self.params['num_customers']):
            self.model += self.a[i] - self.params['time_windows'][i + 1][0] >= 0, \
                'ArrivalTimeConstraint3,{}'.format(i)

    def constraint14(self):
        for i in range(self.params['num_customers']):
            self.model += self.l[i] - self.a[i] + \
                self.params['time_windows'][i+1][1] >= 0, \
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
        self.get_solution_as_excel(self.params['out_path'])

    def get_LP(self, filename):
        self.model.writeLP(filename)

    def _get_serializable_params(self):
        params = {}
        for key in self.params.keys():
            if isinstance(self.params[key], np.ndarray):
                params[key] = self.params[key].copy().tolist()
            elif isinstance(self.params[key], np.int64):
                params[key] = int(self.params[key])
            else:
                params[key] = self.params[key]
        return params

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
        jsn = open(os.path.join(dir_path, 'params.json'), 'w')
        json.dump(self._get_serializable_params(), jsn)
        jsn.close()
        return solution

    def _get_indices(self, limits):
        limits = [list(range(l)) for l in limits]
        return list(itertools.product(*limits))

    def get_solution_as_excel(self, dir_path):
        solution = self.get_solution(dir_path)
        jsn = open(os.path.join(dir_path, 'ref.json'), 'w')
        json.dump(self.id, jsn)
        jsn.close()
        for var, name in self.id.items():
            workbook = xlsxwriter.Workbook(os.path.join(dir_path, name+'.xlsx'))
            indices = self._get_indices(self.indices[var])
            shape = tuple([index + 1 for index in indices[-1]])
            lst = np.zeros(shape = shape)
            for index in indices:
                n = var
                for i, ax in enumerate(index):
                    if i < len(index) - 1:
                        n += str(ax) + ','
                    else:
                        n += str(ax)
                if len(index) == 1:
                    n = var + str(index[0]) + ','
                try:
                    lst[index] = solution[n]
                except KeyError:
                    lst[index] = 0.0
            if len(shape) == 0:
                worksheet = workbook.add_worksheet()
                worksheet.write(0, 0, lst)
            if len(shape) == 1:
                worksheet = workbook.add_worksheet()
                for index in indices:
                    worksheet.write(index[0], 0, lst[index[0]])
            if len(shape) == 2:
                worksheet = workbook.add_worksheet()
                for index in indices:
                    worksheet.write(index[0], index[1], lst[index[0]][index[1]])
            elif len(shape) == 3:
                shape = lst.shape
                last = shape[-1]
                for i in range(last):
                    worksheet = workbook.add_worksheet(var+str(i+1))
                    for j in range(shape[0]):
                        for k in range(shape[1]):
                            worksheet.write(j, k, lst[j][k][i])

            elif len(shape) == 4:
                shape = lst.shape
                print("SHAPE")
                print(shape)
                for i in range(shape[3]):
                    for j in range(shape[2]):
                        worksheet = workbook.add_worksheet(
                            var+str(j+1)+','+str(i+1)
                        )
                        for k in range(shape[1]):
                            for l in range(shape[0]):
                                worksheet.write(l, k, lst[l][k][j][i])
            else:
                shape = lst.shape
            workbook.close()
