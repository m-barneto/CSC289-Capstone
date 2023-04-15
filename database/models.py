from dataclasses import dataclass
from datetime import datetime
from typing import Literal


@dataclass
class Notification:
    id: int
    sub_assignment_id: int
    message: str
    delivery_method: Literal[0, 1, 3]  # Literal is a place holder
    send: datetime


@dataclass
class SubAssignment:
    id: int
    assignment_id: int
    name: str
    description: str
    completed: bool
    due: datetime
    notification: Notification


@dataclass
class Assignment:
    id: int
    course_id: int
    name: str
    type: str
    weight: str  # Maybe change to float, following db scheme for now
    priority: int
    completed: bool
    due: datetime
    recurring: bool
    #sub_assignments: list[SubAssignment]
    notification_id: int
    def params(self):
        return self.course_id, self.name, self.type, self.weight, self.priority, self.completed, self.due, self.recurring, self.notification_id


@dataclass
class Course:
    id: int
    name: str
    section: str
    professor: str
    online: bool
    dropped: bool
    color: str
    def params(self):
        return self.name, self.section, self.professor, self.online, self.dropped, self.color


@dataclass
class User:
    id: int
    username: str
    password: str
    email: str
    phone_number: int
    degree: str
    semester: str
    def params(self):
        return self.id, self.username, self.password, self.email, self.phone_number, self.degree, self.semester
