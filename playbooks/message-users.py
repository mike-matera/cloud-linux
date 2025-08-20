"""
Generate personal Linux servers for students.
"""

import argparse
import textwrap
from pathlib import Path

import canvasapi.folder

from cloud_linux.canvas import Canvas

parser = argparse.ArgumentParser(description="Generate SSH keys.")
parser.add_argument("operator", choices=["send"], help="What to do.")
parser.add_argument(
    "--only",
    help="Only operate on a particular user/users (comma separated list).",
)

args = parser.parse_args()


userdir = Path("./users")
assert userdir.exists(), (
    """Users directory doesn't exist. Generate keys first."""
)


canvas = Canvas()

me = canvas.get_current_user()
attachments_folder: canvasapi.folder.Folder = None  # type: ignore
for folder in me.get_folders():
    if folder.name == "conversation attachments":
        attachments_folder = folder
        break
assert isinstance(attachments_folder, canvasapi.folder.Folder), (
    """Error finding attachments folder."""
)


def send_message(user, course_id, zip_file):
    """Send a key message to a user."""

    ok, file = attachments_folder.upload(zip_file)
    assert ok, f"""Failed to upload file: {file}"""

    canvas.create_conversation(
        user.id,
        textwrap.dedent("""
Hello!

This message has files you need to SSH in to opus.cis.cabrillo.edu, the Linux
server for CIS-90. I'll show you how to use them on the first day of class, so
don't worry if they are unfamilar or you've never used SSH before. 
                
**These files are your class identity, keep them secret!** 

If you're already familiar with SSH, you will find the attached ZIP file
contains an SSH public and private key pair along with an SSH configuration
file. Simply copy them to your ~/.ssh directory. 
  
Opus is the server where you will do most assignments. To login to Opus use ssh
like this: 

ssh opus.cis.cabrillo.edu

I'm looking forward to class! 

Cheers 
./m
        """),
        subject="Your SSH keys for CIS-90",
        force_new=True,
        context_code=f"course_{course_id}",
        attachment_ids=[file["id"]],
    )


def main():
    if args.only is None:
        matcher = None
    else:
        matcher = lambda user: user.pw_name in args.only.split(",")  # noqa: E731

    canvas_users = canvas.course_users("cis-90", matcher=matcher)

    if args.operator == "send":
        for course, user in canvas_users:
            keys = userdir / f"{user.pw_name}_ssh.zip"
            assert keys.exists(), (
                """User's key does not exist. Generate it first."""
            )
            send_message(user, course.id, keys)


if __name__ == "__main__":
    main()
