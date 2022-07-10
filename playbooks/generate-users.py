"""
Generate UNIX users from a Canvas roster
"""

import pathlib 
import logging 
import yaml 
import os
import argparse
import re
import crypt
import hashlib 
import yaml 

from canvasapi import Canvas

parser = argparse.ArgumentParser(description='Add users from a Canvas course.')
parser.add_argument('group',
                    help='Unix group for the users.')
parser.add_argument('course', nargs='+',
                    help='Canvas Course IDs')

args = parser.parse_args()

canvas = Canvas(os.environ['CANVAS_API_URL'], os.environ['CANVAS_API_KEY'])

m = re.search(pattern='(\d+)$', string=args.group)
course_number = m.group(1)

users = []
for course_id in args.course:
    course = canvas.get_course(course_id)
    for user in course.get_users(include=['first_name', 'last_name']):
        t = { 
            ord("'"): "",
            ord("."): "",
            ord("-"): "",
            ord(" "): "",
            ord('"'): "",
        }

        first = user.first_name.translate(t)
        last = user.last_name.translate(t)

        user_data = {}
        user_data['comment'] = f"{first} {last[0]}." 
        first_bound = min(3, len(first))
        last_bound = min(3, len(last))
        user_data['name'] = last[0:last_bound].lower() + first[0:first_bound].lower() + course_number
        user_data['uid'] = int.from_bytes(hashlib.sha1((str(user.id) + args.group).encode('utf-8')).digest(),
                byteorder='big'
            ) % (1 << 32)
        user_data['groups'] = ['users', args.group]
        users.append(user_data)

print(yaml.dump({'users': users}))
