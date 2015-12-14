import subprocess
import time

import requests


class MesosCluster(object):
    def get_state(self):
        return requests.get('http://127.0.0.1:5050/state').json()

    def __enter__(self):
        self.mesos_master = subprocess.Popen('/usr/local/sbin/mesos-master --registry=in_memory --ip=127.0.0.1',
                                             shell=True, stdin=subprocess.PIPE,
                                             stdout=subprocess.PIPE,
                                             stderr=subprocess.PIPE)

        self.mesos_slave = subprocess.Popen('sudo /usr/local/sbin/mesos-slave --master=localhost:5050',
                                            shell=True, stdin=subprocess.PIPE,
                                            stdout=subprocess.PIPE,
                                            stderr=subprocess.PIPE)

        time.sleep(1)

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        subprocess.Popen('sudo kill -9 {0}'.format(self.mesos_slave.pid), shell=True, stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
        self.mesos_master.kill()
