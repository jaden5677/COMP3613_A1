from App.database import db

class StaffRoster(db.Model):
    __tablename__ = 'staff_roster'
    id = db.Column(db.Integer, primary_key=True)
    staff_id = db.Column(db.Integer, db.ForeignKey('staff.id'), nullable=False)
    roster_id = db.Column(db.Integer, db.ForeignKey('roster.id'), nullable=False)
    assigned_date = db.Column(db.Date, db.ForeignKey('roster.shift_date'), nullable=False)
    assigned_shift_start = db.Column(db.Time, db.ForeignKey('roster.shift_start'), nullable=False)
    assigned_shift_end = db.Column(db.Time, db.ForeignKey('roster.shift_end'), nullable=False)
    staff = db.relationship('Staff', backref='staff_rosters', lazy=True)
    roster = db.relationship('Roster', backref='staff_rosters', lazy=True)

    def __repr__(self):
        return f'<StaffRoster Staff {self.staff_id} - Roster {self.roster_id} on {self.assigned_date}>'