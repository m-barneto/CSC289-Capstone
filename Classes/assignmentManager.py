from assignment import Assignment


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
    def create_assignment(self, assignment_id, course_id=None, name=None, type=None, weight=None, priority=None, completed=None, due=None, recurring=None, notification_id=None):
        return Assignment(assignment_id,
                          course_id,
                          name,
                          type,
                          weight,
                          priority,
                          completed,
                          due,
                          recurring,
                          notification_id)

    # Function for user to add additional assignments.
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
    *   repeats       = boolean value to change assignment.recurring to """
    def set_repeating_assignment(self, in_assignment, repeats):
        in_assignment.set_recurring(repeats)

    # Exports assignments to csv file
    def export_assignments(self):
        pass
