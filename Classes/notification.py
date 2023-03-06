import time
from datetime import datetime
from threading import Thread, Event


class NotificationDelegate:
    """
    A class decorator intended to be used on functions.
    You may call the function as normal, for Example:

    @NotificationDelegate
    def foo():
        pass

    foo() # This will call the function foo()

    Other objects may bind their functions to this function
    And be called in sequence as a result. For Example:

    @NotificationDelegate
    def foo():
        pass

    class Bar:
        def do_something(self):
            pass

    bar = Bar()
    foo.add_event(bar.do_something)
    foo() # This will call foo() and then bar.do_something()
    """

    def __init__(self, func):
        """Constructor for delegate object."""

        self._func = func
        self._events = list()

    def __call__(self):
        """() override to call __call__() on all bound events."""

        self._func()
        self.broadcast()

    def broadcast(self):
        """Calls all bound events."""

        for event in self._events:
            event()

    def add_event(self, event):
        """Adds an event to be called when this object has been called."""

        self._events.append(event)


class Notification:
    """
    Class that checks if current date matches the notification date.
    After initializing, call start_tick() to begin checking if the
    Notification should be sent.
    """

    """
    Function Section
    ======= Defaults =======
    """

    def __init__(self, notification_id, subassignment_id, message, send_date=datetime, tick_frequency=60.0): # Checks every minute by default
        """
        Constructor for Notification class

        Parameters:
            notification_id : int
            sub_Assignment_id : int
            message : string
            send_date : datetime
            tick_frequency : float
        """

        self._id = notification_id
        self._assignment_id = subassignment_id
        self._previous_time = datetime.now().time()
        self._frequency = tick_frequency
        self._date = send_date
        self._tick_thread = Thread(target=self._perform_tick())
        self._stop_tick_event = Event()

    """
    Function Section
    ==== Getters ====
    """

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

    """
    Function Section
    ==== Mutators ====
    """

    def set_id(self, new_id):
        self._id = new_id

    def set_subassignment_id(self, new_id):
        self._assignment_id = new_id

    def set_tick_frequency(self, frequency):
        self._frequency = frequency

    def set_date(self, date):
        self._date = date

    """
    Function Section
    ==== Ticking ====
    """

    def start_tick(self):
        """
        Starts notification thread.
        An infinite loop checks if enough time has elapsed
        To check if the send_date has been reached. There is
        An exit event in case of early shutdown as well.
        """
        self._tick_thread.start()

    def _perform_tick(self):
        """Thread function to call at frequency amount."""

        while True:
            delta_time = datetime.now().time() - self._previous_time
            if delta_time > self._frequency:
                self._tick()
                self._previous_time = datetime.now().time()
            if self._stop_tick_event.is_set():
                break

    def _tick(self, delta_time):
        """Event called to check if notification should be sent out"""

        if self._date >= datetime.now().date():
            self.send_notification()

    def stop_tick(self):
        """Event to stop tick thread."""

        self._stop_tick_event.set()
        self._tick_thread.join()

    @NotificationDelegate
    def send_notification(self):
        """
        Event called when notification parameters have been met.
        Should send a phone and email notification.

        This has been decorated with a delegate decoration.
        This means that other functions can bind themselves to
        This function and be called after this Event is called.
        """

        pass
