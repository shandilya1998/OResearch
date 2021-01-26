import src
import pickle
import os

output_path = 'outputs'

"""
    Next run experiments to compare Linear Programming solver and MIP
    solver
"""

milp = src.run(
    src.constants.params
)
