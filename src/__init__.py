from src import model, constants

def run(
    params
):
    milp = model.MILP(
        params
    )   
    milp.build()
    print('-------------------')
    print('Number of Variables:')
    print(milp.num_variables())
    print('-------------------')
    status = milp.solve()
    print('Solver Status')
    print(status)
    return milp.get_solution()

if __name__ == '__main__':
    run(
        constants.params
    )   
