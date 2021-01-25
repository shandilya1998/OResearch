from src import model, constants

def run(
    params,
    solver = None
):
    print('Running MIP model')
    milp = model.MILP(
        params,
        solver
    )   
    milp.build()
    print('-------------------')
    print('Number of Variables:')
    print(milp.num_variables())
    print('-------------------')
    status = milp.solve()
    print('Solver Status')
    print(status)
    return milp.get_solution(), milp

if __name__ == '__main__':
    run(
        constants.params
    )   
