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
    date = db.relationship('Roster', foreign_keys=[assigned_date], primaryjoin='StaffRoster.assigned_date == Roster.shift_date', lazy=True)
    shift_start = db.relationship('Roster', foreign_keys=[assigned_shift_start], primaryjoin='StaffRoster.assigned_shift_start == Roster.shift_start', lazy=True)
    shift_end = db.relationship('Roster', foreign_keys=[assigned_shift_end], primaryjoin='StaffRoster.assigned_shift_end == Roster.shift_end', lazy=True)

    def init__(self, staff_id, roster_id, assigned_date, assigned_shift_start, assigned_shift_end):
        self.staff_id = staff_id
        self.roster_id = roster_id
        self.assigned_date = assigned_date
        self.assigned_shift_start = assigned_shift_start
        self.assigned_shift_end = assigned_shift_end

    def __repr__(self):
        return f'<StaffRoster Staff {self.staff_id} - Roster {self.roster_id} on {self.assigned_date}>'