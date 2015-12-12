from mesos.interface import mesos_pb2



def configure_resources_for_a_task( id, task,slave_id):
    task.task_id.value = id
    task.slave_id.value = slave_id
    task.name = "task {}".format(str(id))
    cpus = task.resources.add()
    cpus.name = "cpus"
    cpus.type = mesos_pb2.Value.SCALAR
    cpus.scalar.value = 1
    mem = task.resources.add()
    mem.name = "mem"
    mem.type = mesos_pb2.Value.SCALAR
    mem.scalar.value = 1000
    return task