This repo uses both python2 and python3.
Thus there is a need for 2 virtual environments to successfully execute all programs.

To run the MILP solver, open an interactive python shell at the root directory of the repository and execute the following code

```
from run import *
solver.get_solution_as_excel('outputs')
```

In the 'outputs' folder excel files will be created.
The first variable in the excel file name is along the rows and the second variable is along the columns

If a variable has more than 2 dimensions, then the additional dimensions are stored in addidional worksheets
