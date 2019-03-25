from multiprocessing import Process, Lock
from collections import deque
import time

TARGET = deque(list(range(60)))


class Test(Process):
    def __init__(self, i):
        super().__init__()
        self.i = i
        self.lock = Lock()

    def run(self):
        self.lock.acquire()
        with open('1.txt', 'a') as f:
            f.write(str(self.i) + '\n')
        self.lock.release()
        time.sleep(1)


if __name__ == "__main__":
    while True:
        plist = []
        for i in range(10):
            p = Test(TARGET.pop())
            p.start()
            plist.append(p)

        for p in plist:
            p.join()
