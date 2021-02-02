import random
import pandas as pd
import os
import numpy as np


TRAVEL_TIME = 'travel_time_full.csv'
VEHICLES = 'vehicles.csv'
VEHICLE_TYPE = 'vehicle_type.csv'
META = 'meta_full.csv'
LOWER_TIME_LIMIT = 'lower_time_limit_full.csv'

def get_params(data_type):
    data_path = 'data'
    travel_time = pd.read_csv(
        os.path.join(data_path, TRAVEL_TIME),
        header = None
    ).values.astype(data_type)
    vehicles = pd.read_csv(os.path.join(data_path, VEHICLES))
    vehicle_type_cost = vehicles['cost'].values.astype(data_type)
    vehicle_type_capacity = vehicles['capacity'].values.astype(data_type)
    vehicle_type = pd.read_csv(os.path.join(data_path, VEHICLE_TYPE))
    vehicle_type = vehicle_type['type'].values.astype(int)
    meta = pd.read_csv(os.path.join(data_path, META))

    num_products = meta['products'][0] #random.randint(0, 5)
    num_customers = meta['customers'][0]
    print('---------------------')
    print('Number of Products:')
    print(num_products)
    print('---------------------')
    print('---------------------')
    print('Number of Customers:')
    print(num_customers)
    print('---------------------')
    num_trips = num_customers
    num_batches = num_customers
    num_vehicle_types = len(vehicle_type_cost) # random.randint(0, 8)
    num_vehicles = len(vehicle_type)
    demand = np.array([
        [
            random.uniform(10, 200) for p in range(num_products)
        ] for i in range(num_customers + 2)
    ])
    for p in range(num_products):
        demand[0][p] = 0
        demand[num_customers + 1] = 0
    demand = demand.astype(np.int32)

    process_time = np.array([
        random.uniform(1, 5) for p in range(num_products)
    ]).astype(data_type)

    service_time_coef = 0.2
    service_time = service_time_coef * np.sum(demand, -1).astype(data_type)
    service_time[0] = 10
    service_time[num_customers + 1] = 10
    service_time = service_time.astype(data_type)

    lower = pd.read_csv(
        os.path.join(
            data_path,
            LOWER_TIME_LIMIT
        )
    )['lower_limit'].values.astype(data_type)
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
    time_windows = np.array(time_windows).astype(data_type)

    params = {
        'num_customers': num_customers,
        'num_trips' : num_trips,
        'num_batches' : num_batches,
        'num_products': num_products,
        'demand': demand,
        'setup_time': np.array([
            [
                random.uniform(1, 10) for q in range(num_products)
            ] for p in range(num_products)
        ]).astype(data_type),
        'process_time': process_time,
        'travel_time': travel_time,
        'time_windows': time_windows,
        'num_vehicles': num_vehicles,
        'vehicle_capacity': np.array(
            [vehicle_type_capacity[t] for t in vehicle_type]
        ),
        'service_time': service_time,
        'processing_cost': 5,
        'setup_cost': 10,
        'travel_cost': 15,
        'early_delivery_penalty': 2,
        'late_delivery_penalty': 4,
        'vehicle_cost': np.array(
            [vehicle_type_cost[t] for t in vehicle_type]
        ),
        'vehicle_type': vehicle_type,
        'M': data_type(1e4),
        'large_int' : data_type(1e5)
    }
    return params
