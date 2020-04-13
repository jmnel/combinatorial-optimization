from __future__ import annotations
from typing import List


class Task:

    next_id: int = 0
    all_tasks: List[Task, ...] = list()

    def __init__(self,
                 description: str,
                 duration: int,
                 predecessors: List[int, ...],
                 max_reduct: int,
                 cost_per_week: float):

        self.id = Task.next_id
        Task.next_id += 1

        Task.all_tasks.append(self)

        self.description = description
        self.duration = duration
        self.predecessors = predecessors
        self.max_reduct = max_reduct
        self.cost_per_week = cost_per_week

    def get_task_num(self):
        return self.id

    def __str__(self):
        return 'Task {:<2} : {}'.format(
            self.get_task_num(), self.description)

    def all():
        return Task.all_tasks
