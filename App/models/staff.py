from App.database import db

class Staff(db.User):
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    position = db.Column(db.String(50), nullable=False, default='Staff')
    roster = db.relationship('Roster', backref='staff', lazy=True)
    check_in_time = db.Column(db.Time, nullable=True)
    check_out_time = db.Column(db.Time, nullable=True)

    def __init__(self, username, password, position='Staff'):
        super().__init__(username, password)
        self.position = position

    def set_check_in(self, check_in_time):
        self.check_in_time = check_in_time

    def set_check_out(self, check_out_time):
        self.check_out_time = check_out_time

    def get_json(self):
        user_json = super().get_json()
        user_json.update({
            'position': self.position
        })
        return user_json