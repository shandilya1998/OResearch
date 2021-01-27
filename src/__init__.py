from src import model, constants

def run(
    params,
    solver = 'MILP'
):
    if solver == 'MILP' or solver == 'LP':
        print('Running model')
        solver = model.Model(
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
        solver = model.CPSATModel(
            params
        )
        solver.build()
        status = solver.solve()
        print(status)
        return solver

if __name__ == '__main__':
    run(
        constants.params
    )   
