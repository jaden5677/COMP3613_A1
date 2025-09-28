from App.models import Admin, Roster
from App.database import db
from App.controllers.roster import (
	create_roster, update_roster, delete_roster, get_roster, get_all_rosters, get_rosters_by_staff
)

# Create a new admin
def create_admin(username, password, email, position='Admin'):
	new_admin = Admin(username=username, password=password, position=position, email=email)
	db.session.add(new_admin)
	db.session.commit()
	return new_admin

def get_admin(admin_id):
	return db.session.get(Admin, admin_id)


def get_all_admins():
	return db.session.query(Admin).all()


def get_all_admins_json():
	admins = get_all_admins()
	if not admins:
		return []
	return [admin.get_json() for admin in admins]


def admin_create_roster(admin_id, staff_id, shift_date, shift_start, shift_end):
	admin = get_admin(admin_id)
	if not admin:
		return None
	return create_roster(staff_id, shift_date, shift_start, shift_end)


def admin_update_roster(admin_id, roster_id, staff_id=None, shift_date=None, shift_start=None, shift_end=None):
	admin = get_admin(admin_id)
	if not admin:
		return None
	return update_roster(roster_id, staff_id, shift_date, shift_start, shift_end)


def admin_delete_roster(admin_id, roster_id):
	admin = get_admin(admin_id)
	if not admin:
		return False
	return delete_roster(roster_id)


def admin_get_rosters_by_staff(admin_id, staff_id):
	admin = get_admin(admin_id)
	if not admin:
		return []
	return get_rosters_by_staff(staff_id)


def admin_get_all_rosters(admin_id):
	admin = get_admin(admin_id)
	if not admin:
		return []
	return get_all_rosters()
