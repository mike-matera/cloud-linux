"""
Generate personal Linux servers for students. 
"""

import pathlib
import json 
import argparse 
import textwrap
import nacl.secret
import nacl.exceptions
import nacl.encoding
import hashlib 
import datetime 

from cloud_linux.canvas import Canvas 

with open('./secrets/ca_key') as fh:
  crypt_key = hashlib.blake2b(
      fh.read().encode('utf-8'), 
      digest_size=nacl.secret.SecretBox.KEY_SIZE
    ).digest()

parser = argparse.ArgumentParser(description='Generate SSH keys.')
parser.add_argument('operator', choices=['generate', 'send'],
                    help='What to do.')
parser.add_argument('--only',
                    help='Only operate on a particular user/users (comma separated list).')

args = parser.parse_args()

canvas = Canvas() 

def encode_token(user, key):
  """Make a token."""
  return nacl.secret.SecretBox(key).encrypt(json.dumps({
          'user': user,
          'create': datetime.datetime.now().timestamp(),
      }).encode('utf-8'), encoder=nacl.encoding.URLSafeBase64Encoder).decode('utf-8')
    
def send_message(user, course_id, zip_file):
    """Send a key message to a user."""

    me = canvas.get_current_user()

    convo = canvas.create_conversation(user.id, 
        textwrap.dedent(f"""
        Hello student!

        This message has important information about how to login to the class Opus and Arya
        servers. In class I will show you how to use this link and how to enter the SSH 
        commands in this email. The URL below will take you to a site where you sign your
        SSH public key, allowing you to login without using a password. 

        **Keep this link secret** 

        https://opus.cis.cabrillo.edu/?token={encode_token(user.pw_name,crypt_key)}
    
        Opus is the server where you will do most assignments. To login to Opus use ssh 
        like this: 
        
        ssh {user.pw_name}@opus.cis.cabrillo.edu
        
        Your Arya server is a personal server. Each of you have a private TCP port. To log in 
        to Arya you need to use ssh like this:

        ssh {user.pw_name}@arya.cis.cabrillo.edu -p {user.tcp_port} 

        I'm looking forward to class! 

        Cheers
        ./m
        """), 
        subject="SSH Keys for Opus and Arya", 
        force_new=True,
        context_code=f"course_{course_id}",
    )


def main():

    if args.only is None:
        matcher = None
    else:
        matcher = lambda user: user.pw_name in args.only.split(',')
    
    canvas_users = canvas.course_users('cis-90', matcher=matcher) 

    output_dir = pathlib.Path(__file__).parent / 'secrets'

    if args.operator == 'generate':
        for course, user in canvas_users:
            print(f"User: {user} Unix User: {user.pw_name} Token: {encode_token(user.pw_name,crypt_key)}")

    elif args.operator == 'send':
        for course, user in canvas_users:
            send_message(user, course.id, output_dir / f'keys-{user.pw_name}.zip')

if __name__ == '__main__':
    main()
