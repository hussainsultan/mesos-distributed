import unittest

from mesos.interface import mesos_pb2
from mesos.native import MesosSchedulerDriver

from expects import expect, equal
from framework.scheduler_driver import DistributedDriver
from framework.distributed_scheduler import DistributedScheduler
from mock import MagicMock, call


class TestSchedulerDriver(unittest.TestCase):
    def test_create_mesos_scheduler_driver_framework(self):
        framework = MagicMock(spec=mesos_pb2.FrameworkInfo)
        driver = MagicMock(spec=MesosSchedulerDriver)
        scheduler = MagicMock(spec=DistributedScheduler)

        mesos_master_uri = '127.0.0.1:5050'

        DistributedDriver(driver, framework).create_driver(scheduler)

        expect(framework.user).to(equal(""))
        expect(framework.name).to(equal('distributed-framework'))
        expect(driver.call_args_list).to(equal([call(framework, scheduler(), mesos_master_uri)]))
