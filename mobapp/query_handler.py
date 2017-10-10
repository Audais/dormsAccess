from django.db import connection
from django.http import HttpResponse
from django.db import connection

from query import *


def validate_admin(data):
    cursor = connection.cursor()
    id = data["id"]
    password = data["password"]
    query = query_check_admin
    cursor.execute(query, (id, password))
    rows = cursor.fetchall()
    count = len(rows)
    cursor.close()
    if count == 1:
        return True
    return False


def validate_user(data):
    res = {}
    # get a cursor
    cursor = connection.cursor()
    # get details from form
    id = data["id"]
    password = data["password"]
    query = query_check_resident
    cursor.execute(query, (id, password))
    rows = cursor.fetchall()
    count = len(rows)
    # Check if a match
    if count == 1:
        res = {'response': 'success', 'result': 'resident'}
    else:
        query = query_check_visitor
        cursor.execute(query, (id, password))
        rows = cursor.fetchall()
        count = len(rows)
        if count == 1:
            res = {'response': 'success', 'result': 'visitor'}
    cursor.close()
    return res


def get_room(data):
    cursor = connection.cursor()
    query = query_get_room
    id = data["id"]
    cursor.execute(query, (id,))
    rows = cursor.fetchall()
    cursor.close()
    if len(rows) == 0:
        return 'visitor'
    return rows[0]


def get_resident_id(room):
    cursor = connection.cursor()
    query = query_get_resident_id
    cursor.execute(query, (room,))
    rows = cursor.fetchall()
    cursor.close()
    if len(rows) == 0:
        return 'visitor'
    return rows[0]

def get_visitor_access(id):
    cursor = connection.cursor()
    query = query_get_visitor_access
    cursor.execute(query, (id,))
    rows = cursor.fetchall()
    cursor.close()
    return rows


def get_visitors_id_access(room):
    cursor = connection.cursor()
    query = query_get_access
    # room = data["room"]
    cursor.execute(query, (room,))
    rows = cursor.fetchall()
    cursor.close()
    return rows


def get_visitor_name(visitor_id):
    cursor = connection.cursor()
    query = query_get_visitor_name
    cursor.execute(query, (visitor_id,))
    rows = cursor.fetchall()
    cursor.close()
    if len(rows) != 0:
        return rows[0]
    return (('UNKOWN'),)


def get_resident_name(resident_id):
    cursor = connection.cursor()
    query = query_get_resident_name
    cursor.execute(query, (resident_id,))
    rows = cursor.fetchall()
    cursor.close()
    return rows[0]


def sign_up_visitor(data):
    cursor = connection.cursor()
    query = query_signup_visitor
    id = data["id"]
    name = data["name"]
    password = data["password"]
    cursor.execute(query, (id, name, password))
    cursor.close()
    return True


def validate_new_user(user):
    # get a cursor
    cursor = connection.cursor()
    # get details from form
    id = user["id"]
    # query all users with this email
    query = query_check_user_exists
    cursor.execute(query, (id,))
    count = cursor.rowcount
    cursor.close()
    # Check if a match
    if count == 1:
        return False
    return True


def add_new_access(data):
    cursor = connection.cursor()
    query = query_add_access
    room = data["room"]
    id = data["id"]
    cursor.execute(query, (room, id))
    cursor.close()
    return True


def validate_visitor_access(data):
    cursor = connection.cursor()
    query = query_validate_access
    id = data["id"]
    room = data["room"]
    cursor.execute(query, (room, id))
    rows = cursor.fetchall()
    count = len(rows)
    cursor.close()
    if count == 1:
        return True
    return False


def check_visitor_exist(id):
    cursor = connection.cursor()
    query = query_check_user_exists
    cursor.execute(query, (id,))
    rows = cursor.fetchall()
    count = len(rows)
    cursor.close()
    if count == 1:
        return True
    return False


def remove_visitor_access(access_id):
    cursor = connection.cursor()
    query = query_remove_access
    cursor.execute(query, (access_id))
    cursor.close()
    return True

