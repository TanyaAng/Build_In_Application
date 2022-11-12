def calculate_total_time_of_project(tasks):
    total_time = 0
    if tasks:
        total_time = sum([task.time_estimation for task in tasks])
    return total_time
