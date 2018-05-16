import psutil
import time
import sys
from collections import deque


bytes_recv = deque(maxlen=20)
bytes_recv.append(psutil.net_io_counters().bytes_recv)


try:
    while True:
        bytes_recv_start = psutil.net_io_counters().bytes_recv
        bytes_per_second = bytes_recv_start - bytes_recv[-1]
        bytes_recv.append(bytes_recv_start)

        print(round(bytes_per_second / 2**20, 2))
        time.sleep(1)

except KeyboardInterrupt:
    sys.exit(0)
