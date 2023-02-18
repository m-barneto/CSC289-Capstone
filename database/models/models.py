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
    description: str
    type: str
    weight: str  # Maybe change to float, following db scheme for now
    priority: int
    completed: bool
    due: datetime
    recurring: bool
    sub_assignments: list[SubAssignment]


@dataclass
class Course:
    id: int
    name: str
    section: str
    professor: str
    online: bool
    dropped: bool
    color: str
    assignments: list[Assignment]


@dataclass
class User:
    id: int
    username: str
    password: str
    email: str
    phone_number: int
    degree: str
    semester: str
