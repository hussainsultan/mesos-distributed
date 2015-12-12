import unittest
import uuid

from mesos.interface import Scheduler

from expects import expect, equal
from framework.task_builder import TaskDirector, CenterTask, WorkerTask
from mock import MagicMock, call
from framework.distributed_scheduler import DistributedScheduler


class TestDistributedScheduler(unittest.TestCase):
    def test_implements_mesos_scheduler_interface(self):
        expect(DistributedScheduler.__bases__[0]).to(equal(Scheduler))

    def test_kicks_off_dcenter_and_dworker_processes_on_offer_once(self):
        driver = MagicMock()

        offer = MagicMock()
        offer.hostname = 'localhost'
        offer.slave_id = MagicMock()
        offer.slave_id.value = 'slave-id'
        offer.id = 1

        offers = [offer for x in range(9)]

        task_director = MagicMock(spec=TaskDirector)
        task_director().make_task_with_id.return_value = 'task'
        task_director.reset_mock()

        id1 = uuid.uuid4()
        id2 = uuid.uuid4()
        id_generator = iter([id1, id2]).next

        DistributedScheduler(task_director, id_generator).resourceOffers(driver, offers)

        expect(task_director.call_args_list).to(equal([call(offer, CenterTask),
                                                       call(offer, WorkerTask)]))
        expect(task_director().make_task_with_id.call_args_list).to(equal([call(str(id1)),
                                                                           call(str(id2))]))
        driver.launchTasks.assert_called_with(1, ['task', 'task'])
