from datetime import datetime


def calculate_days_to_deadline(deadline_date):
    time_delta = deadline_date - datetime.now().date()
    if time_delta.days < 0:
        return "THE PROJECT MUST BE FINISHED YET"
    return f'{time_delta.days} days'


def calculate_total_time_of_project(tasks):
    total_time = 0
    if tasks:
        total_time = sum([task.time_estimation for task in tasks])
    return total_time
