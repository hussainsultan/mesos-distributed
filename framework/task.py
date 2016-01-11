from mesos.interface import mesos_pb2


class Task(object):
    def __init__(self, id, name,slave_id):
        self.task = mesos_pb2.TaskInfo()
        self.task.task_id.value = id
        self.task.slave_id.value = slave_id
        self.task.name = name

    def configure_container_protobuf(self, expose_ports=False):
        container = mesos_pb2.ContainerInfo()
        container.type = 1

        container.docker.image = 'hussainsultan/distributed'
        container.docker.network = 2  # mesos_pb2.ContainerInfo.DockerInfo.Network.BRIDGE
        container.docker.force_pull_image = True

        # # Todo: Configure a port from the offer and assign it dynamically
        if expose_ports:
            docker_port = container.docker.port_mappings.add()
            docker_port.host_port = 33001
            docker_port.container_port = 8786

        self.task.container.MergeFrom(container)
        return self

    def configure_port_resources(self):
        mesos_ports = self.task.resources.add()
        mesos_ports.name = "ports"
        mesos_ports.type = mesos_pb2.Value.RANGES
        port_range = mesos_ports.ranges.range.add()
        # print port_range
        available_port = 33001
        port_range.begin = available_port
        port_range.end = available_port

        return self

    def configure_memory_resources(self):
        mem = self.task.resources.add()
        mem.name = "mem"
        mem.type = mesos_pb2.Value.SCALAR
        mem.scalar.value = 128

        return self

    def configure_cpu_resources(self):
        cpu = self.task.resources.add()
        cpu.name = "cpus"
        cpu.type = mesos_pb2.Value.SCALAR
        cpu.scalar.value = 1
        return self

    def configure_command_protobuf(self, command_string):
        command = mesos_pb2.CommandInfo()
        command.value = command_string
        self.task.command.MergeFrom(command)

        return self
