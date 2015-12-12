from framework.scheduler_driver import DistributedDriver
from framework.distributed_scheduler import DistributedScheduler

if __name__ == '__main__':
    driver = DistributedDriver().create_driver(DistributedScheduler)
    driver.run()
