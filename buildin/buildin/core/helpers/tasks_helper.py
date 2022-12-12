from datetime import datetime
import numpy as np

from buildin.core.repository.task_repository import check_if_task_is_approved, get_task_time_estimation


def calculate_days_to_deadline(deadline_date):
    if deadline_date:
        today = datetime.now().date()
        working_days = np.busday_count(today, deadline_date) + 1
        if working_days < 0:
            return "The project must be finished yet!"
        return f'{working_days} days'
    else:
        return "No deadline set to the project!"


def calculate_total_time_of_tasks(tasks):
    total_time = 0
    if tasks:
        total_time = sum([get_task_time_estimation(task) for task in tasks if task.time_estimation])
    return total_time
