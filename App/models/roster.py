from App.database import db

class Roster(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    staff_id = db.Column(db.Integer, db.ForeignKey('staff.id'), nullable=False)
    shift_date = db.Column(db.Date, nullable=False)
    shift_start = db.Column(db.Time, nullable=True)
    shift_end = db.Column(db.Time, nullable=True)
    #staff = db.relationship('Staff', backref='roster', lazy=True)


    def __init__(self, staff_id, shift_date, shift_start, shift_end):
        self.staff_id = staff_id
        self.shift_date = shift_date
        self.shift_start = shift_start
        self.shift_end = shift_end
    

    def get_json(self):
        return{
            'id': self.id,
            'staff_id': self.staff_id,
            'shift_date': self.shift_date.isoformat(),
            'shift_start': self.shift_start.isoformat(),
            'shift_end': self.shift_end.isoformat()
        }

    def __repr__(self):
        return f'<Roster {self.id} - Staff {self.staff_id} on {self.shift_date}>'