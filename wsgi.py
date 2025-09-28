import click, pytest, sys, datetime
from flask import Flask
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.models import Staff
from App.main import create_app
from App.controllers import ( create_user, get_all_users_json, get_all_users, initialize )
from App.controllers.admin import ( create_admin, get_all_admins, get_admin, admin_create_roster, admin_update_roster, admin_delete_roster, admin_get_rosters_by_staff, admin_get_all_rosters  )
from App.controllers.staff_roster import ( assign_roster_to_staff, get_all_staff_rosters, get_all_staff_rosters_json, update_staff_check_in, update_staff_check_out )


# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def init():
    initialize()
    print('database intialized')

'''
User Commands
'''

# Commands can be organized using groups

# create a group, it would be the first argument of the comand
# eg : flask user <command>
user_cli = AppGroup('user', help='User object commands') 


# Then define the command and any parameters and annotate it with the group (@)
@user_cli.command("create-staff", help="Creates a user")
@click.argument("username", default="rob")
@click.argument("password", default="robpass")
@click.argument("position", default="Staff")
@click.argument("email", default="rob@mail")
def create_user_command(username, password, position, email):
    create_user(username, password, position, email)
    print(f'{username} created!')


@user_cli.command("create-admin", help="Creates an admin user")
@click.argument("username", default="alice")
@click.argument("password", default="alicepass")
@click.argument("email", default="admin@mail")
def create_admin_command(username, password, email):
    create_admin(username, password, email)
    print(f'Admin {username} created!')

# this command will be : flask user create bob bobpass

@user_cli.command("create-roster", help="Creates a roster for a staff (admin only), time is in the format HH:MM:SS")
@click.argument("admin_id", type=int, default=2)
@click.argument("staff_id", type=int, default=1)
@click.argument("shift_date", default="2023-10-10")
@click.argument("shift_start", default="09:00:00")
@click.argument("shift_end", default="17:00:00")
def create_roster_command(admin_id, staff_id, shift_date, shift_start, shift_end):

    shift_date_obj = datetime.datetime.strptime(shift_date, "%Y-%m-%d").date()
    shift_start_obj = datetime.datetime.strptime(shift_start, "%H:%M:%S").time()
    shift_end_obj = datetime.datetime.strptime(shift_end, "%H:%M:%S").time()
    roster = admin_create_roster(admin_id, staff_id, shift_date_obj, shift_start_obj, shift_end_obj)
    if not roster:
        print(f'Admin with id {admin_id} not found. Roster not created.')
    else:
        staffroster = assign_roster_to_staff(staff_id, roster.id, shift_date_obj, shift_start_obj, shift_end_obj)
        if not staffroster:
            print(f'Failed to assign roster to staff {staff_id}.')
        print(f'Roster for staff {staff_id} on {shift_date} created!')

@user_cli.command("get-admins", help="Get all admins")
def get_admins_command():
    admins = get_all_admins()
    if not admins:
        print('No admins found.')
    else:
        for admin in admins:
            print(admin.get_json())

@user_cli.command("get-rosters", help="Get all rosters (admin only)")
@click.argument("admin_id", type=int, default=2)
def get_rosters_command(admin_id):
    rosters = admin_get_all_rosters(admin_id)
    if not rosters:
        print(f'Admin with id {admin_id} not found or no rosters available.')
    else:
        for roster in rosters:
            print(roster.get_json())

@user_cli.command("staff-check-in", help="Staff check in to their assigned roster, time is in the format HH:MM:SS")
@click.argument("assignment_id", type=int, default=1)
@click.argument("check_in_time", default="09:00:00")
def staff_check_in_command(assignment_id, check_in_time):
    shift_start_obj = datetime.datetime.strptime(check_in_time, "%H:%M:%S").time()
    success = update_staff_check_in(assignment_id, shift_start_obj)
    if success is None:
        print(f'Assignment with id {assignment_id} not found. Check-in failed.')
    else:
        print(f'Staff checked in for assignment {assignment_id} at {check_in_time}.')

@user_cli.command("staff-check-out", help="Staff check out of their assigned roster, time is in the format HH:MM:SS")
@click.argument("assignment_id", type=int, default=1)
@click.argument("check_out_time", default="17:00:00")
def staff_check_out_command(assignment_id, check_out_time):
    shift_end_obj = datetime.datetime.strptime(check_out_time, "%H:%M:%S").time()
    success = update_staff_check_out(assignment_id, shift_end_obj)
    if success is None:
        print(f'Assignment with id {assignment_id} not found. Check-out failed.')
    else:
        print(f'Staff checked out for assignment {assignment_id} at {check_out_time}.')
    
@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == 'string':
        print(get_all_users())
    else:
        print(get_all_users_json())

app.cli.add_command(user_cli) # add the group to the cli


'''
Test Commands
'''

test = AppGroup('test', help='Testing commands') 

@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))
    

app.cli.add_command(test)