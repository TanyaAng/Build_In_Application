from datetime import datetime


def calculate_days_to_deadline(deadline_date):
    if deadline_date:
        time_delta = deadline_date - datetime.now().date()
        if time_delta.days < 0:
            return "THE PROJECT MUST BE FINISHED YET"
        return f'{time_delta.days} days'
    else:
        return "NO DEADLINE SET TO THE PROJECT!"


def calculate_total_time_of_tasks(tasks):
    total_time = 0
    if tasks:
        total_time = sum([task.time_estimation for task in tasks])
    return total_time
