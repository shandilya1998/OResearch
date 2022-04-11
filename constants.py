import numpy as np

num_customers = 7
num_products = 2
num_vehicles = num_customers
num_trips = num_customers // 3
demand = None

# Control Parameters for Data Generation
rho = 100
mu = 1
lmbda = 0.2
delta1 = 0.5
delta2 = 0.5

# Variable Initialisation
processing_time = np.random.randint(low = 1, high = rho / num_products, size = (num_customers, num_products,))
demand = np.random.randint(low = np.zeros_like(processing_time), high = processing_time)

min_vehicle_capacity = np.sum(demand, 1).max()
vehicle_capacity = min_vehicle_capacity + np.random.randint(
    low = 0,
    high = mu * min_vehicle_capacity,
    size = (num_vehicles,)
)
service_time = np.random.randint(
    low = 1,
    high = lmbda * rho,
    size = (num_customers + 1,)
)

f = np.sum(
    processing_time * demand, 0
)

setup_time = np.random.randint(
    low = 0,
    high = rho,
    size = (num_products, num_products)
)

seq = np.random.choice(
    np.arange(
        0, num_products
    ), size = (num_products, ), replace = False
)

x = np.zeros((num_products, num_products))
for i in range(1, num_products):
    index = seq[i - 1: i + 1]
    x[index[0]][index[1]] = 1

F = np.sum(f) + np.sum(setup_time * x)

travel_time = np.random.randint(
    low = 1,
    high = rho * num_vehicles,
    size = (num_customers + 1, num_customers + 1)
)

for i in range(num_customers + 1):
    travel_time[i][i] = 0
    for j in range(i):
        travel_time[j][i] = travel_time[i][j]
travel_time = travel_time.T

lower_time_window = np.random.randint(
    low = 0,
    high = np.floor(delta1 * rho * num_customers / (1 + num_vehicles)),
    size = (num_customers,)
) + np.sum(demand * processing_time, 1) + travel_time[0, 1:] + service_time[0]

upper_time_window = np.random.randint(
    low = 1,
    high = np.floor(delta2 * rho),
    size = (num_customers,)
) + lower_time_window

time_window = np.stack([lower_time_window, upper_time_window], 0)

# Data Wrapping
params = {
    'num_customers'                     : num_customers,
    'num_vehicles'                      : num_vehicles,
    'num_trips'                         : num_trips,
    'num_products'                      : num_products,
    'M'                                 : int(1e6),
    'demand'                            : demand,
    'vehicle_capacity'                  : vehicle_capacity,
    'service_time'                      : service_time,
    'F'                                 : F,
    'travel_time'                       : travel_time,
    'time_window'                       : time_window,
    'c1'                                : 1,
    'c2'                                : 1,
    'c3'                                : 1,
}
