import random
import pandas as pd
import os
import numpy as np


TRAVEL_TIME = 'travel_time.csv'
VEHICLES = 'vehicles.csv'
VEHICLE_TYPE = 'vehicle_type.csv'
META = 'meta.csv'
LOWER_TIME_LIMIT = 'lower_time_limit.csv'

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
    num_nodes = num_customers + 2
    print('-----------------------')
    print('Number of Products:')
    print(num_products)
    print('-----------------------')
    print('-----------------------')
    print('Number of Customers:')
    print(num_customers)
    print('-----------------------')
    num_trips = int(num_customers / 2) - 1
    num_batches = num_customers
    num_vehicles = len(vehicle_type)
    demand = np.array([
        [
            random.uniform(10, 200) for p in range(num_products)
        ] for i in range(num_nodes)
    ])
    for p in range(num_products):
        demand[0][p] = 0
        demand[num_nodes - 1][p] = 0
    demand = demand.astype(np.int32)

    process_time = np.array([
        random.uniform(1, 5) for p in range(num_products)
    ]).astype(data_type)

    service_time_coef = 0.2
    service_time = service_time_coef * np.sum(demand, -1).astype(data_type)
    service_time[0] = 10
    service_time[num_nodes - 1] = 10
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
    for i in range(num_nodes):
        if i == 0 or i == num_nodes - 1:
            time_windows.append([0, 0])
        else:
            upper =  sum([
                demand[i-1][p]*process_time[p] for p in range(num_products)
            ]) + service_time[i]
            time_windows.append([
                lower[i - 1],
                lower[i - 1] + 10 + upper
            ])
            if upper + lower[i - 1] + 10 > max_up:
                max_up = upper + lower[i - 1] + 10
                index = i
    time_windows[0][1] = max_up + travel_time[0][index] + 10
    time_windows[num_nodes - 1][1] = max_up + travel_time[0][index] + 10
    time_windows = np.array(time_windows).astype(data_type)

    params = {
        'num_customers': num_customers,
        'num_nodes' : num_nodes,
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
        'large_int' : data_type(1e5),
        'pulp_solver' : 'GUROBI',
        'process_cost' : np.random.random((num_products,)),
        'out_path' : 'assets/generated/model3'
    }
    return params


def get_params_v2(data_type, read = True):
    data_path = 'data'
    travel_time = pd.read_csv(
        os.path.join(data_path, TRAVEL_TIME),
        header = None
    ).values.astype(data_type)
    vehicles = pd.read_csv(os.path.join(data_path, VEHICLES))
    vehicle_type_capacity = vehicles['capacity'].values.astype(data_type)
    vehicle_type = pd.read_csv(os.path.join(data_path, VEHICLE_TYPE))
    vehicle_type = vehicle_type['type'].values.astype(int)
    meta = pd.read_csv(os.path.join(data_path, META))
    num_products = int(meta[meta['metric'] == \
        'products'].reset_index()['quantity'][0])
    num_customers = int(meta[meta['metric'] == \
        'customers'].reset_index()['quantity'][0])
    num_nodes = num_customers + 2
    processing_cost = int(meta[meta['metric'] == \
        'processing cost'].reset_index()['quantity'][0])
    hiring_cost = int(meta[meta['metric'] == \
        'hiring cost'].reset_index()['quantity'][0])
    travel_cost = int(meta[meta['metric'] == \
        'travel cost'].reset_index()['quantity'][0])
    penalty = int(meta[meta['metric'] == \
        'penalty'].reset_index()['quantity'][0])
    print('-----------------------')
    print('Number of Products:')
    print(num_products)
    print('-----------------------')
    print('-----------------------')
    print('Number of Customers:')
    print(num_customers)
    print('-----------------------')
    num_trips = int(num_customers / 2) - 1
    num_batches = num_customers
    num_vehicles = len(vehicle_type)
    
    demand = np.array([
        [
            random.uniform(3, 10) for p in range(num_products)
        ] for i in range(num_nodes)
    ])
    for p in range(num_products):
        demand[0][p] = 0
        demand[num_nodes - 1][p] = 0
    demand = demand.astype(np.int32)

    unloading_time = np.sum(demand, axis = -1) * 0.2

    process_time = np.array([
        random.uniform(1, 3) for p in range(num_products)
    ]).astype(data_type)

    setup_time = np.array([
        [
            random.uniform(1,5) for p in range(num_products)
        ] for q in range(num_products + 1)
    ], dtype = np.int32)
    for p in range(num_products):
        for q in range(num_products):
            if p == q:
                setup_time[p + 1][q] = 0

    demand_info = pd.read_csv(os.path.join(data_path, 'demand_loading_time.csv'))
    products = ['P'+str(i+1) for i in range(num_products)]
    if read:
        demand = demand_info[products].values
        unloading_time = demand_info['Unloading Time'].values
    loading_time = demand_info['Loading Time'].values

    time_windows = pd.read_csv(os.path.join(data_path, 'time_windows.csv'))
    time_windows = time_windows[['A', 'B']].values

    params = { 
        'num_customers': num_customers,
        'num_nodes' : num_nodes,
        'num_trips' : num_trips,
        'num_batches' : num_batches,
        'num_products': num_products,
        'demand': demand,
        'setup_time': setup_time,
        'process_time': process_time,
        'travel_time': travel_time,
        'time_windows': time_windows,
        'num_vehicles': num_vehicles,
        'vehicle_capacity': np.array(
            [vehicle_type_capacity[t] for t in vehicle_type]
        ),  
        'service_time': unloading_time,
        'processing_cost': processing_cost,
        'setup_cost': hiring_cost, 
        'travel_cost': travel_cost, 
        'penalty': penalty,
        'early_delivery_penalty': 2,
        'late_delivery_penalty': 4,
        'vehicle_cost': travel_cost,
        'vehicle_type': vehicle_type,
        'M': data_type(1e4),
        'large_int' : data_type(1e5),
        'pulp_solver' : 'GUROBI',
        'out_path' : 'assets/generated/model3'
    }   
    return params

