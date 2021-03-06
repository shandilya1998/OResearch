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
        self.id = {}
        indices = [(f,) for f in range(self.params['num_batches'])]
        self.s = pulp.LpVariable.dicts(
            'ProductionStartTime',
            indices,
            lowBound = 0,
        )
        #self.id['ProductionStartTime'] = (indices, ('batch'))

        indices = [(f,) for f in range(self.params['num_batches'])]
        self.c = pulp.LpVariable.dicts(
            'ProductionCompletionTime',
            indices,
            lowBound = 0,
        )
        self.id['ProductionCompletionTime'] = (indices, ('batch'))

        indices = []
        for v in range(self.params['num_vehicles']):
            for h in range(self.params['num_trips']):
                indices.append((v,h))
        self.st = pulp.LpVariable.dicts(
            'DeliveryStartTime',
            indices,
            lowBound = 0,
        )
        self.id['DeliveryStartTime'] = (indices, ('vehicle', 'trips'))

        indices = []
        for j in range(self.params['num_nodes']):
            for v in range(self.params['num_vehicles']):
                for h in range(self.params['num_trips']):
                    indices.append((j,v,h))
        self.a = pulp.LpVariable.dicts(
            'ArrivalTime',
            indices,
            lowBound = 0,
        )
        self.id['ArrivalTime'] = (indices ,('customer', 'vehicle', 'trip'))

        self.e = pulp.LpVariable.dicts(
            'EarlyArrivalTime',
            indices,
            lowBound = 0,
        )
        self.id['EarlyArrivalTime'] = (indices, ('customer', 'vehicle', 'trip'))
        self.l = pulp.LpVariable.dicts(
            'LateArrivalTime',
            indices,
            lowBound = 0,
        )
        self.id['LateArrivalTime'] = (indices, ('customer', 'vehicle', 'trip'))

        indices = []
        for p in range(self.params['num_products']):
            for q in range(self.params['num_products']):
                indices.append((p,q))
        self.x = pulp.LpVariable.dicts(
            'ProductSequence',
            indices,
            lowBound = 0,
            upBound = 1,
            cat = pulp.LpInteger
        )
        self.id['ProductSequence'] = (indices, ('product', 'product'))

        indices = []
        for j in range(self.params['num_customers']):
            for f in range(self.params['num_batches']):
                indices.append((j,f))
        self.b = pulp.LpVariable.dicts(
            'BatchCustomerMapping',
            indices,
            lowBound = 0,
            upBound = 1,
            cat = pulp.LpInteger
        )
        self.id['BatchCustomerMapping'] = (indices, ('customer', 'batch'))

        indices = indices = [(f,) for f in range(self.params['num_batches'])]
        self.d = pulp.LpVariable.dicts(
            'ActiveBatchMap',
            indices,
            lowBound = 0,
            upBound = 1,
            cat = pulp.LpInteger
        )
        self.id['ActiveBatchMap'] = (indices, ('batch'))

        indices = []
        for f in range(self.params['num_batches']):
            for f_ in range(self.params['num_batches']):
                indices.append((f, f_))
        self.g = pulp.LpVariable.dicts(
            'BatchSequence',
            indices,
            lowBound = 0,
            upBound = 1,
            cat = pulp.LpInteger
        )
        self.id['BatchSequence'] = (indices, ('batch', 'batch'))

        indices = []
        for f in range(self.params['num_batches']):
            for v in range(self.params['num_vehicles']):
                for h in range(self.params['num_trips']):
                    indices.append((f,v,h))
        self.t = pulp.LpVariable.dicts(
            'BatchVehicleTripMapping',
            indices,
            lowBound = 0,
            upBound = 1,
            cat = pulp.LpInteger
        )
        self.id['BatchVehicleTripMapping'] = (indices, ('batch', 'vehicle', 'trip'))

        indices = []
        for j in range(self.params['num_nodes']):
            for v in range(self.params['num_vehicles']):
                for h in range(self.params['num_trips']):
                    indices.append((j,v,h))
        self.u = pulp.LpVariable.dicts(
            'CustomerVehicleTripMapping',
            indices,
            lowBound = 0,
            upBound = 1,
            cat = pulp.LpInteger
        )
        self.id['CustomerVehicleTripMapping'] = (indices, ('customer', 'vehicle', 'trip'))

        indices = []
        for i in range(self.params['num_nodes']):
            for j in range(self.params['num_nodes']):
                for v in range(self.params['num_vehicles']):
                    for h in range(self.params['num_trips']):
                        indices.append((i, j, v, h))
        self.y = pulp.LpVariable.dicts(
            'CustomerVehicleTripSequence',
            indices,
            lowBound = 0,
            upBound = 1,
            cat = pulp.LpInteger
        )
        self.id['CustomerVehicleTripSequence'] = (indices, ('customer', 'customer', 'vehicle', 'trip'))

        indices = [(v,) for v in range(self.params['num_vehicles'])]
        self.w = pulp.LpVariable.dicts(
            'ActiveVehicleMapping',
            indices,
            lowBound = 0,
            upBound = 1,
            cat = pulp.LpInteger
        )
        self.id['ActiveVehicleMapping'] = (indices, ('vehicle'))

        print('Building Model.')
        self.model = pulp.LpProblem("IntegratedProductionDeliveryModel", 
                pulp.LpMinimize)

        print('Building Objective.')
        indices_x = []
        for p in range(self.params['num_products']):
            for q in range(self.params['num_products']):
                indices_x.append((p,q))
        indices_y = []
        for i in range(1, self.params['num_nodes'] - 1):
            for j in range(1, self.params['num_nodes'] - 1):
                for v in range(self.params['num_vehicles']):
                    for h in range(self.params['num_trips']):
                        indices_y.append((i,j,v,h))
        indices_t = []
        for j in range(1, self.params['num_nodes'] - 1):
            for v in range(self.params['num_vehicles']):
                for h in range(self.params['num_trips']):
                    indices_t.append((j,v,h))
        self.model += pulp.lpSum([
            self.params['setup_cost'] * \
                self.params['setup_time'][p][q] * self.x[(p,q)] \
                for p, q in indices_x if p != q
        ] + [
            self.params['travel_cost'] * \
                self.params['travel_time'][i][j] * self.y[(i, j, v, h)] \
                for i, j, v, h in indices_y
        ] + [
            self.params['vehicle_cost'][v] * self.w[(v,)] \
                for v in range(self.params['num_vehicles'])
        ] + [
            self.params['early_delivery_penalty'] * \
                self.e[(j, v, h)] for j, v, h in indices_t
        ] + [
            self.params['late_delivery_penalty'] * \
                self.l[(j, v, h)] for j, v, h in indices_t
        ]), "MinimizationObjective"

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
        for j in range(1, self.params['num_nodes'] - 1):
            self.model += pulp.lpSum([
                self.u[(j, v, h)] \
                for v in range(self.params['num_vehicles']) \
                for h in range(self.params['num_trips'])
            ]) == 1, 'SingleVistContraint({j},)'.format(j=j)

    def constraint2(self):
        for j in range(1, self.params['num_nodes'] - 1):
            for v in range(self.params['num_vehicles']):
                for h in range(self.params['num_trips']):
                    self.model += self.u[(0, v, h)] - self.u[(j,v,h)] >= 0, \
                        'ActiveTourOriginConstraint1({j},{v},{h})'.format(
                            j = j,
                            v = v,
                            h = h
                        )

                    self.model += self.u[(self.params[
                            'num_nodes'
                        ] - 1, v, h)] - self.u[(j,v,h)] >= 0, \
                        'ActiveTourOriginConstraint2({j},{v},{h})'.format(
                            j = j,
                            v = v,
                            h = h
                        )

    def constraint3(self):
        for v in range(self.params['num_vehicles']):
            for h in range(self.params['num_trips']):
                self.model += pulp.lpSum([
                    self.params['demand'][j][p] * \
                    self.u[(j,v,h)] \
                    for p in range(self.params['num_products']) \
                    for j in range(
                        1,
                        self.params['num_nodes'] - 1
                    )
                ]) <= self.params['vehicle_capacity'][v], \
                    'TotalVehicleCapacityConstraint({v},{h})'.format(
                        v=v,
                        h=h
                    )

    def constraint4(self):
        for i in range(1, self.params['num_nodes'] - 1):
            for j in range(1, self.params['num_nodes'] - 1):
                for v in range(self.params['num_vehicles']):
                    for h in range(self.params['num_trips']):
                        if i == j:
                            continue
                        self.model += self.y[(0,i,v,h)] + \
                            self.y[(0,j,v,h)] + \
                            self.u[(i,v,h)] + \
                            self.u[(j,v,h)] <= 3, \
                            'TripStartConstraint({i},{j},{v},{h})'.format(
                                i=i,
                                j=j,
                                v=v,
                                h=h,
                            )

                        self.model+=self.y[(i,self.params['num_nodes']-1,v,h)]+\
                            self.y[(j,self.params['num_nodes']-1,v,h)] + \
                            self.u[(i,v,h)] + \
                            self.u[(j,v,h)] <= 3, \
                            'TripEndConstraint({i},{j},{v},{h})'.format(
                                i=i,
                                j=j,
                                v=v,
                                h=h,
                            )

    def constraint5(self):
        for j in range(1, self.params['num_nodes'] - 1):
            for v in range(self.params['num_vehciles']):
                for h in range(self.params['num_trips']):
                    self.model += self.u[(j,v,h)] - pulp.lpSum([
                        self.y[(i,j,v,h)] for i in range(
                            self.params['num_customers'] + 1
                        ) if i != j
                    ]) == 0, \
                        'TripMiddleContraint1({j},)'.format(
                            j=j,
                        )

                    self.model += self.u[(j,v,h)] - pulp.lpSum([
                        self.y[(i,j,v,h)] for i in range(
                            1, self.params['num_nodes']
                        ) if i != j
                    ]) == 0, \
                        'TripMiddleContraint2({j},)'.format(
                            j=j,
                        )

    def constraint6(self):
        for i in range(1, self.params['num_nodes'] - 1):
            for j in range(1, self.params['num_nodes'] - 1):
                for v in range(self.params['num_vehicles']):
                    for h in range(self.params['num_trips']):
                        self.model += self.u[(i,v,h)] - self.y[(i,j,v,h)] - \
                            self.u[(j,v,h)] >= -1, \
                            'TripMiddleConstraint3({i},{j},{v},{h})'.format(
                                i=i,
                                j=j,
                                v=v,
                                h=h
                                )

                        self.model += self.u[(j,v,h)] - self.y[(i,j,v,h)] - \
                            self.u[(i,v,h)] >= -1, \
                            'TripMiddleConstraint4({i},{j},{v},{h})'.format(
                                i=i,
                                j=j,
                                v=v,
                                h=h
                            )
    def constraint7(self):
        for v in range(self.params['num_vehicles']):
            for h in range(self.params['num_trips'] - 1):
                self.model += pulp.lpSum([
                    self.params['M']*self.u[(j,v,h)] \
                    for j in range(1, self.params['num_nodes'] - 1)
                ]) - pulp.lpSum([
                    self.u[(j,v,h + 1)] \
                    for j in range(1, self.params['num_nodes'] - 1)
                ]) >= 0, \
                    'VehicleTripActivationConstraint({v},{h})'.format(
                        v = v,
                        h = h
                    )

    def constraint8(self):
        for v in range(self.params['num_vehicles']):
            for h in range(self.params['num_trips']):
                self.model += self.u[(0,v,h)] - self.w[(v,)] >= 0, \
                    'VehicleTripAssignmentConstraint({v},{h})'.format(
                        v = v,
                        h = h
                    )

    def constraint9(self):
        for p in range(self.params['num_products']):
            for q in range(self.params['num_products']):
                self.model += self.x[(p,q)] + self.x[(q,p)] <= 1, \
                    'ProductSchedulingConstraint1({p},{q})'.format(
                        p = p,
                        q = q
                    )

    def constraint10(self):
        for p in range(self.params['num_products']):
            self.model += pulp.lpSum([
                self.x[(p, q)] \
                    for q in range(self.params['num_products']) \
                    if p!=q
            ]) == 1, \
                'ProductSchedulingConstraint1({p},)'.format(
                    p = p,
                )

            self.model += pulp.lpSum([
                self.x[(q,p)] \
                    for q in range(self.params['num_products']) \
                    if p!=q
            ]) == 1, \
                'ProductSchedulingConstraint2({p},)'.format(
                    p = p,
                )

    def constraint11(self):
        self.model += pulp.lpSum([
            self.u[(0,v,h)] \
                for v in range(self.params['num_vehicles']) \
                for h in range(self.params['num_trips'])
        ]) - pulp.lpSum([
            self.d[(f,)] \
                for f in range(self.params['num_batches'])
        ]) == 0, \
            'ActiveTripsProductionBatchesConstraint1'

    def constraint12(self):
        self.model += self.d[(0),] == 1, 'FirstBatchActiveConstraint'

        for f in range(self.params['num_batches']-2):
            self.model += self.d[(f,)] - self.d[(f+1,)] >= 0, \
                'ActiveTripsProductionBatchesConstraint2({f},)'.format(
                    f=f
                )

    def constraint13(self):
        """
            Abnormal Behaviour observed after the addition of this constraint
            Optimal Solution is obtained, but the problem begins to
                take more time to solve
        """
        for v in range(self.params['num_vehicles']):
            for h in range(self.params['num_trips']):
                self.model += pulp.lpSum([
                    self.t[(f,v,h)] \
                        for f in range(self.params['num_batches'])
                ]) - self.u[(0,v,h)] == 0, \
                    'ActiveTripsProductionBatchMappingConstraint3\
                        ({v},{h})'.format(v=v,h=h)

    def constraint14(self):
        """
            Solving time exploded after addition of 14
        """
        for f in range(self.params['num_batches']):
            self.model += self.d[(f,)] - pulp.lpSum([
                self.t[(f,v,h)] \
                    for v in range(self.params['num_vehicles']) \
                    for h in range(self.params['num_trips'])
            ]) == 0, \
                'ActiveTripsProductionBatchMappingConstraint4\
                        ({f},)'.format(f=f)

    def constraint15(self):
        for j in range(self.params['num_customers']):
            self.model += pulp.lpSum([
                self.b[(j,f)] \
                    for f in range(self.params['num_batches'])
            ]) == 1, \
                'CustomerProductionBatchMappingConstraint({j},)'.format(
                    j=j,
                )

    def constraint16(self):
        for f in range(self.params['num_batches']):
            for j in range(1, self.params['num_nodes'] - 1):
                for v in range(self.params['num_vehicles']):
                    for h in range(self.params['num_trips']):
                        self.model += self.b[(j - 1,f)] - \
                            self.u[(j,v,h)] - \
                            self.t[(f,v,h)] >= -1, \
                            'CustomerBatchTripMappingConstraint\
                            ({j},{f},{v},{h})'.format(j=j,f=f,v=v,h=h)

    def constraint17(self):
        for f in range(self.params['num_batches']):
            for j in range(1, self.params['num_nodes'] - 1):
                for v in range(self.params['num_vehicles']):
                    for h in range(self.params['num_trips']):
                        self.model += self.t[(f,v,h)] - self.b[(j - 1,f)] - \
                            self.u[(j,v,h)] >= -1, \
                            'BatchCustomerTripMappingConstraint\
                            ({j},{f},{v},{h})'.format(j=j,f=f,v=v,h=h)

    def constraint18(self):
        """
            This conflicts with one of the constraints between 1 to 17
        """
        for f in range(self.params['num_batches']):
            """
            self.model += pulp.lpSum([
                self.g[(f_, f)] \
                    for f_ in range(self.params['num_batches']) \
                    if f_!= f
            ]) - self.d[(f,)] == 0, \
                'BatchProductionSequenceConstraint1({f},)'.format(f=f)
            self.model += pulp.lpSum([
                self.g[(f, f_)] \
                    for f_ in range(self.params['num_batches']) \
                    if f_!= f
            ]) - self.d[(f,)] == 0, \
                 'BatchProductionSequenceConstraint2({f},)'.format(f=f)
            for f_ in range(self.params['num_batches']):
                self.model += self.g[(f,f_)] + self.g[(f,f_)] <= 1, \
                    'BatchProductionSequenceConstraint3({f},{f_})'.format(
                        f=f, f_=f_
                    )
            """
            self.model += pulp.lpSum([
                self.params['setup_time'][p][q] * self.x[(p,q)] \
                    for p in range(self.params['num_products']) \
                    for q in range(self.params['num_products']) \
                    if p!=q
                ]) + pulp.lpSum([
                    self.params['process_time'][q] * \
                        self.params['demand'][j][q] * \
                        self.b[(j - 1,f)] \
                        for j in range(
                            1,
                            self.params['num_nodes'] - 1
                        ) for q in range(self.params['num_products'])
                ]) - self.params['M'] * (1 - self.g[(0,f)]) - self.c[(f,)]<=0,\
                    'BatchProductionSequenceConstraint3({f},)'.format(
                        f=f
                    )

            for f_ in range(self.params['num_batches']):
                if f != f_:
                    self.model += pulp.lpSum([
                        self.params['setup_time'][p][q] * self.x[(p,q)] \
                            for p in range(self.params['num_products']) \
                            for q in range(self.params['num_products']) \
                            if p!=q
                        ]) + pulp.lpSum([
                            self.params['process_time'][q] * \
                                self.params['demand'][j][q] * \
                                self.b[(j - 1,f_)] \
                                for j in range(
                                    1,
                                    self.params['num_nodes'] - 1
                                ) for q in range(self.params['num_products'])
                        ]) - self.params['M'] * (1 - self.g[(f,f_)]) + \
                            self.c[(f,)] - self.c[(f_,)] <= 0, \
                                'BatchProductionSequenceConstraint3\
                                    ({f},{f_})'.format(
                                        f=f, f_=f_
                                    )

    def constraint19(self):
        for j in range(1, self.params['num_nodes']):
            for v in range(self.params['num_vehicles']):
                for h in range(self.params['num_trips']):
                    for i in range(self.params['num_nodes'] - 1):
                        self.model += self.a[(j,v,h)] - self.a[(i,v,h)] - \
                            self.params['service_time'][i] - \
                            self.params['travel_time'][i][j] + \
                            self.params['M'] * (1 - self.y[(i,j,v,h)])>=0, \
                                'ArrivalTimeConstraint1\
                                ({j},{v},{h},{i})'.format(j=j,v=v,h=h,i=i)

                        self.model += self.a[(j,v,h)] - self.st[(v,h)] - \
                            self.params['service_time'][0] - \
                            self.params['travel_time'][0][j] + \
                            self.params['M'] * (
                                2 - \
                                self.u[(j,v,h)] - \
                                self.y[(i,j,v,h)]
                            ) >= 0, \
                                'ArrivalTimeConstraint2\
                                ({j},{v},{h},{i})'.format(j=j,v=v,h=h,i=i)

    def constraint20(self):
        for v in range(self.params['num_vehicles']):
            for f in range(self.params['num_batches']):
                for h in range(self.params['num_trips']):
                    self.model += self.st[(v,h)] - self.c[(f,)] - \
                        self.params['service_time'][0] + \
                        self.params['M'] * (1 - self.t[(f,v, h)]) >= 0, \
                            'StartTimeConstraint1({v},{f},{h})'.format(
                                v=v, f=f, h=h
                            )

    def constraint21(self):
        for f in range(self.params['num_batches']):
            for v in range(self.params['num_vehicles']):
                for h in range(self.params['num_trips'] - 1):
                    self.model += self.st[(v,h+1)] - self.a[
                        (self.params['num_nodes'] - 1,v,h)
                    ] - self.params['service_time'][
                        self.params['num_nodes'] - 1
                    ] + self.params['M'] * (
                        1 - self.u[(0,v,h)]
                    ) >= 0, \
                        'StartTimeConstraint2({v},{f},{h})'.format(
                            v=v, f=f, h=h
                        )

    def constraint22(self):
        for j in range(1, self.params['num_nodes'] - 1):
            for v in range(self.params['num_vehicles']):
                for h in range(self.params['num_trips']):
                    self.model += self.e[(j,v,h)] + self.a[(j,v,h)] >= \
                        self.params['time_windows'][j][0], \
                            'TimeWindowConstraint1({j},{v},{h})'.format(
                                j=j,v=v,h=h
                            )

                    self.model += self.l[(j,v,h)] - self.a[(j,v,h)] + \
                        self.params[
                            'time_windows'
                        ][j][1] >= 0, \
                            'TimeWindowConstraint2({j},{v},{h})'.format(
                                j=j,v=v,h=h
                            )

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
