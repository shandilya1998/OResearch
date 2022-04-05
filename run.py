from src.model import MVRPModel
from constants import params

# Initialise MVRPModel
model = MVRPModel(params=params)

# Solve Problem
model.solve()
