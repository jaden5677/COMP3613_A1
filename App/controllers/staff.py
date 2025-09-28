from App.models import Staff
from App.database import db

def create_user(username, password, position, email):
    newuser = Staff(username=username, password=password, position=position, email=email)
    db.session.add(newuser)
    db.session.commit()
    return newuser

def get_user_by_username(username):
    result = db.session.execute(db.select(Staff).filter_by(username=username))
    return result.scalar_one_or_none()

def get_user(id):
    return db.session.get(Staff, id)

def get_all_users():
    return db.session.query(Staff).all()

def get_all_users_json():
    users = get_all_users()
    if not users:
        return []
    users = [user.get_json() for user in users]
    return users

def update_user(id, username):
    user = get_user(id)
    if user:
        user.username = username
        # user is already in the session; no need to re-add
        db.session.commit()
        return True
    return None