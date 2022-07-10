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

canvas_cfg_file = pathlib.Path(pathlib.Path(os.environ['HOME']) / '.canvasapi')
canvas_cfg = None
canvas = None
logging.info(f"Loading canvas config file: {canvas_cfg_file}")
with open(canvas_cfg_file) as fh:
    canvas_cfg = yaml.load(fh, Loader=yaml.Loader)
canvas = Canvas(canvas_cfg['API_URL'], canvas_cfg['API_KEY'])

m = re.search(pattern='(\d+)$', string=args.group)
course_number = m.group(1)

users = []
for course_id in args.course:
    course = canvas.get_course(course_id)
    for user in course.get_users(include=['first_name', 'last_name', 'sis_user_id']):
        t = { 
            ord("'"): "",
            ord("."): "",
            ord("-"): "",
            ord(" "): "",
        }
        user_data = {
            'canvas_id': user.id, 
            'cabrillo_id': user.sis_user_id,
            'first': user.first_name.translate(t),
            'last': user.last_name.translate(t),
        }
        user_data['comment'] = f"{user_data['first']} {user_data['last'][0]}." 
        first_bound = min(3, len(user_data['first']))
        last_bound = min(3, len(user_data['last']))
        user_data['name'] = user_data['last'][0:last_bound].lower() + user_data['first'][0:first_bound].lower() + course_number
        user_data['clear_password'] = user_data['first'][0:2] + user_data['last'][0:2] + user_data['cabrillo_id'][-4:]
        user_data['password'] = crypt.crypt(user_data['clear_password'], f'$6${user_data["canvas_id"]}$')
        user_data['uid'] = int.from_bytes(hashlib.sha1((user_data['cabrillo_id'] + args.group).encode('utf-8')).digest(),
                byteorder='big'
            ) % (1 << 32)
        user_data['groups'] = ['users', args.group]
        users.append(user_data)

print(yaml.dump({'users': users}))
