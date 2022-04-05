import pulp as pl
import numpy as np
import os
import shutil

class MVRPModel:
    def __init__(self, params):
        self.params = params
        self.problem = pl.LpProblem('MVRP', pl.LpMinimize)
        self.setup()

    def create_variables(self):
        self.y = np.array([
            [
                [
                    pl.LpVariable('y_{}_{}_{}'.format(i, v, h), 0, 1) for h in range(self.params['num_trips'])
                ] for v in range(self.params['num_vehicles'])
            ] for i in range(self.params['num_customers'] + 1)
        ])

        self.z = np.array([
            [
                [
                    [
                        pl.LpVariable('z_{}_{}_{}_{}'.format(i, j, v, h)) for h in range(self.params['num_trips'])
                    ] for v in range(self.params['num_vehicles'])
                ] for j in range(self.params['num_customers'] + 1)
            ] for i in range(self.params['num_customers'] + 1)
        ])

        self.k = np.array([
            [
                pl.LpVariable('k_{}_{}'.format(v, h), 0) for h in range(self.params['num_trips'])
            ] for v in range(self.params['num_vehicles'])
        ])

        self.D = np.array([
            pl.LpVariable('D_{}'.format(i), 0) for i in range(1, self.params['num_customers'] + 1)
        ])

        self.T = np.array([
            pl.LpVariable('T_{}'.format(i), 0) for i in range(1, self.params['num_customers'] + 1)
        ])

    def create_constraints(self):
        # Customer must be visited exactly once
        for i in range(1, self.params['num_customers'] + 1):
            self.problem += np.sum(self.y[i]) == 1, 'CustomerVisitationContraint_{}'.format(
                i
            )

        # Customer Assignment to Active Tour Constraint
        for i in range(1, self.params['num_customers'] + 1):
            for v in range(self.params['num_vehicles']):
                for h in range(self.params['num_trips']):
                    self.problem += self.y[0, v, h] - self.y[i, v, h] >= 0, 'ActiveTourCustomerAssignmentConstraint_{}_{}_{}'.format(i, v, h)

        # Multiple Trip Constraints
        for v in range(self.params['num_vehicles']):
            for h in range(self.params['num_trips'] - 1):
                self.problem += self.params['M'] * np.sum(self.y[1:, v, h]) - np.sum(self.y[1:, v, h + 1]) >= 0, 'ActiveTourConstraint_{}_{}'.format(
                    v, h
                )

        # Continuity or Travel Flow constraints (a)
        for j in range(self.params['num_customers']):
            for v in range(self.params['num_vehicles']):
                for h in range(self.params['num_trips']):
                    self.problem += self.y[j, v, h] - np.sum(self.z[j, :, v, h]) + self.z[j, j, v, h] == 0, 'TravelFlowConstraint_a_{}_{}_{}'.format(
                        j, v, h
                    )
        # Continuity or Travel Flow constraints (b)    
        for j in range(1, self.params['num_customers'] + 1):
            for v in range(self.params['num_vehicles']):
                for h in range(self.params['num_trips']):
                    self.problem += self.y[j, v, h] - np.sum(self.z[:, j, v, h]) + self.z[j, j, v, h] == 0, 'TravelFlowConstraint_b_{}_{}_{}'.format(
                        j, v, h
                    )

        # Capacity Constraint
        for v in range(self.params['num_vehicles']):
            for h in range(self.params['num_trips']):
                self.problem += np.sum(self.params['demand'] * np.repeat(
                    np.expand_dims(self.y[1:, v, h], -1), self.params['num_products'], -1
                )) <= self.params['vehicle_capacity'][v], 'CapacityConstraint_{}_{}'.format(
                    v, h
                )



        # Minimum Delivery Start Time Constraint
        for v in range(self.params['num_vehicles']):
            for h in range(self.params['num_trips']):
                self.problem += self.k[v, h] >= self.params['service_time'][0], 'MinimumDeliveryStartTimeConstraint_{}_{}'.format(
                    v, h
                )

        # First Trip Delivery Start Time Constraint
        for v in range(self.params['num_vehicles']):
            self.problem += self.k[v, 1] >= self.params['F'] + self.params['service_time'][0], 'FirstTripDeliveryConstraint_{}'.format(v)

        # Consecutive Trip Start Time Constraint
        for i in range(self.params['num_customers']):
            for v in range(self.params['num_vehicles']):
                for h in range(self.params['num_trips'] - 1):
                    self.problem += self.k[v, h + 1] - self.D[i] - self.params['service_time'][i + 1] - self.params['travel_time'][i, 0] - self.params['service_time'][0] + self.params['M'] * (1 - self.y[i, v, h]) >= 0, 'ConsecutiveTripStartTimeConstraint_{}_{}_{}'.format(
                                i, v, h
                            )

        # Lower Time Window Constraint
        for i in range(self.params['num_customers'] - 1):
            self.problem += self.D[i] >= self.params['time_window'][0], 'LowerTimeWindowConstraint_{}'.format(i)

        # First Customer Delivery Time Constraint
        for i in range(self.params['num_customers'] - 1):
            for v in range(self.params['num_vehicles']):
                for h in range(self.params['num_trips']):
                    self.problem += self.D[i] - self.k[v, h] - self.params['time_window'][0, i] + self.params['M'] * (1 - self.y[i + 1, v, h]) >= 0, 'FirstCustomerDeliveryTimeConstraint_{}_{}_{}'.format(i, v, h)

        # Consecutive Customer Delivery Time Constraint
        for i in range(self.params['num_customers'] - 1):
            for j in range(self.params['num_customers'] - 1):
                for v in range(self.params['num_vehicles']):
                    for h in range(self.params['num_trips']):
                        if i != j:
                            self.problem += self.D[j] - self.D[i] - self.params['service_time'][i + 1] - self.params['travel_time'][i + 1][j + 1] + self.params['M'] * (1 - self.z[i + 1, j + 1, v, h]) >= 0, 'ConsecutiveCustomerDeliveryTimeConstraint_{}_{}_{}_{}'.format(
                                    i, j, v, h
                                )

        # Upper Time Window Constraint
        for i in range(1, self.params['num_customers']):
            self.problem += self.T[i] - self.D[i] + self.params['time_window'][1, i] >= 0, 'UpperTimeWindowConstraint_{}'.format(i)

    def create_objective(self):
        dc1 = self.params['c1'] * np.sum(self.z[0, 1:])
        expanded_travel_time = np.repeat(
            np.expand_dims(
                np.repeat(
                    np.expand_dims(
                        self.params['travel_time'], -1
                    ), self.params['num_vehicles'], -1
                ), -1
            ), self.params['num_trips'], -1
        )
        dc2 = self.params['c2'] * np.sum(expanded_travel_time * self.z) - sum([
            np.sum(expanded_travel_time[i, i] * self.z[i, i]) for i in range(self.params['num_customers'])
        ])

        pc = self.params['c3'] * np.sum(self.T)

        self.problem ++ dc1 + dc2 + pc, 'Objective'

    def setup(self): 
        self.create_variables()
        self.create_constraints()
        self.create_objective()

    def solve(self):
        self.problem.solve()

    def store_solution(self, logdir):
        if os.path.exists(logdir):
            shutil.rmtree(logdir)
        os.mkdir(logdir)


