import unittest
import uuid

from mesos.interface import Scheduler

from expects import expect, equal, be
from framework.task_builder import TaskDirector, SchedulerTask, WorkerTask
from mock import MagicMock, call
from framework.distributed_scheduler import DistributedScheduler


class TestDistributedScheduler(unittest.TestCase):

    def setUp(self):
        self.driver = MagicMock()

        offer = MagicMock()
        offer.hostname = 'localhost'
        offer.slave_id = MagicMock()
        offer.slave_id.value = 'slave-id'
        offer.id = 1

        self.offers = [offer for x in range(9)]

        self.id1 = uuid.uuid4()
        self.id2 = uuid.uuid4()
        self.id_generator = iter([self.id1, self.id2]).next

    def test_implements_mesos_scheduler_interface(self):
        expect(DistributedScheduler.__bases__[0]).to(equal(Scheduler))

    def test_kicks_off_dcenter_and_dworker_processes_on_offer_once(self):

        task_director = MagicMock(spec=TaskDirector)
        task_director().make_task_with_id.return_value = 'task'
        task_director.reset_mock()



        DistributedScheduler(task_director, self.id_generator).resourceOffers(self.driver, self.offers)

        expect(task_director.call_args_list).to(equal([call(self.offers[0], SchedulerTask),
                                                       call(self.offers[0], WorkerTask)]))
        expect(task_director().make_task_with_id.call_args_list).to(equal([call(str(self.id1)),
                                                                           call(str(self.id2))]))
        self.driver.launchTasks.assert_called_with(1, ['task', 'task'])

    def test_declines_offers_if_dscheduler_and_worker_are_already_running(self):
        task_director = MagicMock(spec=TaskDirector)
        task_director().make_task_with_id.return_value = 'task'
        task_director.reset_mock()

        scheduler = DistributedScheduler(task_director, self.id_generator)
        scheduler.started_dcenter=1
        scheduler.started_dworker=1

        scheduler.resourceOffers(self.driver, self.offers)

        expect(self.driver.declineOffer.called).to(be(True))
        self.driver.declineOffer.assert_called_with(1)


