from App.database import db
from .staff import Staff

class Admin(Staff):
    id = db.Column(db.Integer, db.ForeignKey('staff.id'), primary_key=True)
    staff_list = db.relationship('Staff', backref='admin', lazy=True)
    roster_list = db.relationship('Roster', backref='admin', lazy=True)

    def __init__(self, username, password, position, email):
        super().__init__(username, password, position=position, email=email)
        

    def get_staff_roster(self):
        return {
            'staff': [staff.get_json() for staff in self.staff_list],
            'rosters': [roster.get_json() for roster in self.roster_list]
        }

    def get_json(self):
        user_json = super().get_json()

        return user_json