import numpy as np

num_customers = 3
num_products = 3
num_vehicles = num_customers
num_trips = num_customers
demand = None

# Control Parameters for Data Generation
rho = 10
mu = 2
lmbda = 3

# Variable Initialisation
processing_time = np.random.uniform(low = 0, high = rho, size = (num_products,))
demand = np.stack([
    np.random.uniform(
        low = 0,
        high = processing_time[p],
        size = (num_customers,)
    ) for p in range(num_products)
], 1)

min_vehicle_capacity = np.sum(demand, 1).max()
vehicle_capacity = min_vehicle_capacity + np.random.uniform(
    low = 0,
    high = mu * min_vehicle_capacity,
    size = (num_vehicles,)
)
service_time = np.random.uniform(
    low = 1,
    high = lmbda * rho,
    size = (num_customers + 1,)
)

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

}
