"""
Helper functions for the Python Canvas library 
"""

import os
import re 
import logging
import pathlib
import yaml
import canvasapi
import typing 
import hashlib 
from collections import namedtuple

class UnixUser(canvasapi.user.User):
    """
    A view of a user with stuff I need to make UNIX accounts. 
    """

    def __init__(self, requester, attributes):
        super().__init__(requester, attributes)
        self._hash_id = hashlib.sha1((f'{self.sis_user_id}').encode('utf-8')).digest()

    def _stable_id(self, begin, end):
        return str((int.from_bytes(self._hash_id, byteorder='little') % (end-begin)) + begin)

    @property
    def uid(self):
        """A UNIX user ID that's stable based on the student and course."""
        return self._stable_id(10000, (1<<31))

    @property
    def tcp_port(self):
        """A stable port for a multi-ssh app."""
        return self._stable_id(10000, (1<<16))

    @property
    def pw_name(self):
        """A lame name."""
        f, _ = self.name.lower().split(' ', 1)
        f = re.sub('[^a-z]', '', f)[0:3]
        return f"{f}{self.sis_user_id[-4:]}"

    @property
    def comment(self):
        return re.sub('[:]', '', self.short_name)


class Canvas(canvasapi.Canvas):
    """
    Extensions that I keep re-writing for making Canvas easier to use.     
    """

    CourseUser = namedtuple("CourseUser", "course user")

    def __init__(self, base_url:str = None, access_token:str = None) -> canvasapi.Canvas:
        """
        Get a Canvas instance with optional environment or file configuration. 
        """

        canvas = None

        if base_url is not None and access_token is not None:
            super().__init__(base_url=base_url, access_token=access_token)

        elif os.environ.get('CANVAS_API_URL') is not None and os.environ.get('CANVAS_API_KEY') is not None:
            super().__init__(os.environ['CANVAS_API_URL'], os.environ['CANVAS_API_KEY'])

        elif (pathlib.Path(os.environ['HOME']) / '.canvasapi').exists():
            canvas_cfg_file = pathlib.Path(os.environ['HOME']) / '.canvasapi'
            logging.info(f"Loading canvas config file: {canvas_cfg_file}")
            with open(canvas_cfg_file) as fh:
                canvas_cfg = yaml.safe_load(fh)
            super().__init__(canvas_cfg['API_URL'], canvas_cfg['API_KEY']) 

        else:
            raise ValueError('No URL/KEY given.')


    def find_course(self, matcher:typing.Callable = None) -> typing.Generator[canvasapi.course.Course, None, None]: 
        """
        Search active courses where you are the instructor. 
        """
        for course in self.get_courses(enrollment_type='teacher', enrollment_state='active'):
            if matcher is None or matcher(course):
                yield course 

    def unix_users(self, *args, matcher=None) -> typing.Generator[UnixUser, None, None]:
        """
        Deprecate.
        """
        for course_id in args:
            for course in self.find_course(lambda x: course_id.lower() in x.course_code.lower()):
                return (user for user in course.get_users() if matcher is None or matcher(user))

    def course_users(self, *args, matcher=None) -> typing.Generator[CourseUser, None, None]: 
        for course_id in args:
            for course in self.find_course(lambda x: course_id.lower() in x.course_code.lower()):
                yield from (
                    Canvas.CourseUser(course=course, user=user) 
                    for user in course.get_users() 
                    if matcher is None or matcher(user)
                )

# Monkey patch the Canvas API to give me the users I want.
canvasapi.user.User = UnixUser
