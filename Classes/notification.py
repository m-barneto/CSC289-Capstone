import time
from datetime import datetime, timedelta


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

    All passed in events should have a Notification (object) parameter.
    """

    def __init__(self, func):
        """Constructor for delegate object."""

        self._func = func
        self._events = list()

    def __call__(self):
        """() override to call __call__() on all bound events."""

        self.broadcast()

    def broadcast(self):
        """Calls all bound events."""

        ret_value = self._func()
        for event in self._events:
            event(ret_value)

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
        self._date = send_date
        self._has_been_sent = False

        self._frequency = tick_frequency
        self._should_tick = True

    """
    Function Section
    ==== Getters ====
    """

    def get_id(self):
        return self._id

    def get_assignment_id(self):
        return self._assignment_id

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

    def reset(self, days):
        date_strip = datetime.strptime(self._date, "%m/%d/%y")
        new_date = date_strip + timedelta(days=10)
        self._date = new_date
        self._has_been_sent = False

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

        self._should_tick = True
        self._perform_tick()

    async def _perform_tick(self):
        """Thread function to call at frequency amount."""

        while self._should_tick:
            time.sleep(self._frequency)
            self._tick()

    def _tick(self, delta_time):
        """Event called to check if notification should be sent out"""

        if self._date >= datetime.now().date() and not self._has_been_sent:
            self.send_notification()

    def stop_tick(self):
        """Event to stop tick thread."""

        self._should_tick = False

    @NotificationDelegate
    def send_notification(self):
        """
        Event called when notification parameters have been met.
        Should send a phone and email notification.

        This has been decorated with a delegate decoration.
        This means that other functions can bind themselves to
        This function and be called after this Event is called.
        """

        self._has_been_sent = True
        return self
