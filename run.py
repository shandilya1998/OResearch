import src
import pickle
import os


output_path = 'outputs'

"""
    Next run experiments to compare Linear Programming solver and MIP
    solver
"""
#"""
params = None
model = 'MILP'
if model == 'CPSAT':
    params = src.constants.get_params(int)
elif model == 'MILP':
    params = src.constants.get_params(int)

solver = src.run(
    params,
    model
)
#"""

"""
    numpy model test
"""
"""
params = src.constants.get_params(int)
model = src.models.model.MIPModel(params)
model.build()
"""
