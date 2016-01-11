import uuid

from mesos.interface import Scheduler

from framework.task_builder import TaskDirector, SchedulerTask, WorkerTask


class DistributedScheduler(Scheduler):
    def __init__(self, task_director=TaskDirector, id_generator=uuid.uuid4):
        self.id_generator = id_generator
        self.task_director = task_director
        self.started_dcenter = 0
        self.started_dworker = 0

    def resourceOffers(self, driver, offers):
        tasks = []

        for offer in offers:

            if self.started_dcenter and self.started_dworker:
                driver.declineOffer(offer.id)

            if self.started_dcenter == 0:
                self.started_dcenter += 1
                id = str(self.id_generator())
                task = self.task_director(offer, SchedulerTask).make_task_with_id(id)
                tasks.append(task)

            if self.started_dworker == 0:
                self.started_dworker += 1
                id = str(self.id_generator())
                task = self.task_director(offer, WorkerTask).make_task_with_id(id)
                tasks.append(task)
                driver.launchTasks(offer.id, tasks)
