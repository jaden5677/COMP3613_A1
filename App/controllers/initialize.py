from .staff import create_user
from .admin import create_admin
from .roster import create_roster

from App.database import db


def initialize():
    db.drop_all()
    db.create_all()
    create_user('bob', 'bobpass', 'Manager', 'bob@mail.com')
    create_admin('admin', 'adminpass', 'Admin', 'admin@mail.com')
    create_roster(1, '2023-10-01', '09:00:00', '17:00:00')
    create_roster(1, '2023-10-02', '10:00:00', '18:00:00')
