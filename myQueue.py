###
### Elementary Synchronized Queue as a monitor (with condition variable)
###
### Author:    Mark A. Sheldon, Tufts University
### Date:      28 September 2014
### Modified:  28 September 2014
###
### Intended for producer consumer problems.  This implements an infinite
### queue, and therefore, there is no need for a condition variable
### to indicate space available.  The only condition of interest indicates
### that a data element is available.
###
### Python condition variables create a lock associated with them, so
### there is no need to make a lock of our own, we could use that one.
### I find it hard to pick a good name, though, that can mean both
### "acquire the lock" for mutual exclusion and "alert the troops" for
### signaling the condition.
###

import threading

class SynchronizedQueue:
    def __init__(self):
        self.__data           = []
        self.__lock           = threading.Lock()
        self.__data_available = threading.Condition(self.__lock)

    def __isEmpty(self):
        return len(self.__data) == 0

    def put(self, item):
        with self.__lock:
            self.__data.append(item)         # Last element goes on back
            self.__data_available.notify()

    def get(self):
        with self.__lock:
            while self.__isEmpty():
                self.__data_available.wait()
            return self.__data.pop(0)        # First element is at front