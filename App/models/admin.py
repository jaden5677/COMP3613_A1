from App.database import db

class Admin(db.User):
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    staff_list = db.relationship('Staff', backref='admin', lazy=True)
    roster_list = db.relationship('Roster', backref='admin', lazy=True)

    def __init__(self, username, password):
        super().__init__(username, password)
        

    def get_json(self):
        user_json = super().get_json()
        user_json.update({
            'admin_level': self.admin_level
        })
        return user_json