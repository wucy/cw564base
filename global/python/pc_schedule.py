#! /usr/bin/env python


import Queue
import time
import os
import re
import sys
import threading

class pc_worker(threading.Thread):
    def __init__(self, queue, name = "WORKER", time_out = 1):
        threading.Thread.__init__(self)
        self.queue = queue
        self.is_stop = False
        self.name = name
        self.time_out = time_out
        self.log = list()

    def run(self):
        while not self.is_stop or self.queue.qsize() != 0:
            if (self.is_stop):
                if self.queue.qsize() != 0:
                    pass
                    #print '[%s]%s Waiting %d item(s) in queue.' % (self.name, time.ctime(), self.queue.qsize())a
                else:
                    #print '[%s] Stopping ...' % (self.name)
                    break
            cmd = None
            try:
                cmd = self.queue.get(True, self.time_out)
            except:
                #print '[%s]%s Queue is empty, waiting...' % (self.name, time.ctime())
                continue
            log = (cmd, os.popen(cmd).readlines())
            self.log.append(log)

    def stop(self):
        self.is_stop = True



class pc_scheduler:
    def __init__(self, num_worker):
        self.queue = Queue.Queue()
        self.worker_list = list()
        for i in range(num_worker):
            worker = pc_worker(self.queue, "WORKER" + str(i))
            worker.setDaemon(True)
            self.worker_list.append(worker)
            worker.start()

    def add_job(self, cmd):
        self.queue.put(cmd)

    def wait(self):
        for worker in self.worker_list:
            worker.stop()
        for worker in self.worker_list:
            worker.join()


def tester():
    schedule = pc_scheduler(10000)
    for i in range(10000):
        schedule.add_job('ls')

    schedule.wait()
    #print schedule.worker_list[0].log


if __name__ == '__main__':
    tester()