def remove_visitor_access_by_resident(visitor_id,room):
    cursor = connection.cursor()
    query = query_remove_access_by_resident
    cursor.execute(query, (visitor_id,room))
    cursor.close()
    return True

def remove_resident(resident_id):
    cursor = connection.cursor()
    query = query_remove_reident
    cursor.execute(query, (resident_id,))
    cursor.close()
    return True

def remove_visitor(visitor_id):
    cursor = connection.cursor()
    query = query_remove_visitor
    cursor.execute(query, (visitor_id,))
    cursor.close()
    return True



def check_resident_access(data):
    id = data["id"]
    cursor = connection.cursor()
    query = query_validate_resident_access
    cursor.execute(query, (id,))
    rows = cursor.fetchall()
    count = len(rows)
    cursor.close()
    if count == 1:
        return True
    return False


def get_all_residents():
    cursor = connection.cursor()
    query = query_get_all_residents
    cursor.execute(query, )
    rows = cursor.fetchall()
    cursor.close()
    return rows


def add_new_resident(data):
    cursor = connection.cursor()
    query = query_add_resident
    room = data["room"]
    id = data["resident_id"]
    name = data["name"]
    password = data["password"]
    validation_data = {'id': id}
    valid = check_resident_access(validation_data)
    if valid:
        return False
    cursor.execute(query, (id, name, room, password))
    cursor.close()
    return True


def add_to_blacklist(id, admin_id):
    cursor = connection.cursor()
    query = query_add_to_blacklist
    user_type = get_user_type(id)
    cursor.execute(query, (id, admin_id, user_type))
    cursor.close()
    return True


def remove_user_from_blacklist(user_id):
    cursor = connection.cursor()
    query = query_from_blacklist
    cursor.execute(query, (user_id,))
    cursor.close()
    return True


def get_all_blacklist():
    cursor = connection.cursor()
    query = query_get_all_blacklist
    cursor.execute(query, )
    rows = cursor.fetchall()
    cursor.close()
    return rows


def check_in_blacklist(id):
    cursor = connection.cursor()
    query = query_check_blacklist
    cursor.execute(query, (id,))
    rows = cursor.fetchall()
    count = len(rows)
    cursor.close()
    if count == 1:
        return True
    return False


def get_user_type(id):
    cursor = connection.cursor()
    query = query_validate_resident_access
    cursor.execute(query, (id,))
    rows = cursor.fetchall()
    count = len(rows)
    cursor.close()
    if count == 1:
        return 'resident'
    return 'visitor'

def get_all_visitors_access():
    cursor = connection.cursor()
    query = query_join_access_visitors
    cursor.execute(query, )
    rows = cursor.fetchall()
    cursor.close()
    return rows

def get_all_visitors():
    cursor = connection.cursor()
    query = query_get_all_visitors
    cursor.execute(query, )
    rows = cursor.fetchall()
    cursor.close()
    return rows


def get_all_log():
    cursor = connection.cursor()
    query = query_get_all_logs
    cursor.execute(query, )
    rows = cursor.fetchall()
    cursor.close()
    return rows

def get_room_logs(room):
    cursor = connection.cursor()
    query = query_get_room_logs
    cursor.execute(query,(room,) )
    rows = cursor.fetchall()
    cursor.close()
    return rows

def get_id_logs(id):
    cursor = connection.cursor()
    query = query_get_id_logs
    cursor.execute(query,(id,) )
    rows = cursor.fetchall()
    cursor.close()
    return rows

def insert_new_log(timestamp,date,room,id):
    cursor = connection.cursor()
    query = query = query_insert_logs
    cursor.execute(query, (timestamp,date,room,id))
    cursor.close()
    return True

def get_date_logs(date):
    cursor = connection.cursor()
    query = query_get_date_logs
    cursor.execute(query,(date,) )
    rows = cursor.fetchall()
    cursor.close()
    return rows
