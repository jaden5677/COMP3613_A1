from App.models import StaffRoster
from App.database import db

def assign_roster_to_staff(staff_id, roster_id, assigned_date, assigned_shift_start, assigned_shift_end):
    new_assignment = StaffRoster(
        staff_id=staff_id,
        roster_id=roster_id,
        assigned_date=assigned_date,
        assigned_shift_start=assigned_shift_start,
        assigned_shift_end=assigned_shift_end
    )
    db.session.add(new_assignment)
    db.session.commit()
    return new_assignment

def get_staff_roster_by_id(assignment_id):
    return db.session.get(StaffRoster, assignment_id)

def get_all_staff_rosters():
    return db.session.query(StaffRoster).all()


def get_all_staff_rosters_by_complete():
    return db.session.query(StaffRoster).filter(StaffRoster.staff_check_in.isnot(None), StaffRoster.staff_check_out.isnot(None)).all()

def get_all_staff_rosters_json():
    rosters = get_all_staff_rosters()
    if not rosters:
        return []
    return [roster.__repr__() for roster in rosters]

def update_staff_check_in(assignment_id, check_in_time):
    assignment = get_staff_roster_by_id(assignment_id)
    if assignment:
        assignment.set_check_in(check_in_time)
        db.session.commit()
        return True
    return None

def update_staff_check_out(assignment_id, check_out_time):
    assignment = get_staff_roster_by_id(assignment_id)
    if assignment:
        assignment.set_check_out(check_out_time)
        db.session.commit()
        return True
    return None

def get_all_staff_rosters_by_complete_json():
    rosters = get_all_staff_rosters_by_complete()
    if not rosters:
        return []
    return [roster.__repr__() for roster in rosters]