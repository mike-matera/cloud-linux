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
            'name': user.pw_name,
            'comment': user.comment, 
            'groups': ['users', course],
            'uid': user.uid,
            'sid': user.sis_user_id,
        } for user in canvas.unix_users(course) 
    ]

print(yaml.dump({'users': users}))
