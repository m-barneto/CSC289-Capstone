class Assignment:
    def __init__(self,
                 assignment_id,
                 course_id=None,
                 name=None,
                 desc=None,
                 type=None,
                 weight=None,
                 priority=None,
                 completed=None,
                 due=None,
                 recurring=None,
                 notification_id=None):
        self._id                = assignment_id
        self._course_id         = course_id
        self._name              = name
        self._desc              = desc
        self._type              = type,
        self._weight            = weight
        self._priority          = priority
        self._completed         = completed
        self._due               = due
        self._recurring         = recurring
        self._notification_id   = notification_id

    """ ==== Getters ==== """

    def get_id(self):
        return self._id

    def get_course_id(self):
        return self._course_id

    def get_name(self):
        return self._name

    def get_desc(self):
        return self._desc

    def get_type(self):
        return self._type

    def get_weight(self):
        return self._weight

    def get_priority(self):
        return self._priority

    def get_completed(self):
        return self._completed

    def get_due(self):
        return self._due

    def get_recurring(self):
        return self._recurring

    def get_notification_id(self):
        return self._notification_id

    """ ==== Mutators ==== """

    def set_id(self, id):
        self._id = id

    def set_course_id(self, course_id):
        self._course_id = course_id

    def set_name(self, name):
        self._name = name

    def set_desc(self, desc):
        self._desc = desc

    def set_type(self, type):
        self._type = type

    def set_weight(self, weight):
        self._weight = weight

    def set_priority(self, priority):
        self._priority = priority

    def set_completed(self, completed):
        self._completed = completed

    def set_due(self, due):
        self._due = due

    def set_recurring(self, recurring):
        self._recurring = recurring

    def set_notification_id(self, notification_id):
        self._notification_id = notification_id
