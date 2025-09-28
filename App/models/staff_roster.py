from App.database import db

class StaffRoster(db.Model):
    __tablename__ = 'staff_roster'
    id = db.Column(db.Integer, primary_key=True)
    staff_id = db.Column(db.Integer, db.ForeignKey('staff.id'), nullable=False)
    roster_id = db.Column(db.Integer, db.ForeignKey('roster.id'), nullable=False)
    assigned_date = db.Column(db.Date, nullable=False)
    assigned_shift_start = db.Column(db.Time, nullable=False)
    assigned_shift_end = db.Column(db.Time, nullable=False)
    staff_check_in = db.Column(db.Time, nullable=True)
    staff_check_out = db.Column(db.Time, nullable=True)
    staff = db.relationship('Staff', backref='staff_rosters', lazy=True)
    roster = db.relationship('Roster', backref='staff_rosters', lazy=True)
    

    def init__(self, staff_id, roster_id, assigned_date, assigned_shift_start, assigned_shift_end):
        self.staff_id = staff_id
        self.roster_id = roster_id
        self.assigned_date = assigned_date
        self.assigned_shift_start = assigned_shift_start
        self.assigned_shift_end = assigned_shift_end
        self.staff_check_in = None
        self.staff_check_out = None

    def __repr__(self):
        if self.staff_check_in and self.staff_check_out:
            return f'<StaffRoster Staff {self.staff_id} - Roster {self.roster_id} on {self.assigned_date} (Checked in at {self.staff_check_in}, Checked out at {self.staff_check_out})>'
        else:
            return f'<StaffRoster Staff {self.staff_id} - Roster {self.roster_id} on {self.assigned_date}>'
    
    def set_check_in(self, check_in_time):
        self.staff_check_in = check_in_time

    def set_check_out(self, check_out_time):
        self.staff_check_out = check_out_time