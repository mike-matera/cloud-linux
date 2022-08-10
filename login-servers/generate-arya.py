"""
Generate personal Linux servers for students. 
"""

import re
import json
import subprocess
import argparse 

from cloud_linux.canvas import Canvas 

parser = argparse.ArgumentParser(description='Make personal servers from a Canvas course.')
parser.add_argument('operator', choices=['update', 'upgrade', 'stop', 'purge'],
                    help='What to do.')

args = parser.parse_args()

helm_users = json.loads(
    subprocess.run("""helm list -n login-servers --filter 'arya-.*' -o json""", shell=True, stdout=subprocess.PIPE, check=True).stdout
)

canvas = Canvas() 
canvas_users = { courseuser.user.pw_name: courseuser.user for courseuser in canvas.course_users('cis-90', 'cis-91') } 

helm_install = """helm -n login-servers {op} arya-{user} cloud-native-server/cloud-server \
    --values values-arya.yaml --set ssh.existingSecret=cis-ca-key \
    --set user={user} \
    --set userID={userid} \
    --set service.port={port} \
    && sleep 5 \
    && kubectl -n login-servers wait --for=condition=ready --timeout=10m pod -l app.kubernetes.io/instance=arya-{user}
    """

helm_uninstall = """helm -n login-servers uninstall {user}"""

if args.operator == 'update':
    # Create users who are missing. 
    for user in set(canvas_users.keys()) - { x["name"] for x in helm_users }:
        subprocess.run(helm_install.format(
            op='install',
            user=user,
            userid=canvas_users[user].uid,
            port=canvas_users[user].tcp_port,
        ), shell=True, check=True)

    # Delete users who dropped. 
    for user in { x["name"] for x in helm_users } - set(canvas_users.keys()):
        subprocess.run(helm_uninstall.format(
            user=user
        ), shell=True, check=True)

elif args.operator == 'upgrade':
    for user in { x["name"] for x in helm_users }:
        subprocess.run(helm_install.format(
            op='upgrade',
            user=user,
            userid=canvas_users[user].uid,
            port=canvas_users[user].tcp_port,
        ), shell=True, check=True)

elif args.operator == 'stop':
    for user in { x["name"] for x in helm_users }:
        subprocess.run(helm_uninstall.format(
            user=user
        ), shell=True, check=True)

elif args.operator == 'purge':
    for user in { x["name"] for x in helm_users }:
        subprocess.run(helm_uninstall.format(
            user=user
        ), shell=True, check=False)

    pvcs = json.loads(
        subprocess.run("kubectl -n login-servers get pvc -o json", shell=True, check=True, stdout=subprocess.PIPE).stdout
    )
    for pvc in pvcs['items']:
        if 'arya' in pvc['metadata']['name']:
            subprocess.run(f"kubectl -n login-servers delete pvc {pvc['metadata']['name']}", shell=True, check=False)
        
