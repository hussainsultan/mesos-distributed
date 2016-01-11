import unittest

from expects import expect, equal, be
from framework.task import Task


class TestTask(unittest.TestCase):
    MESOS_DOCKER_NETWORK_BRIDGE = 2

    def test_task(self):
        mesos_task = Task('id','name''slave-id').task

        expect(mesos_task.task_id.value).to(equal('id'))
        expect(mesos_task.slave_id.value).to(equal('slave-id'))
        expect(mesos_task.name).to(equal('name'))


    def test_configures_container_information_protobuf(self):

        mesos_task = Task('id','name''slave-id').configure_container_protobuf()
        container_protobuf = mesos_task.task.container


        expect(container_protobuf.docker.image).to(equal('hussainsultan/dcenter'))
        expect(container_protobuf.docker.network).to(equal(self.MESOS_DOCKER_NETWORK_BRIDGE))
        expect(container_protobuf.docker.force_pull_image).to(be(True))

        expect(container_protobuf.docker.port_mappings[0].host_port).to(equal(33001))
        expect(container_protobuf.docker.port_mappings[0].container_port).to(equal(8787))

    def test_configure_memory_resources(self):
        mesos_task = Task('id','name''slave-id').configure_memory_resources().task

        expect(mesos_task.resources[0].name).to(equal('mem'))
        expect(mesos_task.resources[0].scalar.value).to(equal(128))

    def test_configure_cpu_resources(self):
        mesos_task = Task('id','name''slave-id').configure_cpu_resources().task

        expect(mesos_task.resources[0].name).to(equal('cpus'))
        expect(mesos_task.resources[0].scalar.value).to(equal(2))

    def test_configure_command_protobuf(self):
        mesos_task = Task('id','name''slave-id').configure_command_protobuf('sleep 30').task

        expect(mesos_task.command.value).to(equal('sleep 30'))




