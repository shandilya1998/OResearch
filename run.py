import src
import pickle
import os

output_path = 'outputs'

"""
    Next run experiments to compare Linear Programming solver and MIP
    solver
"""
params = None
model = 'MILP'
if model == 'CPSAT':
    params = src.constants.get_params(int)
elif model == 'MILP' or model == 'LP':
    params = src.constants.get_params(float)

solver = src.run(
    params,
    model
)
