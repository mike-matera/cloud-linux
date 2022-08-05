"""
Generate personal Linux servers for students. 
"""

import subprocess
import pathlib
import tempfile  
import zipfile 
import argparse 
import textwrap

from cloud_linux.canvas import Canvas 

parser = argparse.ArgumentParser(description='Generate SSH keys.')
parser.add_argument('operator', choices=['generate', 'send'],
                    help='What to do.')
parser.add_argument('--only',
                    help='Only operate on a particular user/users (comma separated list).')

args = parser.parse_args()

canvas = Canvas() 

def generate_key(user, signing_key, output_zip):
    """Generate SSH key ZIP."""
    with tempfile.TemporaryDirectory() as temp: 
        userdir = pathlib.Path(temp)
        subprocess.run(f'ssh-keygen -C "{user.pw_name}@opus" -N "" -f id_rsa', shell=True, check=True, cwd=userdir)
        subprocess.run(f'ssh-keygen -s {signing_key} -n {user.pw_name} -I {user.pw_name} id_rsa.pub', shell=True, check=True, cwd=userdir)

        with zipfile.ZipFile(output_zip, 'w') as keyzip:
            keyzip.write(userdir / 'id_rsa', arcname='id_rsa')
            keyzip.write(userdir / 'id_rsa.pub', arcname='id_rsa.pub')
            keyzip.write(userdir / 'id_rsa-cert.pub', arcname='id_rsa-cert.pub')


def send_message(user, course_id, zip_file):
    """Send a key message to a user."""

    me = canvas.get_current_user()

    canvas_key_file = me.upload(file=zip_file, parent_folder_path="conversation attachments", name=str(zip), on_duplicate="overwrite")

    convo = canvas.create_conversation(user.id, 
        textwrap.dedent(f"""
        Hello!
        
        This message has instructions for how to login to servers that I use to teach 
        my Linux and cloud classes. 

        ssh {user.pw_name}@arya.cis.cabrillo.edu -p {user.tcp_port} 
        ssh {user.pw_name}@opus.cis.cabrillo.edu 
        
        Please find the SSH keys attached. They will enable you to login.

        Cheers
        ./m
        """), 
        subject="Your SSH Keys for Opus and Arya", 
        attachment_ids=[canvas_key_file[1]["id"]],
        force_new=True,
        context_code=f"course_{course_id}",
    )


def main():

    if args.only is None:
        matcher = None
    else:
        matcher = lambda user: user.pw_name in args.only.split(',')
    
    canvas_users = canvas.course_users('cis-90', 'cis-91', matcher=matcher) 

    signing_key = pathlib.Path(__file__).parent / '../arya/secrets/ca_key'
    output_dir = pathlib.Path(__file__).parent / 'secrets'

    if args.operator == 'generate':
        for course, user in canvas_users:
            output_zip = output_dir / f'keys-{user.pw_name}.zip'
            if not output_zip.exists():
                generate_key(user, signing_key, output_zip)
            else:
                print(f"Skipping user {user.pw_name} in {course.sis_course_id}. Key already exists.")

    elif args.operator == 'send':
        for course, user in canvas_users:
            send_message(user, course.id, output_dir / f'keys-{user.pw_name}.zip')

if __name__ == '__main__':
    main()
