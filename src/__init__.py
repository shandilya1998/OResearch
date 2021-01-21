from src import model, constants

def run(
    params
):
    milp = model.MILP(
        params
    )   
    milp.build()
    status = milp.solve()
    print('Solver Status')
    print(status)
    return milp.get_solution()

if __name__ == '__main__':
    run(
        constants.params
    )   
