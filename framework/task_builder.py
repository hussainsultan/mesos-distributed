from mesos.interface import mesos_pb2

from framework.task import Task


class TaskDirector(object):
    def __init__(self, offer, builder):
        self.builder = builder(offer.slave_id.value, offer.url.address.ip)
        print offer

    def make_task_with_id(self, id):
        self.builder.add_resources_configurations(id)
        return self.builder.task.task


class WorkerTask(object):
    def __init__(self, slave_id, slave_ip):
        self.task = mesos_pb2.TaskInfo()
        self.slave_id = slave_id
        self.slave_ip = slave_ip

    def add_resources_configurations(self, id):
        self.task = Task(id,'dwoker', self.slave_id)
        #TODO: add config for test environment vs production evs for worker uri
        self.task.configure_command_protobuf('dworker 192.168.99.100:33001'.format(self.slave_ip))
        self.task.configure_container_protobuf()
        self.task.configure_cpu_resources()
        self.task.configure_memory_resources()


class SchedulerTask(object):
    def __init__(self, slave_id, slave_ip):
        self.task = mesos_pb2.TaskInfo()
        self.slave_id = slave_id

    def add_resources_configurations(self, id):
        self.task = Task(id,'dscheduler', self.slave_id)
        self.task.configure_command_protobuf('dscheduler')

        self.task.configure_memory_resources()
        self.task.configure_container_protobuf(expose_ports=True)
        self.task.configure_port_resources()
        self.task.configure_cpu_resources()

