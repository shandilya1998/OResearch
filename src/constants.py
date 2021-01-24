import random
import pandas as pd
import os

data_path = 'data'
travel_time = pd.read_csv(
    os.path.join(data_path, 'travel_time.csv'),
    header = None
).values.tolist()
vehicles = pd.read_csv(os.path.join(data_path, 'vehicles.csv'))
vehicle_type_cost = vehicles['cost'].values.tolist()
vehicle_type_capacity = vehicles['capacity'].values.tolist()
vehicle_type = pd.read_csv(os.path.join(data_path, 'vehicle_type.csv'))
vehicle_type = vehicle_type['type'].values.tolist()
meta = pd.read_csv(os.path.join(data_path, 'meta.csv'))

num_products = meta['products'][0] #random.randint(0, 5)
num_customers = meta['customers'][0]
print('-------------------')
print('Number of Products:')
print(num_products)
print('-------------------')
print('-------------------')
print('Number of Customers:')
print(num_customers)
print('-------------------')
num_trips = num_customers
num_batches = num_customers
num_vehicle_types = len(vehicle_type_cost) # random.randint(0, 8)
num_vehicles = len(vehicle_type)
demand = [
    [
        int(random.uniform(10, 50)) for j in range(num_customers)
    ] for i in range(num_products)
]

process_time = [
    int(random.uniform(1, 5)) for i in range(num_products)
]

service_time = [
    int(random.uniform(1, 30)) \
    if j != 0 or j == num_customers + 1 \
    else 0 \
    for j in range(num_customers + 2)
]

lower = pd.read_csv(
    os.path.join(
        data_path, 
        'lower_time_limit.csv'
    )
)['lower_limit'].values.tolist()
time_windows = []
upper = 0
max_up = 0
index = 0
for i in range(num_customers + 2):
    if i == 0 or num_customers + 1:
        time_windows.append([0, 0])
    else:
        upper =  sum([
            demand[p][i-1]*process_time[p] for p in range(num_products)
        ]) + service_time[i]
        time_windows.append([
            lower[i - 1],
            lower[i - 1] + 10 + upper
        ])
        if upper > max_up:
            max_up = upper
            index = i

time_windows[0][1] = max_up + travel_time[0][index] + 10
time_windows[num_customers + 1][1] = max_up + travel_time[0][index] + 10

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
    'process_time': process_time,
    'travel_time': travel_time,
    'time_windows': time_windows,
    'num_vehicles': num_vehicles,
    'vehicle_capacity': [vehicle_type_capacity[t] for t in vehicle_type],
    'service_time': service_time,
    'processing_cost': 5,
    'setup_cost': 10,
    'travel_cost': 15,
    'early_delivery_penalty': 2,
    'late_delivery_penalty': 4,
    'vehicle_cost': [vehicle_type_cost[t] for t in vehicle_type],
    'vehicle_type': vehicle_type,
    'M': 1e4,
}
