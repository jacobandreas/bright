from events import *

import threading
import collections
import traceback
import sys

class Dispatcher:

    def __init__(self):
        self.listeners = []
        self.events = collections.deque()
        self.cv = threading.Condition()

        t = threading.Thread(None, self.Listen, "EventQueue")
        t.daemon = True
        t.start()

    def Register(self, listener):
        self.listeners.append(listener)

    def Unregister(self, listener):
        self.listeners.remove(listener)

    def Post(self, evt):
        self.cv.acquire()
        self.events.append(evt)
        self.cv.notify()
        self.cv.release()

    def Listen(self):
        while True:
            try:
                self.cv.acquire()
                while not len(self.events) > 0:
                    self.cv.wait()
                evt = self.events.popleft()
                for listener in self.listeners:
                    listener.Notify(evt)
                self.cv.release()
                if isinstance(evt, QuitEvent):
                    break
            except Exception as inst:
                traceback.print_exc()
                q = QuitEvent()
                for listener in self.listeners:
                    listener.Notify(q)
