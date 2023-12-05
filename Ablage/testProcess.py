import logging

import threading

import time

def threadRoutine(wert):
    print('Thread wert',wert)
    time.sleep(2)
    print('Thread wert', wert)
    return

x = threading.Thread(target=threadRoutine, args=(1,))



x.start()
print('Main')
time.sleep(1)
print('Main')
time.sleep(1)
print('Main')
time.sleep(1)
print('Main')
time.sleep(1)
print('Main')
time.sleep(1)
# x.join()

logging.info("Main    : all done")