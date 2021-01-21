import src
import pickle
import os

output_path = 'outputs'

solution = src.run(
    src.constants.params
)

pkl = open(os.path.join(output_path, 'test.pickle'), 'wb')
pickle.dump(solution, pkl)
pkl.close()
