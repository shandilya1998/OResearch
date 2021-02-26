import pulp

class PuLPModel:
    def __init__(self, params):
        self.params = params

    def build(self):
        print('Building Variables.')
        indices = [(f,) for f in range(self.params['num_batches'])]
        self.s = pulp.LpVariable.dicts(
            'ProductionStartTime',
            indices,
            lowBound = 0,
        )

        indices = [(f,) for f in range(self.params['num_batches'])]
        self.c = pulp.LpVariable.dicts(
            'ProductionCompletionTime',
            indices,
            lowBound = 0,
        )

        indices = []
        for v in range(self.params['num_vehicles']):
            for h in range(self.params['num_trips']):
                indices.append((v,h))
        self.st = pulp.LpVariable.dicts(
            'DeliveryStartTime',
            indices,
            lowBound = 0,
        )

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
        self.e = pulp.LpVariable.dicts(
            'EarlyArrivalTime',
            indices,
            lowBound = 0,
        )
        self.l = pulp.LpVariable.dicts(
            'LateArrivalTime',
            indices,
            lowBound = 0,
        )

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

        indices = []
        for j in range(self.params['num_customers'])
            for f in range(self.params['num_batches']):
                indices.append((j,f))
        self.b = pulp.LpVariable.dicts(
            'BatchCustomerMapping',
            indices,
            lowBound = 0,
            upBound = 1,
            cat = pulp.LpInteger
        )

        indices = indices = [(f,) for f in range(self.params['num_batches'])]
        self.d = pulp.LpVariable.dicts(
            'ActiveBatchMap',
            indices,
            lowBound = 0,
            upBound = 1,
            cat = pulp.LpInteger
        )

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

        indices = []
        for j in range(self.params['num_nodes']):
            for v in range(self.params['num_vehicles']):
                for h in range(self.params['num_trips']):
                    indices.append((f,v,h))
        self.u = pulp.LpVariable.dicts(
            'CustomerVehicleTripMapping',
            indices,
            lowBound = 0,
            upBound = 1,
            cat = pulp.LpInteger
        )

        indices = []
        for i in range(self.params['num_nodes']):
            for j in range(self.params['num_nodes']):
                for v in range(self.params['num_vehicles']):
                    for h in range(self.params['num_trips']):
                        indices.append((i,j,v,h))
        self.y = pulp.LpVariable.dicts(
            'CustomerVehicleTripSequence',
            indices,
            lowBound = 0,
            upBound = 1,
            cat = pulp.LpInteger
        )

        indices = [(v,) for v in range(self.params['num_vehicles'])]
        self.w = pulp.LpVariable.dicts(
            'ActiveVehicleMapping',
            indices,
            lowBound = 0,
            upBound = 1,
            cat = pulp.LpInteger
        )

        print('Building Model.')
        self.model = pulp.LpProblem("Integrated Production Delivery Model", 
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
                        indices_y.appnd((i,j,v,h))
        indices_t = []
        for j in range(1, self.params['num_nodes'] - 1):
            for v in range(self.params['num_vehicles']):
                for h in range(self.params['num_trips']):
                    indices_t.append((j,v,h))
        self.model += pulp.lpSum([
            self.params['processing_cost'] * np.sum(
                self.params['process_time'] * self.params['demand']
            )
        ] + [
            self.params['setup_cost'] * \
                self.params['setup_time'][p][q] * self.x[(p,q)] \
                for p, q in indices_x
        ] + [
            self.params['travel_cost'] * \
                self.params['travel_time'][i][j] * self.y[(i, j, v, h)] \
                for i, j, v, h in indices_y
        ] + [
            self.params['vehicle_cost'][v] * self.x[(v,)] \
                for v in range(self.params['num_vehicles'])
        ] + [
            self.params['early_delivery_penalty'] * \
                self.e[(j, v, h)] for j, v, h in indices_t
        ] + [
            self.params['late_delivery_penalty'] * \
                self.l[(j, v, h)] for j, v, h in indices_t
        ]), "minimization objective"

        print('Building Constraint.')
        for j in range(1, self.params['num_nodes'] - 1):
            self.model += pulp.lpSum([
                self.u[(j, v, h)] \
                for v in range(self.params['num_vehicles']) \
                for h in range(self.params['num_trips'])
            ]) == 1. 'Single Vist Contraint {j}'.format(j=j)

        for j in range(1, self.params['num_nodes'] - 1):
            for v in range(self.params['num_vehicles']):
                for h in range(self.params['num_trips']):
                    self.model += self.u[(0, v, h)] - self.u[(j,v,h)] >= 0, \
                        'Active Tour Origin Constraint {(j},{v},{h})'.format(
                            j = j,
                            v = v,
                            h = h
                        )

                    self.model += self.u[(self.params[
                            'num_nodes'
                        ] - 1, v, h)] - self.u[(j,v,h)] >= 0, \
                        'Active Tour Origin Constraint {(j},{v},{h})'.format(
                            j = j,
                            v = v,
                            h = h
                        )

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
                    'Total Vehicle Capacity Constraint ({j},{v},{h})'.format(
                        j=j,
                        v=v,
                        h=h
                    )

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
                            'Trip Start Constraint ({i},{j},{v},{h})'.format(
                                i=i,
                                j=j,
                                v=v,
                                h=h,
                            )

                        self.model+=self.y[(i,self.params['num_nodes']-1,v,h)]+\
                            self.y[(j,self.params['num_nodes']-1,v,h)] + \
                            self.u[(i,v,h)] + \
                            self.u[(j,v,h)] <= 3, \
                            'Trip End Constraint ({i},{j},{v},{h})'.format(
                                i=i,
                                j=j,
                                v=v,
                                h=h,
                            )

        for j in range(1, self.params['num_nodes'] - 1):
            for v in range(self.params['num_vehicles']):
                for h in range(self.params['num_trips']):
                    self.model += self.u[(j,v,h)] - pulp.lpSum([
                        self.y[(i,j,v,h)] for i in range(
                            self.params['num_customers'] + 1
                        )
                    ]) + self.y[j][j][v][h]  == 0, \
                        'Trip Middle Contraint 1 ({j},{v},{h})'.format(
                            j=j,
                            v=v,
                            h=h
                        )

                    self.model += self.u[(j,v,h)] - pulp.lpSum([
                        self.y[(i,j,v,h)] for i in range(
                            1, self.params['num_nodes']
                        )
                    ]) + self.y[j][j][v][h]  == 0, \
                        'Trip Middle Contraint 2 ({j},{v},{h})'.format(
                            j=j,
                            v=v,
                            h=h
                        )

        for i in range(1, self.params['num_nodes'] - 1):
            for j in range(1, self.params['num_nodes'] - 1):
                for v in range(self.params['num_vehicles']):
                    for h in range(self.params['num_trips']):
                        self.model += self.u[(i,v,h)] - self.y[(i,j,v,h)] - \
                            self.u[(j,v,h)] >= -1, \
                            'Trip Middle Constraint 3 ({i},{j},{v},{h})'.format(
                                i=i,
                                j=j,
                                v=v,
                                h=h
                                )

                        self.model += self.u[(j,v,h)] - self.y[(i,j,v,h)] - \
                            self.u[(i,v,h)] >= -1, \
                            'Trip Middle Constraint 4 ({i},{j},{v},{h})'.format(
                                i=i,
                                j=j,
                                v=v,
                                h=h
                            )

        for v in range(self.params['num_vehicles']):
            for h in range(self.params['num_trips'] - 1):
                self.model += pulp.lpSum([
                    self.params['M']*self.u[(j,v,h)] \
                    for j in range(1, self.params['num_nodes'] - 1)
                ]) - pulp.lpSum([
                    self.u[(j,v,h + 1)] \
                    for j in range(1, self.params['num_nodes'] - 1)
                ]) >= 0, \
                    'Vehicle Trip Activation Constrant ({v},{h})'.format(
                        v = v,
                        h = h
                    )

        for v in range(self.params['num_vehicles']):
            for h in range(self.params['num_trips']):
                self.model += self.u[(0,v,h)] - self.w[(v,)] >= 0, \
                    'Vehicle Trip Assignment Constraint ({v},{h})'.format(
                        v = v,
                        h = h
                    )

        for p in range(self.params['num_products']):
            for q in range(self.params['num_products']):
                self.model += self.x[(p,q)] + self.x[(q,p)] <= 1, \
                    'Product Scheduling Constraint 1 ({p},{q})'.format(
                        p = p,
                        q = q
                    )

        for p in range(self.params['num_products']):
            self.model += pulp.lpSum([
                self.x[(p, q)] \
                    for q in range(self.params['num_products'])
            ]) - self.x[p][p] == 1, \
                'Product Scheduling Constraint 1 ({p},)'.format(
                    p = p,
                )

            self.model += pulp.lpSum([
                self.x[(q,p)] \
                    for q in range(self.params['num_prodcuts'])
            ]) - self.x[p][p] == 1, \
                'Product Scheduling Constraint 1 ({p},)'.format(
                    p = p,
                )

        self.model += pulp.lpSum([
            self.u[(0,v,h)] \
                for v in range(self.params['num_vehicles']) \
                for h in range(self.params['num_trips'])
        ]) - pulp.lpSum([
            self.d[(f,)] \
                for f in range(self.params['num_batches'])
        ]) == 0, \
            'Active Trips Production Batches Constraint 1'

        self.model += self.d[(0),] == 1, 'First Batch Active Constraint'

        for f in range(self.params['num_batches']-2):
            self.model += self.d[(f,)] - self.d[(f+1,)] >= 0, \
                'Active Trips Production Batches Constraint 2 ({f,})'.format(
                    f=f
                )

        for v in range(self.params['num_vehicles']):
            for h in range(self.params['num_trips']):
                self.model += pulp.lpSum([
                    self.t[(f,v,h)] \
                        for f in range(self.params['num_batches'])
                ]) == self.u[(0,v,h)], \
                    'Active Trips Production Batch Mapping Constraint 3 \
                        ({v},{h})'.format(f=f,v=v,h=h)

        for f in range(self.params['num_batches']):
            self.model += self.d[f] - pulp.lpSum([
                self.t[(f,v,h)] \
                    for v in range(self.params['num_vehicles']) \
                    for h in range(self.params['num_trips'])
            ]) == 0, \
                'Active Trips Production Batch Mapping Constraint 4 \
                        ({f},)'.format(f=f)

        for j in range(self.params['num_customers']):
            self.model += pulp.lpSum([
                self.b[(j,f)] \
                    for f in range(self.params['num_batches'])
            ]) == 1,
                'Customer Production Batch Mapping Constraint ({j},{f})'.format(
                    j=j
                )

        for f in range(self.params['num_batches']):
            for j in range(1, self.params['num_nodes'] - 1):
                for v in range(self.params['num_vehicles']):
                    for h in range(self.params['num_trips']):
                        self.model += self.b[(j - 1,f)] - \
                            self.u[(j,v,h)] - \
                            self.t[(f,v,h)] >= -1, \
                            'Customer Batch Trip Mapping Constraint \
                            ({j},{f},{v},{h})'.format(j=j,f=f,v=v,h=h)

        for f in range(self.params['num_batches']):
            for j in range(1, self.params['num_nodes'] - 1):
                for v in range(self.params['num_vehicles']):
                    for h in range(self.params['num_trips']):
                        self.model += self.t[(f,v,h)] - self.b[(j - 1,f)] - \
                            self.u[(j,v,h)] >= -1, \
                            'Batch Customer Trip Mapping Constraint \
                            ({j},{f},{v},{h})'.format(j=j,f=f,v=v,h=h)

        for f in range(self.params['num_batches']):
            self.model += pulp.lpSum([
                self.g[(f_, f) \
                    for f_ in range(self.params['num_batches']) \
                    if f_!= f
            ]) - self.d[(f,)] == 0, \
                'Batch Production Sequence Constraint 1 ({f},)'.format(f=f)

            self.model += pulp.lpSum([
                self.g[(f, f_)] \
                    for f_ in range(self.params['num_batches']) \
                    if f_!= f
            ]) - self.d[(f,)] == 0, \
                'Batch Production Sequence Constraint 2 ({f},)'.format(f=f)

            for f_ in range(self.params['num_batches']):
                self.model += self.g[(f,f_)] + self.g[(f,f_)] <= 1,
                    'Batch Production Sequence Constraint 3 ({f},{f_})'.format(
                        f=f, f_=f_
                    )

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
                ]) - self.params['M'] * (1 - self.g[(0,f)]) - self.c[(f,)] <= 0

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
                            self.c[(f,)] - self.c[(f_,)] <= 0

        for j in range(1, self.params['num_nodes']):
            for v in range(self.params['num_vehicles']):
                for h in range(self.params['num_trips']):
                    for i in range(self.params['num_nodes'] - 1):
                        self.model += self.a[(j,v,h)] - self.a[(i,v,h)] - \
                                self.params['service_time'][i] - \
                                self.params['travel_time'][i][j] + \
                                self.params['M'] * (1 - self.y[(i,j,v,h)])>=0, \
                                    'Arrival Time Constraint 1 \
                                    ({j},{v},{h},{i})'.format(j=j,v=v,h=h,i=i)

                        self.model += self.a[(j,v,h)] - self.st[(v,h)] - \
                                self.params['service_time'][0] - \
                                self.params['travel_time'][0][j] + \
                                self.params['M'] * (
                                    2 - \
                                    self.u[(j,v,h)] - \
                                    self.y[(i,j,v,h)]
                                ) >= 0, \
                                    'Arrival Time Constraint 2 \
                                    ({j},{v},{h},{i})'.format(j=j,v=v,h=h,i=i)

        for v in range(self.params['num_vehicles']):
            for f in range(self.params['num_batches']):
                for h in range(self.params['num_trips']):
                    self.model += self.st[(v,h)] - self.c[(f,)] - \
                        self.params['service_time'][0] + \
                        self.params['M'] * (1 - self.t[(f,v, h)]) >= 0, \
                            'Start Time Constraint 1 ({v},{f},{h})'.format(
                                v=v, f=f, h=h
                            )

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
                        'Start Time Consttraint 2 ({v},{f},{h})'.format(
                            v=v, f=f, h=h
                        )

        for j in range(1, self.params['num_nodes'] - 1):
            for v in range(self.params['num_vehicles']):
                for h in range(self.params['num_trips']):
                    self.model += self.e[(j,v,h)] + self.a[(j,v,h)] >= \
                        self.params['time_windows'][j][0], \
                            'Time Window Constraint 1 ({j},{v},{h})'.format(
                                j=j,v=v,h=h
                            )

                    self.model += self.l[(j,v,h)] - self.a[(j,v,h)] + \
                        self.params[
                            'time_windows'
                        ][j][1] >= 0,
                            'Time Window Constraint 2 ({j},{v},{h})'.format(
                                j=j,v=v,h=h
                            )

    def solve(self):
        self.model.solve()
        print("Status:", pulp.LpStatus[self.model.status])

    def get_solution(self):
        solution = {
            v.name : v.varValue \
                for v in self.model.variables()
        }
        solution.update({
            'objective' : pulp.value(gemstoneprob.objective)
        })
        return solution

