from App.models import Roster, Staff
from App.database import db
from datetime import datetime, time

# Get a roster by ID
def get_roster(roster_id):
	return db.session.get(Roster, roster_id)

# Get all rosters
def get_all_rosters():
	return db.session.query(Roster).all()

# Get all rosters as JSON
def get_all_rosters_json():
	rosters = get_all_rosters()
	if not rosters:
		return []
	return [roster.get_json() for roster in rosters]

# Create a new roster
def create_roster(staff_id, shift_date, shift_start, shift_end):
	try:
		shift_date_obj = datetime.strptime(shift_date, '%Y-%m-%d').date() if isinstance(shift_date, str) else shift_date
		shift_start_obj = datetime.strptime(shift_start, '%H:%M:%S').time() if isinstance(shift_start, str) else shift_start
		shift_end_obj = datetime.strptime(shift_end, '%H:%M:%S').time() if isinstance(shift_end, str) else shift_end
	except Exception as e:
		raise ValueError(f"Invalid date/time format: {e}")
	new_roster = Roster(staff_id=staff_id, shift_date=shift_date_obj, shift_start=shift_start_obj, shift_end=shift_end_obj)
	db.session.add(new_roster)
	db.session.commit()
	return new_roster

def update_roster(roster_id, staff_id=None, shift_date=None, shift_start=None, shift_end=None):
	roster = get_roster(roster_id)
	if not roster:
		return None
	if staff_id is not None:
		roster.staff_id = staff_id
	if shift_date is not None:
		roster.shift_date = datetime.strptime(shift_date, '%Y-%m-%d').date() if isinstance(shift_date, str) else shift_date
	if shift_start is not None:
		roster.shift_start = datetime.strptime(shift_start, '%H:%M:%S').time() if isinstance(shift_start, str) else shift_start
	if shift_end is not None:
		roster.shift_end = datetime.strptime(shift_end, '%H:%M:%S').time() if isinstance(shift_end, str) else shift_end
	db.session.commit()
	return roster

def delete_roster(roster_id):
	roster = get_roster(roster_id)
	if not roster:
		return False
	db.session.delete(roster)
	db.session.commit()
	return True

def get_rosters_by_staff(staff_id):
	return db.session.scalars(db.select(Roster).filter_by(staff_id=staff_id)).all()


def get_rosters_by_date(shift_date):
	if isinstance(shift_date, str):
		shift_date = datetime.strptime(shift_date, '%Y-%m-%d').date()
	return db.session.scalars(db.select(Roster).filter_by(shift_date=shift_date)).all()

def is_staff_scheduled(staff_id, shift_date):
	if isinstance(shift_date, str):
		shift_date = datetime.strptime(shift_date, '%Y-%m-%d').date()
	return db.session.scalar(db.select(Roster).filter_by(staff_id=staff_id, shift_date=shift_date)) is not None


def get_next_roster_for_staff(staff_id):
	today = datetime.now().date()
	return db.session.scalars(
		db.select(Roster).filter(Roster.staff_id == staff_id, Roster.shift_date >= today).order_by(Roster.shift_date.asc())
	).first()
