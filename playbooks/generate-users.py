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

from cloud_linux.canvas import Canvas 

canvas = Canvas() 

for course in ['cis-90']:
    users = [ {
            'name': cu.user.pw_name,
            'comment': cu.user.comment, 
            'groups': ['users', course],
            'uid': cu.user.uid,
            'sid': cu.user.sis_user_id,
        } for cu in canvas.course_users(course) 
    ]

print(yaml.dump({'users': users}))
