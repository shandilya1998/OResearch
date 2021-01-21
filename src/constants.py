import random
import pandas as pd
import os

data_path = 'data'
travel_time = pd.read_csv(
    os.path.join(data_path, 'travel_time.csv'),
    header = None
)
vehicles = pd.read_csv(os.path.join(output_path, 'vehicles.csv'))
vehicle_type_cost = vehicles['cost'].values.tolist()
vehivle_type_capacity = vehicles['capacity'].values.tolist()
vehicle_type = pd.read_csv(os.path.join(data_path, 'travel_type.csv'))
vehicle_type = vehicle_type['type'].values.tolist()
meta = pd.read_csv(os.path.join(data_path, 'meta.csv'))

num_products = meta['products'][0] #random.randint(0, 5)
num_customers = meta['customers'][0]
num_trips = num_customers
num_batches = num_customers
num_vehicle_types = len(vehicle_type_cost) # random.randint(0, 8)
num_vehicles = len(vehicle_type)
demand = [
    [
        int(random.uniform(10, 50)) for j in range(num_customers)
    ] for i in range(num_products)
]

def get_time_window():
    ub = int(random.uniform(0, 50))
    lb = int(random.uniform(0, ub))
    if lb != ub:
        return [lb, ub]
    else:
        return get_time_window()


params = {
    'num_customers': num_customers,
    'num_trips' : num_trips,
    'num_batches' : num_batches,
    'num_products': num_products,
    'demand': demand,
    'setup_time': [
        [
            int(random.uniform(1, 10)) for j in range(num_products)
        ] for i in range(num_products)
    ],
    'process_time': [
        int(random.uniform(1, 5)) for i in range(num_products)
    ],
    'travel_time': travel_time.reset_index().values.tolist(),
    'time_windows': [
        get_time_window() for j in range(num_customers + 2)
    ],
    'num_vehicles': num_vehicles,
    'vehicle_capacity': [vehicle_type_capacity[t] for t in vehicle_type],
    'service_time': [
        int(random.uniform(1, 30)) for j in range(num_customers + 2)
    ],
    'processing_cost': 5,
    'setup_cost': 10,
    'travel_cost': 15),
    'early_delivery_penalty': 2,
    'late_delivery_penalty': 4,
    'vehicle_cost': [vehicle_type_cost[t] for t in vehicle_type],
    'vehicle_type': vehicle_type,
    'M': 1e10,
}
