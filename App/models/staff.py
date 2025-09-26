from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db

class Staff(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username =  db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=True, unique=True)
    position = db.Column(db.String(50), nullable=False, default='Staff')
    #roster = db.relationship('Roster', backref='staff', lazy=True)
    check_in_time = db.Column(db.Time, nullable=True)
    check_out_time = db.Column(db.Time, nullable=True)

    def __init__(self, username, password, position=position, email=email):
        self.username = username
        self.set_password(password)
        self.email = email
        self.position = position

    def set_check_in(self, check_in_time):
        self.check_in_time = check_in_time

    def set_check_out(self, check_out_time):
        self.check_out_time = check_out_time

    def get_json(self):
        return{
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'position': self.position,
            'check_in_time': self.check_in_time,
            'check_out_time': self.check_out_time
        }
    
    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f'<User {self.username} - {self.email}>'