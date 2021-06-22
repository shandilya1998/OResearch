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
            self.parmas['num_products'] + 1 + \
            self.parmas['num_vehicles'] * self.params['num_trips'] + \
            2 * self.params['num_customers'] + \
            self.params['num_products'] * self.params['num_products'] + \
            self.params['num_customers'] * self.params['num_vehicles'] * \
                self.params['num_trips'] + \
            self.params['num_customers'] * self.params['num_customers'] * \
                self.params['num_vehicles'] * self.params['trips']

        self.num_constraints = self.params['num_customers'] + \

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

        start = 0
        end = self.params['num_products']
        for i in range(self.params['num_products']):
            self.A[start + i, self.indices['x'][
                self.params['num_products'] * i: \
                    self.params['num_products'] * (i + 1)
            ]] = 1
            self.A[start + i, self.indices['x'][i]] = 0
        self.b[start: end] = 1

        start = end
        end += self.params['num_products']
        for i in range(self.params['num_products']):
            indices = [self.indices['x'][j] for j in range(i, \
                self.params['num_products'] * self.params['num_products'], \
                self.params['num_products'])]
            self.A[start + i, indices] = 1
            self.A[start + i, self.indices['x'][i]] = 0
        self.b[start: end] = 1

        start = end
        end += self.params['num_products']
        for i in range(self.params['num_products']):
            self.A[start: end, self.indices['f'][i]] = 1
            for j in range(self.params['num_customers']):
                self.b[start + i] += self.params['process_time'][i] * \
                    self.params['demand'][j + 1][i]

        start = end
        end += self.params['num_products'] * self.params['num_products']
        for i in range(end - start):
            for p in range(self.params['num_products']):
                for q in range(self.params['num_products'])
                    self.A[
                        start + i
                    ][]
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
        for i in range(self.params['num_customers']):
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
        end += self.params['num_products']
        xmax = self.params['num_prodcuts']
        ymax = self.params['num_products']
        x_start = self.indices['x'][0]
        x_end = self.indices['x'][-1]
        for p in range(self.params['num_products']):
            for q in range(self.params['num_products']):
                idx1 = self._2Dto1D(p, q, xmax, ymax)
                if p != q:
                    self.A[p + start, idx1 + x_start] = 1
        start = end
        end += self.params['num_products']
        for p in range(self.params['num_products']):
            for q in range(self.params['num_products']):
                idx1 = self._2Dto1D(q, p, xmax, ymax)
                if p != q:
                    self.A[p + start, idx1 + x_start] = 1

        """
            Batch Trip Constraints
        """
        start = end
        end += 1
        xmax = self.params['num_nodes']
        ymax = self.params['num_vehicles']
        zmax = self.params['num_trips']
        for v in range(self.params['num_vehicles']):
            for h in range(self.params['num_trips']):
                idx = self._3Dto1D(0, v, h, xmax, ymax, zmax)
                self.A[start, idx + u_start] = 1
        d_start = self.indices['d'][0]
        d_end = self.indices['d'][-1]
        for f in range(self.params['num_batches']):
            self.A[start, f + d_start] = -1

        start = end
        end += self.params['num_batches'] - 1
        for f in range(self.params['num_batches'] - 1):
            self.A[f + start, f + d_start] = -1
            self.A[f + start, f + d_start + 1] = 1

        """
            Active Trip Batch Constraints
        """
        start = end
        end += self.params['num_vehicles'] * self.params['num_trips']
        _xmax = self.params['num_batches']
        t_start = self.indices['t'][0]
        t_end = self.indices['t'][-1]
        for v in range(self.params['num_vehicles']):
            for h in range(self.params['num_vehicles']):
                idx1 = self._2Dto1D(v, h, ymax, zmax)
                for f in range(self.params['num_batches']):
                    idx3 = self._3Dto1D(f, v, h, _xmax, ymax, zmax)
                    self.A[idx1 + start, idx3 + t_start] = -1
                idx2 = self._3Dto1D(0, v, h, xmax, ymax, zmax)
                self.A[idx1 + start, idx2 + u_start] = 1
        start = end
        end += self.params['num_batches']
        for f in range(self.params['num_batches']):
            self.A[f + start, f + d_start] = 1
            for v in range(self.params['num_vehicles']):
                for h in range(self.params['num_trips']):
                    idx = self._3Dto1D(f, v, h, _xmax, ymax, zmax)
                    self.A[f + start, idx + t_start] = -1

        """
            Customer Batch Constraints
        """
        start = end
        end += self.params['num_customers']
        xmax = self.params['num_customers']
        ymax = self.params['num_batches']
        b_start = self.indices['b'][0]
        b_end = self.indices['b'][-1]
        for j in range(self.params['num_customers']):
            for f in range(self.params['num_batches']):
                idx = self._2Dto1D(j, f, xmax, ymax)
                self.A[j + start, idx + b_start]
            self.b[j + start] = 1

        """
            Link1 Constraint
        """
        start = end
        end += self.params['num_customers'] * self.params['num_batches'] * \
            self.params['num_vehicles'] * self.params['num_trips']
        _xmax = self.params['num_nodes']
        zmax = self.params['num_vehicles']
        umax = self.params['num_trips']
        for j in range(1, self.params['num_customers'] + 1):
            for f in range(self.params['num_batches']):
                for v in range(self.params['num_vehicles']):
                    for h in range(self.params['num_trips']):
                        idx1 = self._4Dto1D(j - 1, f, v, h, _xmax, ymax, zmax, \
                            umax)
                        idx2 = self._2Dto1D(j, f, xmax, ymax)
                        idx3 = self._3Dto1D(j, v, h, _xmax, zmax, umax)
                        idx4 = self._3Dto1D(f, v, h, ymax, zmax, umax)
                        self.A[idx1 + start, idx2 + b_start] = -1
                        self.A[idx1 + start, idx3 + u_start] = 1
                        self.A[idx1 + start, idx4 + t_start] = 1

        """
            Link2 Constraint
        """
        start = end
        end += self.params['num_customers'] * self.params['num_batches'] * \
            self.params['num_vehicles'] * self.params['num_trips']
        for j in range(1, self.params['num_customers'] + 1):
            for f in range(self.params['num_batches']):
                for v in range(self.params['num_vehicles']):
                    for h in range(self.params['num_trips']):
                        idx1 = self._4Dto1D(j - 1, f, v, h, _xmax, ymax, zmax, \
                                umax)
                        idx2 = self._3Dto1D(f, v, h, ymax, zmax, umax)
                        idx3 = self._2Dto1D(j, f, xmax, ymax)
                        idx4 = self._3Dto1D(j, v, h, _xmax, zmax, umax)
                        self.A[idx1 + start, idx2 + t_start] = -1
                        self.A[idx1 + start, idx3 + b_start] = 1
                        self.A[idx1 + start, idx4 + u_start] = 1
                        self.b[idx1 + start] = 1

        """
            Batch Production Sequence Constraint
        """
        start = end
        end += self.params['num_batches']
        xmax = self.params['num_batches']
        ymax = self.params['num_batches']
        g_start = self.indices['g'][0]
        g_end = self.indices['g'][-1]
        for f in range(self.params['num_batches']):
            for f_ in range(self.params['num_batches']):
                if f != f_:
                    idx1 = self._2Dto1D(f_, f, xmax, ymax)
                    self.A[f + start, idx1 + g_start ] = -1
            self.A[f + start, f + d_start] = 1

        start = end
        end += self.params['num_batches']
        for f in range(self.params['num_batches']):
            for f_ in range(self.params['num_batches']):
                if f != f_:
                    idx1 = self._2Dto1D(f, f_, xmax, ymax)
                    self.A[f + start, idx1 + g_start] = -1
            self.A[f + start, f + d_start] = 1

        """
            Production Completion Constraint
            Mistakes in this formulations need correction
        """
        start = end
        end += self.params['num_products'] * self.params['num_batches']
        xmax = self.params['num_products']
        ymax = self.params['num_batches']
        zmax = self.params['num_products']
        umax = self.params['num_customers']
        c_start = self.indices['c'][0]
        c_end = self.indices['c'][-1]
        for p in range(self.params['num_products']):
            for f in range(self.params['num_batches']):
                idx = self._2Dto1D(p, f, xmax, ymax)
                idx3 = self._2Dto1D(0, f, ymax, ymax)
                self.b[idx + start] = self.params['M']
                for _p in range(self.params['num_products']):
                    for _q in range(self.params['num_products']):
                        if _p != _q:
                            idx1 = self._2Dto1D(_p, _q, xmax, zmax)
                            self.A[idx + start, idx1 + x_start] = \
                                self.params['setup_time']
                    for j in range(self.params['num_customers']):
                        idx2 = self._2Dto1D(j, f, umax, ymax)
                        self.A[idx + start, idx2 + b_start] = \
                            self.params['process_time'] * \
                            self.params['demand'][j + 1][_p]
                self.A[idx + start, idx3 + g_start] = self.params['M']
                self.A[idx + start, idx + c_start] = -1

        start = end
        end += self.params['num_products'] * self.params['num_batches'] * \
            self.params['num_batches']
        wmax = self.params['num_batches']
        s_start = self.indices['s'][0]
        s_end = self.indices['s'][-1]
        for p in range(self.params['num_products']):
            for f in range(self.params['num_batches']):
                for f_ in range(self.params['num_batches']):
                    idx = self._3Dto1D(p, f, f_, xmax, ymax, wmax)
                    idx3 = self._2Dto1D(f, f_, ymax, wmax)
                    idx4 = self._2Dto1D(p, f_, xmax, ymax)
                    self.b[idx + start] = self.params['M']
                    for _p in range(self.params['num_products']):
                        for _q in range(self.params['num_products']):
                            if _p != _q:
                                idx1 = self._2Dto1D(_p, _q, xmax, zmax)
                                self.A[idx + start, idx1 + x_start] = \
                                    self.params['setup_time']
                        for j in range(self.params['num_customers']):
                            idx2 = self._2Dto1D(j, f, umax, ymax)
                            self.A[idx + start, idx2 + b_start] = \
                                self.params['process_time'] * \
                                self.params['demand'][j + 1][_p]
                    self.A[idx + start, idx3 + g_start] = self.params['M']
                    self.A[idx + start, idx4 + c_start] = -1
                    self.A[idx + start, idx + start] = 1

        """
            Arrival Customer Constraints
        """
        start = end
        end += self.params['num_customers'] * self.params['num_vehicles'] * \
            self.params['num_trips']
        xmax = self.params['num_nodes']
        ymax = self.params['num_vehicles']
        zmax = self.params['num_trips']
        umax = self.params['num_batches']
        a_start = self.indices['a'][0]
        a_end = self.indices['s'][-1]
        st_start = self.indices['st'][0]
        st_end = self.indices['st'][-1]
        for j in range(self.params['num_customers']):
            for v in range(self.params['num_vehicles']):
                for h in range(self.params['num_trips']):
                    idx = self._3Dto1D(j, v, h, xmax, ymax, zmax)
                    idx1 = self._3Dto1D(j + 1, v, h, xmax, ymax, zmax)
                    idx2 = self._2Dto1D(v, h, ymax, zmax)
                    idx3 = self._2Dto1D(0, j + 1, umax, xmax)
                    idx4 = self._3Dto1D(j + 1, v, h, xmax, ymax, zmax)
                    self.A[idx + start, idx1 + a_start] = -1
                    self.A[idx + start, idx2 + st_start] = 1
                    self.A[idx + start, idx3 + t_start] = 1
                    self.A[idx + start, idx4 + u_start] = self.params['M']
                    self.b[idx + start] = self.params['M'] + \
                        self.params['service_time'][0]

        """
            Arrival Next Constraints
        """
        start = end
        end += (self.params['num_customers'] + 1) * \
            (self.params['num_customers'] + 1) * \
            self.params['num_vehicles'] * self.params['num_trips']
        xmax = self.params['num_nodes']
        ymax = self.params['num_nodes']
        zmax = self.params['num_vehicles']
        umax = self.params['num_trips']
        for i in range(self.params['num_customers'] + 1):
            for j in range(self.params['num_customers'] + 1):
                for v in range(self.params['num_vehicles']):
                    for h in range(self.params['num_trips']):
                        idx = self._4Dto1D(i, j, v, h, xmax, ymax, zmax, umax)
                        idx1 = self._3Dto1D(j + 1, v, h, ymax, zmax, umax)
                        idx2 = self._3Dto1D(i, v, h, xmax, zmax, umax)
                        idx3 = self._2Dto1D(i, j + 1, xmax, ymax)
                        idx4 = self._4Dto1D(i, j + 1, v, h, xmax, ymax, zmax, \
                            umax)
                        self.A[idx + start, idx1 + a_start] = -1
                        self.A[idx + start, idx2 + a_start] = 1
                        self.A[idx + start, idx3 + t_start] = 1
                        self.A[idx + start, idx4 + y_start] = self.params['M']
                        self.b[idx + start] = self.params['M'] + \
                            self.params['service_time'][i]

        """
            Start Tour Constraint
        """
        start = end
        end += self.params['num_products'] * self.params['num_vehicles'] * \
            self.params['num_batches']
        xmax = self.params['num_products']
        ymax = self.params['num_vehicles']
        zmax = self.params['num_batches']
        umax = self.params['num_trips']
        for v in range(self.params['num_vehicles']):
            for f in range(self.params['num_batches']):
                idx = self._2Dto1D(v, h, ymax, zmax)
                idx1 = self._2Dto1D(v, 1, xmax, umax)
                idx2 = self._2Dto1D(p, f, xmax, ymax)
                idx3 = self._3Dto1D(f, v, 1, ymax, zmax, umax)
                self.A[idx + start, idx1 + st_start] = -1
                self.A[idx + start, idx2 + c_start] = 1
                self.A[idx + start, idx3 + t_stat] = self.params['M']
                self.b[idx + start] = self.params['M'] - \
                    self.params['service_time'][0]


        #"""
        #    Start Next Constraint
        """
        start = end
        end += self.params['num_products'] * self.params['num_vehicles'] * \
            self.params['num_trips'] * self.params['num_batches']
        xmax = self.params['num_products']
        ymax = self.params['num_vehicles']
        zmax = self.params['num_trips']
        umax = self.params['num_batches']
        for p in range(self.params['num_products']):
            for v in range(self.params['num_vehicles']):
                for h in range(self.params['num_trips']):
                    for f in range(self.params['num_batches']):
                        pass
        """
        """
            Time Window Constraint
        """
        start = end
        end += self.params['num_customers'] * self.params['num_vehicles'] * \
            self.params['num_trips']
        xmax = self.params['num_nodes']
        ymax = self.params['num_vehicles']
        zmax = self.params['num_trips']
        e_start = self.indices['e'][0]
        e_end = self.indices['e'][-1]
        l_start = self.indices['l'][0]
        l_end = self.indices['l'][-1]
        for j in range(self.params['num_customers']):
            for v in range(self.params['num_vehicles']):
                for h in range(self.params['num_trips']):
                    idx = self._3Dto1D(j, v, h, xmax, ymax, zmax)
                    idx1 = self._3Dto1D(j + 1, v, h, xmax, ymax, zmax)
                    self.A[idx + start, idx1 + e_start] = -1
                    self.A[idx + start, idx1 + a_start] = - 1
                    self.b[idx + start] = -self.params['time_window'][j + 1][0]

        start = end
        end += self.params['num_customers'] * self.params['num_vehicles'] * \
            self.params['num_trips']
        for j in range(self.params['num_customers']):
            for v in range(self.params['num_vehicles']):
                for h in range(self.params['num_trips']):
                    idx = self._3Dto1D(j, v, h, xmax, ymax, zmax)
                    idx1 = self._3Dto1D(j + 1, v, h, xmax, ymax, zmax)
                    self.A[idx + start, idx1 + l_start] = -1
                    self.A[idx + start, idx1 + a_start] = - 1
                    self.b[idx + start] = -self.params['time_window'][j + 1][1]

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
        end = self.params['num_products']
        self.indices['f'] = list(range(start, end))

        start = end
        end += 1
        self.indices['F'] = list(range(start, end))

        start = end
        end += self.params['num_vehicles'] * self.params['num_trips']
        self.indices['k'] = list(range(start, end))

        start = end
        end += self.params['customers']
        self.indices['a'] = list(range(start, end))

        start = end
        end += self.params['num_customers']
        self.indices['l'] = list(range(start, end))

        start = end
        end += self.params['num_products'] * self.params['num_products']
        self.indices['x'] = list(range(start, end))

        start = end
        end += self.params['num_customers'] * self.params['num_vehicles'] * \
            self.params['num_trips']
        self.indices['y'] = list(range(start, end))

        start = end
        end += self.params['num_customers'] * self.params['num_customers'] * \
            self.params['num_vehicles'] * self.params['num_trips']
        self.indices['z'] = list(range(start, end))
