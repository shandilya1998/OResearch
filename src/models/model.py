import numpy as np

class MIPModel:
    def __init__(self, params):
        self.params = params

    def build(self):
        self.num_variables = \
            self.params['num_products'] * self.params['num_batches'] + \
            self.params['num_products'] * self.params['num_batches'] + \
            self.params['num_vehicles'] * self.params['num_trips'] + \
            self.params['num_nodes'] * self.params['num_vehicles'] * \
                self.params['num_trips'] + \
            self.params['num_nodes'] * self.params['num_vehicles'] * \
                self.params['num_trips'] + \
            self.params['num_nodes'] * self.params['num_vehicles'] * \
                self.params['num_trips'] + \
            self.params['num_products'] * self.params['num_products'] + \
            self.params['num_customers'] * self.params['num_batches'] + \
            self.params['num_batches'] + \
            self.params['num_batches'] * self.params['num_batches'] + \
            self.params['num_batches'] * self.params['num_vehicles'] * \
                self.params['num_trips'] + \
            self.params['num_nodes'] * self.params['num_vehicles'] * \
                self.params['num_trips'] + \
            self.params['num_nodes'] * self.params['num_nodes'] * \
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
            (self.params['num_customers'] + 1) * \
                (self.params['num_customers'] + 1) * \
                self.params['num_vehicles'] * self.params['num_trips'] + \
            self.params['num_vehicles'] * self.params['num_batches'] + \
            self.params['num_vehicles'] * self.params['num_trips'] * \
                self.params['num_batches'] + \
            self.params['num_vehicles'] * self.params['num_trips'] * \
                self.params['num_batches'] * self.params['num_products'] + \
            2 * self.params['num_customers'] * self.params['num_vehicles'] * \
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
        print('-----------------------')
        print('Number of Variables:\n{num}'.format(num = self.num_variables))
        print('-----------------------')
        print('-----------------------')
        print('Number of Constraints:\n{num}'.format(
            num = self.num_constraints)
        )
        print('-----------------------')
        self.A = np.zeros((self.num_constraints, self.num_variables))
        self.b = np.zeros((self.num_constraints, ))
        self.c = np.zeros((self.num_variables, ))
        self._create_variable_indices()


        """
            Integer Variable Constraint on 'x'
        """
        start = 0
        end = len(self.indices['x'])
        self.A[start: end, self.indices['x']] = 1
        self.b[start: end] = 1

        """
            Boolean Variable Contstaint on 'b'
        """
        start = end
        end += len(self.indices['b'])
        self.A[start: end, self.indices['b']] = 1
        self.b[start: end] = 1

        """
            Boolean Variable Constraint on 'd'
        """
        start = end
        end += len(self.indices['d'])
        self.A[start: end, self.indices['d']] = 1
        self.b[start: end] = 1

        """
            Boolean Variable Contraint on 'g'
        """
        start = end
        end += len(self.indices['g'])
        self.A[start: end, self.indices['g']] = 1
        self.b[start: end] = 1

        """
            Boolean Variable Contraint on 't'
        """
        start = end
        end += len(self.indices['t'])
        self.A[start: end, self.indices['t']] = 1
        self.b[start: end] = 1

        """
            Boolean Variable Contraint on 'u'
        """
        start = end
        end += len(self.indices['u'])
        self.A[start: end, self.indices['u']] = 1
        self.b[start: end] = 1

        """
            Boolean Variable Contraint on 'y'
        """
        start = end
        end += len(self.indices['y'])
        self.A[start: end, self.indices['y']] = 1
        self.b[start: end] = 1

        """
            Visit Once Contraint
        """
        start = end
        end += self.params['num_customers']
        #for i in range(start, end):
        #    self.A[i, self.]

    def _create_variable_indices(self):
        self.indices = {}

        start = 0
        end = self.params['num_products'] * self.params['num_batches']
        self.indices['s'] = list(range(start, end))

        start = end
        end += self.params['num_products'] * self.params['num_batches']
        self.indices['c'] = list(range(start, end))

        start = end
        end += self.params['num_vehicles'] * self.params['num_trips']
        self.indices['st'] = list(range(start, end))

        start = end
        end += self.params['num_nodes'] * self.params['num_vehicles'] * \
            self.params['num_trips']
        self.indices['a'] = list(range(start, end))

        start = end
        end += self.params['num_nodes'] * self.params['num_vehicles'] * \
            self.params['num_trips']
        self.indices['e'] = list(range(start, end))

        start = end
        end += self.params['num_nodes'] * self.params['num_vehicles'] * \
            self.params['num_trips']
        self.indices['l'] = list(range(start, end))

        start = end
        end += self.params['num_products'] * self.params['num_products']
        self.indices['x'] = list(range(start, end))

        start = end
        end += self.params['num_customers'] * self.params['num_batches']
        self.indices['b'] = list(range(start, end))

        start = end
        end += self.params['num_batches']
        self.indices['d'] = list(range(start, end))

        start = end
        end += self.params['num_batches'] * self.params['num_batches']
        self.indices['g'] = list(range(start, end))

        start = end
        end += self.params['num_batches'] * self.params['num_vehicles'] * \
            self.params['num_trips']
        self.indices['t'] = list(range(start, end))

        start = end
        end += self.params['num_nodes'] * self.params['num_vehicles'] * \
            self.params['num_trips']
        self.indices['u'] = list(range(start, end))

        start = end
        end += self.params['num_nodes'] * self.params['num_nodes'] * \
            self.params['num_vehicles'] * self.params['num_trips']
        self.indices['y'] = list(range(start, end))

        start = end
        end += self.params['num_vehicles']
        self.indices['w'] = list(range(start, end))
