import numpy as np

class MIPModel:
    def __init__(self, params):
        self.params = params

    def build(self):
        self.num_variables = \
            self.params['num_products'] * self.params['num_batches'] + \
            self.params['num_products'] * self.params['num_batches'] + \
            self.params['num_vehicles'] * self.params['num_trips'] + \
            self.params['num_customers'] * self.params['num_vehicles'] * \
                self.params['num_trips'] + \
            self.params['num_customers'] * self.params['num_vehicles'] * \
                self.params['num_trips'] + \
            self.params['num_customers'] * self.params['num_vehicles'] * \
                self.params['num_trips'] + \
            self.params['num_products'] * self.params['num_products'] + \
            self.params['num_customers'] * self.params['num_batches'] + \
            self.params['num_batches'] + \
            self.params['num_batches'] * self.params['num_batches'] + \
            self.params['num_batches'] * self.params['num_vehicles'] * \
                self.params['num_trips'] + \
            self.params['num_customers'] * self.params['num_vehicles'] * \
                self.params['num_trips'] + \
            self.params['num_customers'] * self.params['num_customers'] * \
                self.params['num_vehicles'] * self.params['num_trips'] + \
            self.params['num_vehicles']

        self.num_constraints = self.params['num_customers'] + \
            self.params['num_customers'] * self.params['num_vehicles'] * \
                self.params['num_trips'] + \
            self.params['num_vehicles'] * self.params['num_trips'] + \
            self.params['num_customers'] * self.params['num_customers'] * \
                self.params['num_vehicles'] * self.params['num_trips'] + \
            2 * self.params['num_customers'] * self.params['num_vehicles'] * \
                self.params['num_trips'] + \
            2 * self.params['num_customers'] * self.params['num_customers'] * \
                self.params['num_vehicles'] * self.params['num_trips'] + \
            self.params['num_vehicles'] * self.params['num_trips'] + \
            self.params['num_vehicles'] * self.params['num_trips'] + \
            2 * self.params['num_products'] + \
            self.params['num_products'] * self.params['num_products'] + \
            1 + \
            self.params['num_batches'] + \
            self.params['num_vehicles'] * self.params['num_trips'] + \
            self.params['num_batches'] + \
            self.params['num_customers'] + \
            self.params['num_customers'] * self.params['num_batches'] * \
                self.params['num_vehicles'] * self.params['num_trips'] + \
            self.params['num_customers'] * self.params['num_batches'] * \
                self.params['num_vehicles'] * self.params['num_trips'] + \
            self.params['num_batches'] + \
            self.params['num_products'] * self.params['num_batches'] + \
            self.params['num_products'] * self.params['num_batches'] * \
                self.params['num_batches'] + \
            self.params['num_customers'] * self.params['num_vehicles'] * \
                self.params['num_trips'] + \
            self.params['num_customers'] * self.params['num_customers'] * \
                self.params['num_vehicles'] * self.params['num_trips'] + \
            self.params['num_vehicles'] * self.params['num_batches'] + \
            self.params['num_vehicles'] * self.params['num_trips'] * \
                self.params['num_batches'] + \
            self.params['num_vehicles'] * self.params['num_trips'] * \
                self.params['num_batches'] * self.params['num_products'] + \
            2 * self.params['num_customers'] * self.params['num_vehicles'] * \
                self.params['num_trips']


