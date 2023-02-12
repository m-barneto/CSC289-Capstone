from assignment import Assignment
import csv


""" Manager model for handling all assignments added by the user.
* Ideally, the user would create an assignment, then add it to the list.
* The list then would sync with the database.
* @todo: Add database interaction either through function parameters or
*        a member variable. """
class AssignmentManager:

    # Parameter: in_assignments = list of assignment type.
    def __init__(self, in_assignments):
        self._assignments = in_assignments

    # Utility for creating assignments
    def create_assignment(self, assignment_id, course_id=None, name=None, desc=None, type=None, weight=None, priority=None, completed=None, due=None, recurring=None, notification_id=None):
        return Assignment(assignment_id,
                          course_id,
                          name,
                          type,
                          desc,
                          weight,
                          priority,
                          completed,
                          due,
                          recurring,
                          notification_id)

    """ Function for user to add additional assignments.
    * @todo: Add connnection to database; something like...
        INSERT INTO assignments(assignment_id, course_id, name, desc, type, weight, priority, completed, due, recurring, notification_id) 
        VALUES(in_asignment.get_id(),in_asignment.get_course_id(),in_asignment.get_name(), in_assignment.get_desc(), in_asignment.get_type(),in_asignment.get_weight(),in_asignment.get_priority(),in_asignment.get_completed(),in_asignment.get_due(),in_asignment.get_recurring(),in_asignment.get_notification_id());
         """
    def add_assignment(self, in_assignment):
        self._assignments.append(in_assignment)

    # Function for user to remove assignments.
    def remove_assignment(self, in_assignment, conn):
        in_assignment.on_removed()
        self._assignments.remove(in_assignment)

    # Overloaded version to allow passing assignment_id.
    def remove_assignment_from_id(self, id):
        del self._assignments[id]

    # Returns all assignments that are internally marked as completed.
    def view_completed_assignments(self):
        completed_assignments = []
        for a in self._assignments:
            if a.get_completed():
                completed_assignments.append(a)
        return completed_assignments

    """ Sends a message to assignment to change to repeating (recurring)
    * Parameters:
    *   in_assignment = assignment to change
    *   repeats       = boolean value to change assignment.recurring to 
    *
    * #todo: Add connection to database; something like...
     ALTER_TABLE 
        WHERE
            assignment_id = in_assignment.id;"""
    def set_repeating_assignment(self, in_assignment, repeats):
        in_assignment.set_recurring(repeats)

    # Exports assignments to csv file
    def export_assignments(self, filename):
        with open(filename, 'w', newline='') as csvfile:
            fieldnames = ['assignment_id', 'course_id', 'name', 'desc', 'type', 'weight', 'priority', 'completed', 'due', 'recurring', 'notification_id']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            # todo: integrate with database
            # for assignment in database:
            #   writer.writerow({'assignment_id': assignment.get_id(),
            #                   'course_id': assignment.get_course_id(),
            #                   'name': assignment.get_name(),
            #                   'desc': assignment.get_desc(),
            #                   'type': assignment.get_type(),
            #                   'weight': assignment.get_weight(),
            #                   'priority': assignment.get_priority(),
            #                   'completed': assignment.get_completed(),
            #                   'due': assignment.get_due(),
            #                   'recurring': assignment.get_recurring(),
            #                   'notification_id': assignment.get_notification_id})

