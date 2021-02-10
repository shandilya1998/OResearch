import src
import pickle
import os


output_path = 'outputs'

"""
    Next run experiments to compare Linear Programming solver and MIP
    solver
"""
"""
params = None
model = 'LP'
if model == 'CPSAT':
    params = src.constants.get_params(int)
elif model == 'MILP' or model == 'LP':
    params = src.constants.get_params(float)

solver = src.run(
    params,
    model
)
"""

"""
    numpy model test
"""
params = src.constants.get_params(int)
model = src.models.model.MIPModel(params)
model.build()
