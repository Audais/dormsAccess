
from django.db import connection
from django.http import HttpResponse
from django.db import connection

from query import *


def validate_resident(resident):
    # get a cursor
    cursor = connection.cursor()
    # get details from form
    id = resident["id"]
    password = resident["password"]
    query = query_check_resident
    cursor.execute(query, (id, password))
    rows = cursor.fetchall()
    count = len(rows)
    cursor.close()
    # Check if a match
    if count == 1:
        return True
    return False

def filter_courses(course_prefix):
    cursor = connection.cursor()

    if course_prefix is None:
        query = query_search_course_by_name
        cursor.execute(query, ("",))
    else:
        query = query_search_course_by_name
        cursor.execute(query, (course_prefix + '%',))
    results = {}
    for course in cursor.fetchall():
        results[course[0]] = course[1]
    cursor.close()
    return results