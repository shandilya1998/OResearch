import numpy as np

"""
    Refer to the following link for indexing of 3D array to 1D array
        https://stackoverflow.com/questions/7367770/how-to-flatten-or-index-3d-array-in-1d-array

    Refer to the following links for indexing 2D array to 1D array and
    vice versa
        https://stackoverflow.com/questions/5134555/how-to-convert-a-1d-array-to-2d-array
        https://stackoverflow.com/questions/2151084/map-a-2d-array-onto-a-1d-array

"""

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
            self.params['num_vehicles'] * (self.params['num_trips'] - 1) + \
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
        xmax = self.params['num_nodes']
        ymax = self.params['num_vehicles']
        xmax = self.params['num_trips']
        u_start = self.indices['u'][0]
        u_end = self.indices['u'][-1]
        for i in range(self.num_params):
            for v in range(self.params['num_vehicles']):
                for h in range(self.params['num_trips']):
                    idx = self._3Dto1D(i+1, v, h, xmax, ymax, zmax) + u_start
                    if idx > _end:
                        raise ValueError
                    self.A[i + start, idx] = 1
            self.b[i + start] = 1

        """
            Active Tour Constraint
        """
        start = end
        end += self.params['num_customers'] * self.params['num_vehicles'] * \
            self.params['num_trips']
        for i in range(self.params['num_customers']):
            for v in range(self.params['num_vehicles']):
                for h in range(self.params['num_trips']):
                    idx1 = self._3Dto1D(0, v, h, xmax, ymax, zmax) + u_start
                    idx2 = self._3Dto1D(i+1, v, h, xmax, ymax, zmax) + u_start
                    idx3 = self._3Dto1D(i, v, h, xmax, ymax, zmax) + start
                    self.A[idx3, idx1] = -1
                    self.A[idx3, idx2] = 1

        """
            Capacity Constraint
        """
        start = end
        end += self.params['num_vehicles'] * self.params['num_trips']
        _xmax = self.params['num_vehicles']
        _ymax = self.params['num_trips']
        for v in range(self.params['num_vehicles']):
            for h in range(self.params['num_trips']):
                idx1 = self._2Dto1D(v, h, _xmax, _ymax)
                for j in range(self.params['num_customers']):
                    d_jp = np.sum(self.params['demand'], -1)
                    idx2 = self._3Dto1D(j + 1, v, h, xmax, ymax, zmax)
                    self.A[idx1 + start, idx2 + u_start] = d_jp
                self.b[idx1] = self.params['vehicle_capacity'][v]

        """
            Start End Constraints
        """
        start = end
        end += self.params['num_customers'] * self.params['num_customers'] * \
            self.params['num_vehicles'] * self.params['num_trips']
        xmax = self.params['num_nodes']
        ymax = self.params['num_nodes']
        zmax = self.params['num_vehicles']
        umax = self.params['num_trips']
        _xmax = self.params['num_nodes']
        _ymax = self.params['num_vehicles']
        _zmax = self.params['num_trips']
        y_start = self.indices['y'][0]
        y_end = self.indices['y'][-1]
        #Start End Constraint 1
        for i in range(self.params['num_customers']):
            for j in range(self.params['num_customers']):
                for v in range(self.params['num_vehicles']):
                    for h in range(self.params['num_trips']):
                        idx1 = self._4Dto1D(i, j, v, h, xmax, ymax, zmax, umax)
                        idx2 = self._4Dto1D(0,j+1, v, h, xmax, ymax, zmax, umax)
                        idx3 = self._4Dto1D(i+1,0, v, h, xmax, ymax, zmax, umax)
                        idx4 = self._3Dto1D(i+1, v, h, _xmax, _ymax, _zmax)
                        idx5 = self._3Dto1D(j+1, v, h, _xmax, _ymax, _zmax)
                        """
                             Start End Constraint 1
                        """
                        self.A[idx1 + start, idx2 + y_start] = 1
                        self.A[idx1 + start, idx3 + y_start] = 1
                        self.A[idx1 + start, idx4 + u_start] = 1
                        self.A[idx1 + start, idx5 + u_start] = 1
                        self.b[idx1 + start] = 3

        #Start End Constraint 2
        start = end
        end += self.params['num_customers'] * self.params['num_customers'] * \
            self.params['num_vehicles'] * self.params['num_trips']
        for i in range(self.params['num_customers'] + 1):
            for j in range(self.params['num_customers']):
                for v in range(self.params['num_vehicles']):
                    for h in range(self.params['num_trips']):
                        idx1 = self._3Dto1D(j, v, h, ymax, zmax, umax)
                        idx2 = self._4Dto1D(i, j+1, v, h, xmax, ymax, zmax, \
                            umax)
                        idx3 = self._3Dto1D(j+1, v, h, ymax, zmax, umax)
                        if i!= j:
                            self.A[idx1 + start, idx2 + y_start] = -1
                        self.A[idx1 + start, idx3 + u_start] = 1

        #Start End Constraint 3
        start = end
        end += self.params['num_customers'] * self.params['num_customers'] * \
            self.params['num_vehicles'] * self.params['num_trips']
        for i in range(1, self.params['num_nodes']):
            for j in range(self.params['num_customers']):
                for v in range(self.params['num_vehicles']):
                    for h in range(self.params['num_trips']):
                        idx1 = self._3Dto1D(j, v, h, ymax, zmax, umax)
                        idx2 = self._4Dto1D(i, j + 1, v, h, xmax, ymax, zmax, \
                            umax)
                        idx3 = self._3Dto1D(j + 1, v, h, ymax, zmax, umax)
                        if i!= j:
                            self.A[idx1 + start, idx2 + y_start] = -1
                        self.A[idx1 + start, idx3 + u_start] = 1

        #Start End Constraint 3
        start = end
        end += self.params['num_customers'] * self.params['num_customers'] * \
            self.params['num_vehicles'] * self.params['num_trips']
        for i in range(self.params['num_customers'] + 1):
            for j in range(self.params['num_customers']):
                for v in range(self.params['num_vehicles']):
                    for h in range(self.params['num_trips']):
                        idx1 = self._4Dto1D(i, j, v, h, xmax, ymax, zmax, umax)
                        idx2 = self._4Dto1D(i + 1, j + 1, v, h, xmax, ymax, \
                            zmax, umax)
                        idx3 = self._3Dto1D(i + 1, v, h, ymax, zmax, umax)
                        idx4 = self._3Dto1D(j + 1, v, h, ymax, zmax, umax)
                        self.A[idx1 + start, idx2 + y_start] = 1
                        self.A[idx1 + start, idx3 + u_start] = -1
                        self.A[idx1 + start, idx4 + u_start] = 1
                        self.b[idx1 + start] = 1

        #Start End Constraint 4
        start = end
        end += self.params['num_customers'] * self.params['num_customers'] * \
            self.params['num_vehicles'] * self.params['num_trips']
        for i in range(self.params['num_customers'] + 1):
            for j in range(self.params['num_customers']):
                for v in range(self.params['num_vehicles']):
                    for h in range(self.params['num_trips']):
                        idx1 = self._4Dto1D(i, j, v, h, xmax, ymax, zmax, umax)
                        idx2 = self._4Dto1D(i + 1, j + 1, v, h, xmax, ymax, \
                            zmax, umax)
                        idx3 = self._3Dto1D(i + 1, v, h, ymax, zmax, umax)
                        idx4 = self._3Dto1D(j + 1, v, h, ymax, zmax, umax)
                        self.A[idx1 + start, idx2 + y_start] = -1
                        self.A[idx1 + start, idx3 + u_start] = 1
                        self.A[idx1 + start, idx4 + u_start] = 1
                        self.b[idx1 + start] = 1

        """
            Active Trip Constraint
        """
        start = end
        end += self.params['num_vehicles'] * (self.params['num_trips'] - 1)
        xmax = self.params['num_nodes']
        ymax = self.params['num_vehicles']
        zmax = self.params['num_trips']
        for v in range(self.params['num_vehicles']):
            for h in range(self.params['num_trips']) - 1:
                idx1 = self._2Dto1D(v, h, ymax, zmax)
                for j in range(self.params['num_customers']):
                    idx2 = self._3Dto1D(j, v, h, xmax, ymax, zmax)
                    idx3 = self._3Dto1D(j, v, h + 1, xmax, ymax, zmax)
                    self.A[idx1 + start, idx2 + u_start] = -self.params['M']
                    self.A[idx1 + start, idx3 + u_start] = 1

        """
            Used Vehicle Constraint
        """
        start = end
        end += self.params['num_vehicles'] * self.params['num_trips']
        xmax = self.params['num_nodes']
        ymax = self.params['num_vehicles']
        zmax = self.params['num_trips']
        w_start = self.indices['w'][0]
        w_end = self.indices['w'][-1]
        for v in range(self.params['num_vehicles']):
            for h in range(self.params['num_trips']):
                idx1 = self._2Dto1D(v, h, ymax, zmax)
                idx2 = self._3Dto1D(0, v, h, xmax, ymax, zmax)
                self.A[idx1 + start, idx2 + u_start] = -1
                self.A[idx1 + start, v + w_start] = 1

        """
            Production Sequence Constraint
        """
        start = end
        end += 1
        xmax = self.params['num_prodcuts']
        ymax = self.params['num_products']
        p_start = self.indices[0]
        p_end = self.indices[-1]
        for p in range(self.params['num_products']):
            #idx1  
            for q in range(self.params['num_products']):
                idx1 = self._2Dto1D(p, q, xmax, ymax)
                idx2 = self._2Dto1D(q, p, xmax, ymax)
                if p != q:
                    self.A[start, idx1]

    def _3Dto1D(self, x, y, z, xmax, ymax, zmax):
        return (z * xmax * ymax) + (y * xmax) + x

    def _1Dto3D(self, idx, xmax, ymax, zmax):
        z = int(idx / (xmax * ymax))
        idx -= (z * xmax * ymax)
        y = idx / xmax
        x = idx % xmax
        return x, y, z

    def _2Dto1D(self, x, y, xmax, ymax):
        return y*xmax + x

    def _1Dto2D(self, idx, xmax, ymax):
        x = idx % xmax
        y = int(idx / xmax)
        return x, y

    def _4Dto1D(self, x, y, z, u, xmax, ymax, zmax, umax):
        return x + xmax * (y + ymax * (z + zmax * u))

    def _1Dto4D(self, idx, xmax, ymax, zmax, umax):
        x = idx % xmax
        idx = (idx - x) / xmax
        y = idx % ymax
        idx = (idx - y) / ymax
        z = idx % zmax
        u = (idx - z) / zmax
        return x, y, z, u

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
