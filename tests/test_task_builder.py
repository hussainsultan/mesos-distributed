import unittest

from mesos.interface import mesos_pb2

from expects import expect, equal
from framework.task_builder import TaskDirector, WorkerTask, CenterTask
from mock import MagicMock


class TestTaskDirector(unittest.TestCase):
    def test_create_task_configures_resources_with_offers(self):
        offer = MagicMock()
        offer.url.address.ip = 'localhost'
        offer.slave_id = MagicMock()
        offer.slave_id.value = 'slave-id'

        mesos_task = TaskDirector(offer,WorkerTask).make_task_with_id('task-id')

        expect(mesos_task.slave_id.value).to(equal('slave-id'))
        expect(mesos_task.task_id.value).to(equal('task-id'))
        expect(len(mesos_task.resources)).to(equal(2))

        expect(mesos_task.resources[0].name).to(equal('cpus'))
        expect(mesos_task.resources[0].type).to(equal(mesos_pb2.Value.SCALAR))
        expect(mesos_task.resources[0].scalar.value).to(equal(1))

        expect(mesos_task.resources[1].name).to(equal('mem'))
        expect(mesos_task.resources[1].type).to(equal(mesos_pb2.Value.SCALAR))
        expect(mesos_task.resources[1].scalar.value).to(equal(1000))

    def test_task_has_command_to_launch_dworkers(self):
        offer = MagicMock()
        offer.url.address.ip = 'localhost'
        offer.slave_id = MagicMock()
        offer.slave_id.value = 'slave-id'

        mesos_task = TaskDirector(offer,WorkerTask).make_task_with_id('task-id')

        expect(mesos_task.command.value).to(equal('dworker localhost:8787'))

    def test_task_has_command_to_launch_dcenter(self):
        offer = MagicMock()
        offer.hostname = 'localhost'
        offer.slave_id = MagicMock()
        offer.slave_id.value = 'slave-id'

        mesos_task = TaskDirector(offer,CenterTask).make_task_with_id('task-id')

        expect(mesos_task.command.value).to(equal('dcenter'))
