import time
from datetime import datetime
from threading import Thread, Event


# Create class that checks if current date matches the notification date
# After initializing, call start_tick() to begin checking if the 
# Notification should be sent.
class Notification:

    """
    param: Notification_id : int
    param: SubAssignment_id : int
    param: Message : string
    param: send_date : datetime
    param: tick_frequency : float
    """
    def __init__(self, notification_id, subassignment_id, message, send_date=datetime, tick_frequency=60.0): # Checks every minute by default
        self._id = notification_id
        self._assignment_id = subassignment_id
        self._previous_time = datetime.now().time()
        self._frequency = tick_frequency
        self._date = send_date
        self._tick_thread = Thread(target=self._perform_tick())
        self._stop_tick_event = Event()

    """ ==== Getters ==== """

    def get_id(self):
        return self._id
    
    def get_assignment_id(self):
        return self._assignment_id

    def get_previous_tick_execution(self):
        return self._previous_time

    def get_tick_frequency(self):
        return self._frequency

    def get_date(self):
        return self._date

    """ ==== Mutators ==== """

    def set_id(self, new_id):
        self._id = new_id
        
    def set_subassignment_id(self, new_id):
        self._assignment_id = new_id

    def set_tick_frequency(self, frequency):
        self._frequency = frequency

    def set_date(self, date):
        self._date = date

    """ ==== Ticking ==== """

    # Start notification thread
    def start_tick(self):
        self._tick_thread.start()

    # Thread function to call at frequency amount
    def _perform_tick(self):
        while True:
            delta_time = datetime.now().time() - self._previous_time
            if delta_time > self._frequency:
                self._tick()
                self._previous_time = datetime.now().time()
            if self._stop_tick_event.is_set():
                break

    # Event called to check if notification should be sent out
    def _tick(self, delta_time):
        if self._date >= datetime.now().date():
            self.send_notification()

    # Event to stop tick thread
    def stop_tick(self):
        self._stop_tick_event.set()
        self._tick_thread.join()

    # Event called when notification parameters have been met.
    # Should send a phone and email notification.
    def send_notification(self):
        pass
