"""
event_queue.py

Central event queue for the engine.
All events (market, signal, order, fill) flow through here.
"""

from queue import Queue

class EventQueue:
    """
    Wrapper around Python's Queue to manage events.
    """

    def __init__(self):
        self.queue = Queue()

    def put(self, event):
        self.queue.put(event)

    def get(self):
        return self.queue.get()

    def empty(self):
        return self.queue.empty()