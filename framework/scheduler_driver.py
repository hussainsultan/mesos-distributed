from mesos.interface import mesos_pb2
from mesos.native import MesosSchedulerDriver


class DistributedDriver(object):
    def __init__(self, driver=MesosSchedulerDriver, framework=mesos_pb2.FrameworkInfo()):
        self.mesos_scheduler_driver = driver
        self.framework = framework
        self.framework.user = ""
        self.framework.name = 'distributed-framework'

    def create_driver(self, scheduler):
        return self.mesos_scheduler_driver(scheduler(), self.framework, '172.17.0.4:5050')
