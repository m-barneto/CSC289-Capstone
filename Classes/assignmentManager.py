from assignment import Assignment
from assignmentDatabase import AssignmentDatabase
from notification import Notification
from datetime import datetime, timedelta
import csv


class AssignmentManager:
    """
    * Manager model for handling all assignments added by the user.
    * Ideally, the user would create an assignment, then add it to the list.
    * The list then would sync with the database.
    """

    """
    Function Section
    ======= Defaults =======
    """

    def __init__(self, in_database: AssignmentDatabase):
        """
        The constructor for AssignmentManager.

        Parameters:
            in_database (assignmentDatabase): The assignment database to manage.
        """

        self._database = in_database
        self._init_assignments_()
        self._init_notifications_()

    """
    Function Section
    ===== Initialization =====
    """

    def _init_assignments_(self):
        """
        Utility to break up functionality of __init__() into more clear and clean tasks.
        Sets assignments to an empty list, then retrieves all assignments from database.
        """

        self._assignments = list()
        rows = self._database.get_all_rows_assignments()
        for row in rows:
            self._assignments.append(Assignment(row[0],  # id
                                               row[1],   # course id
                                               row[2],   # name
                                               row[3],   # type
                                               row[4],   # weight
                                               row[5],   # priority
                                               row[6],   # completed
                                               row[7],   # due
                                               row[8],   # recurring
                                               row[9]))  # notification id

    def _init_notifications_(self):
        """
        Utility to break up functionality of __init__() into more clear and clean tasks
        Sets notifications to an empty list, then retrieves all notifications from the database.
        """

        self._notifications = list()
        rows = self._database.get_all_rows_notifications()
        for row in rows:
            n = Notification(row[0], # id
                           row[1],  # message
                           row[2],  # delivery_method
                           row[3],  # send_at
                           row[4],  # assignment_id
                           row[5])  # sub_assignment_id
            n.send_notification.add_event(self._on_notification_sent)
            self._notifications.append(n)

    """
    Function Section
    ==== Getters ====
    """

    def get_assignments_with_notification_id(self, id):
        """
        Retrieves all assignments attached to a notification id.

        Returns:
            a (Assignment object): Assignment connected to notification_id
        """

        for a in self._assignments:
            if id == a.get_notification_id():
                return a
        return None

    """
    Function Section
    ===== Object Creation =====
    """

    def create_assignment(self, course_id=None, name=None, type=None, weight=None, priority=None, completed=None, due=None, recurring=None, notification_id=None):
        """
        Utility for creating assignment objects.

        Parameters:
            assignment_id (int):
            course_id (int):
            name (string):
            type (str):
            weight (string):
            priority (int):
            completed (boolean):
            due (datetime):
            recurring (boolean):
            notification_id (int):

        Returns:
            Assignment (object)
        """

        return Assignment(self._find_assignment_id(),    # We can probably use len(_assignments) if we never remove assignments.
                          course_id,
                          name,
                          type,
                          weight,
                          priority,
                          completed,
                          due,
                          recurring,
                          notification_id)

    def create_notification(self, sub_assignment_id=None, message=None, delivery_method=None, send_at=None):
        """
        Utility for creating notification objects.

        Parameters:
            notification_id (int): A unique identifier used as a primary key in the SQL database
            sub_assignment_id (int): Foriegn key identifying the assignments that this notification references.
            message (string): Literal string to display when notification is sent out.
            delivery_method (int, enum, Literal @todo: figure this out):

        Returns:
            Notification (object)
        """

        n = Notification(self._find_notification_id(),    # Same comment as create_assignment(); we can probably use len(self._notifications) if we never remove any notifications.
                           message,
                           delivery_method,
                           send_at,
                           sub_assignment_id)
        n.send_notification.add_event(self._on_notification_sent)
        return n

    def _find_assignment_id(self):
        id = 0
        for assignment in self._assignments:
            if assignment.get_id() != id:
                return id
            id += 1
        return len(self._assignments)

    def _find_notification_id(self):
        id = 0
        for notification in self._notifications:
            if notification.get_id() != id:
                return id
            id += 1
        return len(self._notificaitons)

    """
    Function Section
    == Delegate Events ==
    """

    def _on_notification_sent(self, sent_notification):
        """
        Function bound to notification delegate inside of each Notification.
        Will be called from a separate thread when date matches current date.
        """

        if self.get_assignments_with_notification_id(sent_notification.get_id()).get_recurring():
            sent_notification.reset(7) # Default is weekly, but should the occurrence be variable?
        else:
            sent_notification.stop_tick()

    """
    Function Section
    ===== Addition =====
    """

    def add_notification(self, in_notification):
        """Function for adding notifications when additional assignments get added."""

        self._database.add_row_notifications(in_notification)

    def add_assignment(self, in_assignment):
        """Function for user to add additional assignments."""

        self._assignments.append(in_assignment)
        self._database.add_row_assignments(in_assignment)
        if not in_assignment.get_completed:
            self.add_notification(self.create_notification())

    """
    Function Section
    === Modification ===
    """

    def update_assignment(self, in_assignment):
        database.update_row_assignments(in_assignment)

    def set_repeating_assignment(self, in_assignment, repeats):
        """Sets a given assignment to repeat."""

        in_assignment.set_recurring(repeats)
        self._database.update_row_assignments_recurring(in_assignment)

    """
    Function Section
    ===== Removal =====
    """

    def remove_assignment(self, in_assignment):
        """Function for user to remove assignments."""

        in_assignment.on_removed()
        self._assignments.remove(in_assignment)
        self._database.remove_row_assignments(in_assignment.get_id())

    def remove_assignment_from_id(self, id):
        """Overloaded version to allow passing assignment_id."""

        del self._assignments[id]
        self._database.remove_row_assignments(id)

    """
    Function Section
    ===== Viewing =====
    """

    def view_completed_assignments(self):
        """Returns all assignments that are internally marked as completed."""

        completed_assignments = []
        for a in self._assignments:
            if a.get_completed():
                completed_assignments.append(a)
        return completed_assignments

    def export_assignments(self, filename):
        """Exports assignments to csv file."""

        with open(filename, 'w', newline='') as csvfile:
            fieldnames = ['assignment_id', 'course_id', 'name','type', 'weight', 'priority', 'completed', 'due', 'recurring', 'notification_id']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            # todo: integrate with database
            # for assignment in database:
            #   writer.writerow({'assignment_id': assignment.get_id(),
            #                   'course_id': assignment.get_course_id(),
            #                   'name': assignment.get_name(),
            #                   'type': assignment.get_type(),
            #                   'weight': assignment.get_weight(),
            #                   'priority': assignment.get_priority(),
            #                   'completed': assignment.get_completed(),
            #                   'due': assignment.get_due(),
            #                   'recurring': assignment.get_recurring(),
            #                   'notification_id': assignment.get_notification_id})
            #
            # Hey you can actually just use the self._assignments variable for this since it should be the exact same as the database.
