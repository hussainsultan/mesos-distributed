from mesos.interface import mesos_pb2

from framework.support import configure_resources_for_a_task


class TaskDirector(object):
    def __init__(self, offer, builder):
        self.builder = builder(offer.slave_id.value, offer.url.address.ip)

    def make_task_with_id(self, id):
        self.builder.add_resources(id)
        self.builder.add_commands()
        return self.builder.task


class WorkerTask(object):
    def __init__(self, slave_id, slave_ip):
        self.task = mesos_pb2.TaskInfo()
        self.slave_id = slave_id
        self.slave_ip = slave_ip

    def add_resources(self, id):
        self.task = configure_resources_for_a_task(id, self.task, self.slave_id)

    def add_commands(self):
        self.task.command.value = 'dworker {0}:8787'.format(self.slave_ip)


class CenterTask(object):
    def __init__(self, slave_id, slave_ip):
        self.task = mesos_pb2.TaskInfo()
        self.slave_id = slave_id

    def add_resources(self, id):
        self.task = configure_resources_for_a_task(id, self.task, self.slave_id)

    def add_commands(self):
        self.task.command.value = 'dcenter'
