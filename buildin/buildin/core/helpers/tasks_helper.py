from datetime import datetime


def calculate_days_to_deadline(deadline_date):
    if deadline_date:
        time_delta = deadline_date - datetime.now().date()
        if time_delta.days < 0:
            return "The project must be finished yet!"
        return f'{time_delta.days} days'
    else:
        return "No deadline set to the project!"


def calculate_total_time_of_tasks(tasks):
    total_time = 0
    if tasks:
        total_time = sum([task.time_estimation for task in tasks])
    return total_time
