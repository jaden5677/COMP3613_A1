from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db

class Admin(db.User):
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    admin_level = db.Column(db.Integer, nullable=False, default=1)

    def __init__(self, username, password, admin_level=1):
        super().__init__(username, password)
        self.admin_level = admin_level

    def get_json(self):
        user_json = super().get_json()
        user_json.update({
            'admin_level': self.admin_level
        })
        return user_json