import sqlite3


class CRUD:

    def __init__(self, courses, assignments, subassignments, notifications):
        self.courses = []
        self.assignments = []
        self.subassignments = []
        self.notifications = []

    def readclass(self, courses):
        con = sqlite3.connect('storage.db')
        for row in con.execute("SELECT * FROM courses"):
            courses.append(row)
        return courses

    def readassignment(self, assignments):
        con = sqlite3.connect('storage.db')
        for row in con.execute("SELECT * FROM assignments"):
            assignments.append(row)
        return assignments

    def readsubassignments(self, subassignments):
        con = sqlite3.connect('storage.db')
        for row in con.execute("SELECT * FROM subassignments"):
            subassignments.append(row)
        return subassignments

    def readnotifications(self, notifications):
        con = sqlite3.connect('storage.db')
        for row in con.execute("SELECT * FROM notifications"):
            notifications.append(row)
        return notifications

    def updateclass(self):
        con = sqlite3.connect('storage.db')
        con.execute("UPDATE class SET ? WHERE ?", new, old)
        con.commit()

    def updateassignments(self):
        con = sqlite3.connect('storage.db')
        con.execute("UPDATE assignments SET ? WHERE ?", new, old)
        con.commit()

    def updatesubassignmentss(self):
        con = sqlite3.connect('storage.db')
        con.execute("UPDATE subassignments SET ? WHERE ?", new, old)
        con.commit()

    def updatenotifications(self):
        con = sqlite3.connect('storage.db')
        con.execute("UPDATE notifications SET ? WHERE ?", new, old)
        con.commit()

     def deleteclass(self):
        con = sqlite3.connect('storage.db')
        con.execute("DELETE FROM class WHERE ?", query)
        con.commit()

    def deleteassignments(self):
        con = sqlite3.connect('storage.db')
        con.execute("DELETE FROM assignments WHERE ?", query)
        con.commit()

    def deletesubassignmentss(self):
        con = sqlite3.connect('storage.db')
        con.execute("DELETE FROM subassignments WHERE ?", query)
        con.commit()

    def deletenotifications(self):
        con = sqlite3.connect('storage.db')
        con.execute("DELETE FROM notifications WHERE ?", query)
        con.commit()
