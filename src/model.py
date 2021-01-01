import ortools
from ortools.linear_solver import pywraplp

class MILP:
    def __init__(self):
        self.solver = pywraplp.Solver.CreateSolver('SCIP')
        
    def set_variables(self):
        raise NotImplementedError

    def set_constraints(self):
        raise NotImplementedError

    def set_objective(self):
        raise NotImplementedError

    def solve(self):
        status = solver.Solve()
        return status
