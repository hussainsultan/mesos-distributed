import unittest
import time

from distributed import Executor
from expects import expect, equal
from framework.distributed_scheduler import DistributedScheduler
from framework.scheduler_driver import DistributedDriver
from system_tests.matchers.framework_matchers import have_activated_slaves, have_framework_name
from system_tests.support.mesos_cluster import MesosCluster


class TestSystem(unittest.TestCase):
    def test_framework_runs(self):
        with MesosCluster() as cluster:
            time.sleep(2)
            driver = DistributedDriver().create_driver(DistributedScheduler)
            driver.start()
            time.sleep(5)

            expect(cluster).to(have_activated_slaves(1))
            expect(cluster).to(have_framework_name('distributed-framework'))

            # distributed test - this probably doesnt belong here
            executor = Executor('127.0.0.1:8787')
            A = executor.map(lambda x: x**2, range(10))
            B = executor.map(lambda x: -x, A)
            total = executor.submit(sum, B)
            expect(total.result()).to(equal(-285))
            driver.stop()
