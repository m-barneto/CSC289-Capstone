from assignment import Assignment
import csv


""" Manager model for handling all assignments added by the user.
* Ideally, the user would create an assignment, then add it to the list.
* The list then would sync with the database.
* @todo: Add database interaction either through function parameters or
*        a member variable. """
class AssignmentManager:

    # Parameter: in_database = assignmentDatabase type
    def __init__(self, in_database):
        self._assignments = list()
        self._notifications = list()
        self._database = in_database
        rows = in_database.get_all_rows_assignments()
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
        rows = in_database.get_all_rows_notifications()
        for row in rows:
            self._notifications.append(Notification(row[0], # id
                                                   row[1],  # message
                                                   row[2],  # delivery_method
                                                   row[3],  # send_at
                                                   row[4],  # assignment_id
                                                   row[5])) # sub_assignment_id

    # Utility for creating assignments
    def create_assignment(self, assignment_id, course_id=None, name=None, type=None, weight=None, priority=None, completed=None, due=None, recurring=None, notification_id=None):
        return Assignment(assignment_id,    # We can probably use len(_assignments) if we never remove assignments.
                          course_id,
                          name,
                          type,
                          weight,
                          priority,
                          completed,
                          due,
                          recurring,
                          notification_id)

    # Utility for creating notifications
    def create_notification(self, notification_id, message=None, delivery_method=None, send_at=None, assignment_id=None, sub_assignment_id=None):
        return Notification(notification_id,    # Same comment as create_assignment(); we can probably use len(self._notifications) if we never remove any notifications.
                           message,
                           delivery_method,
                           send_at,
                           assignment_id,
                           sub_assignment_id)
    
    # Function for adding notifications when additional assignments get added
    def add_notification(self, in_notification):
        self._database.add_row_notifications(in_notification)
    
    # Function for user to add additional assignments.
    def add_assignment(self, in_assignment):
        self._assignments.append(in_assignment)
        self._database.add_row_assignments(in_assignment)
        if not in_assignment.get_completed:
            self.add_notification(self.create_notification(len(self._notifications)))

    # Function for user to remove assignments.
    def remove_assignment(self, in_assignment):
        in_assignment.on_removed()
        self._assignments.remove(in_assignment)
        self._database.remove_row_assignments(in_assignment.get_id())

    # Overloaded version to allow passing assignment_id.
    def remove_assignment_from_id(self, id):
        del self._assignments[id]
        self._database.remove_row_assignments(id)

    # Returns all assignments that are internally marked as completed.
    def view_completed_assignments(self):
        completed_assignments = []
        for a in self._assignments:
            if a.get_completed():
                completed_assignments.append(a)
        return completed_assignments

    # Sets a given assignment to repeat
    def set_repeating_assignment(self, in_assignment, repeats):
        in_assignment.set_recurring(repeats)
        self._database.update_row_assignments_recurring(in_assignment)

    # Exports assignments to csv file
    def export_assignments(self, filename):
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

