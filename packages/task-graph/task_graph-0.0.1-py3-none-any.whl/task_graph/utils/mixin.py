from task_graph import TaskGraph


class TaskGraphMixin:
    def __init__(self):
        self.graph: TaskGraph = TaskGraph()

    def task(self, func):
        def wrapper(self_, *args, **kwargs):
            self.graph.add_task(func)(self, *args, **kwargs)
# TODO: implement