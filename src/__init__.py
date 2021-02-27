from src import models, constants

def run(
    params,
    solver = 'MILP'
):
    if solver == 'MILP' or solver == 'LP':
        print('Running model')
        solver = models.Model(
            params,
            solver
        )
        solver.build()
        print('---------------------')
        print('Number of Variables:')
        print(solver.num_variables())
        print('---------------------')
        status = solver.solve()
        print('Solver Status')
        print(status)
        return solver

    elif solver == 'CPSAT':
        print('Running Model')
        solver = models.CPSATModel(
            params
        )
        solver.build()
        status = solver.solve()
        print(status)
        return solver

    elif solver == 'PULP':
        print('Running Model')
        solver = models.PuLPModel(
            params
        )
        solver.build()
        solver.solve()
        return solver

if __name__ == '__main__':
    run(
        constants.params
    )
