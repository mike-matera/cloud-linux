"""
Generate UNIX users from a Canvas roster
"""

import subprocess
import tempfile
import textwrap
import zipfile
from pathlib import Path

import yaml

from cloud_linux.canvas import Canvas

canvas = Canvas()

users = [
    {
        "name": cu.user.pw_name,
        "comment": cu.user.comment,
        "groups": ["users", "cis-90"],
        "uid": cu.user.uid,
        "sid": cu.user.sis_user_id,
    }
    for cu in canvas.course_users("cis-90")
]

userdir = Path("./users")
if not userdir.exists():
    userdir.mkdir()

for user in users:
    sshzip = userdir / f"{user['name']}_ssh.zip"
    if not sshzip.exists():
        # Generate credentials
        with tempfile.TemporaryDirectory() as td:
            subprocess.run(
                f"ssh-keygen -t ed25519 -f id_opus_ed25519 -N '' -C {user['name']}@opus",
                cwd=td,
                shell=True,
                check=True,
            )
            with open(Path(td) / "config", "w") as fh:
                fh.write(
                    textwrap.dedent(f"""
                    Host opus.cis.cabrillo.edu
                        HostName opus.cis.cabrillo.edu
                        User {user["name"]}
                        IdentityFile ~/.ssh/id_opus_ed25519
                    """)
                )
            zipname = userdir / f"{user['name']}_ssh.zip"
            with zipfile.ZipFile(zipname, "w") as zipf:
                for file in [
                    "id_opus_ed25519",
                    "id_opus_ed25519.pub",
                    "config",
                ]:
                    zipf.write(Path(td) / file, arcname=file)

    # Read credentials from the zip file.
    with zipfile.ZipFile(sshzip, "r") as zipf:
        with zipf.open("id_opus_ed25519.pub") as fh:
            user["pub_key"] = fh.read().decode("utf-8").strip()
        with zipf.open("id_opus_ed25519") as fh:
            user["priv_key"] = fh.read().decode("utf-8").strip()

with open(userdir / "ansible-user-data.yaml", "w") as fh:
    fh.write(yaml.dump({"users": users}))
