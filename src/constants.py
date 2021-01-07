import random

num_products  = random.randint(0, 15)
num_customers = 100
num_vehicle_types = random.randint(0, 30)
num_vehicles = random.randint(num_vehicle_types, 40)

demand = [ 
    [   
        int(random.uniform(10, 50)) for j in range(num_customers) 
    ] for i in range(num_products)
] 

def get_random_time_window():
    ub = int(random.uniform(0, 1000))
    lb = int(random.uniform(0, ub))
    if lb != ub:
        return [lb, ub]
    else:
        return get_random_time_window() 

params = {
    'num_customers' : num_customers,
    'num_products' : num_products,
    'demand' : demand,
    'setup_time' : [
        [
            int(random.uniform(1, 10)) for j in range(num_products)
        ] for i in range(num_products)
    ],
    'process_time' : [
        int(random.uniform(1, 5)) for i in range(num_products)
    ],
    'travel_time' : [
        [
            int(random.uniform(1, 30)) for j in range(num_customers)
        ] for i in range(num_customers)
    ],
    'time_windows' : [
        get_random_time_window for j in range(num_customers)
    ],
    'num_vehicles' : num_vehicles,
    'vehicle_capacity' : [
        int(random.uniform(50, 250)) for i in range(num_vehicles)
    ],
    'service_time' : [
        int(random.uniform(1, 30)) for j in range(num_customers)
    ],
    'processing_cost' : int(random.uniform(1, 50)),
    'setup_cost' : int(random.uniform(1, 50)),
    'travel_cost' : int(random.uniform(1,50)),
    'early_delivery_penalty' : int(random.uniform(1, 50)),
    'late_delivery_penalty' : int(random.uniform(1, 50)),
    'vehicle_cost' : [
        int(random.uniform(1, 50)) for i in range(num_vehicle_types)
    ],
    'vehicle_type' : [
        random.randint(0, num_vehicle_types) for i in range(num_vehicles)
    ],
    'M' : 1e10,
}
