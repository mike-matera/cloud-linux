"""
A web application to sign SSH public keys.
"""

import os
import sys
import json
import flask 
import base64
import logging
import pathlib
import tempfile
import hashlib
import subprocess
import urllib.parse
import nacl.secret
import nacl.exceptions

logging.basicConfig(level=logging.DEBUG)

app = flask.Flask(__name__)
os.umask(0o0077)

key = os.environ['TOKEN_KEY']
crypt_key = hashlib.blake2b(
    key.encode('utf-8'), 
    digest_size=nacl.secret.SecretBox.KEY_SIZE
  ).digest()


@app.route('/', methods=['GET', 'POST'])
def make_key():

  if flask.request.method == 'GET':
    token = flask.request.args.get("token")
  else:
    token = flask.request.form.get("token")

  if token is None:
    return flask.render_template('index.html')

  # Validate Token
  box = nacl.secret.SecretBox(crypt_key)
  try:
    data = json.loads(
      box.decrypt(
        base64.b64decode(token)
      )
    )
    logging.debug(f"Sign key for: {data}")
  except Exception as e:
    logging.warning(e)
    return flask.render_template('index.html', error="Invalid token.")

  pubkey = flask.request.form.get("pubkey")
  if pubkey is None:
    return flask.render_template('keygen.html', username=data['user'], token=token)

  with tempfile.TemporaryDirectory() as temp:
      temppath = pathlib.Path(temp)

      with open(temppath / 'id_rsa.pub', 'w') as fh:
        fh.write(pubkey)

      kg = subprocess.run(
        f"""ssh-keygen -s ./secrets/ca_key -n "{data['user']}" -I "{data['user']}" {temppath / "id_rsa.pub"}""", 
        shell=True,
      )

      if (kg.returncode != 0):
          return flask.render_template('keygen.html', username=data['user'], token=token, pubkey=pubkey, error="Invalid public key!")

      return flask.send_file(temppath / 'id_rsa-cert.pub', as_attachment=True)


if __name__ == '__main__':
  token = base64.b64encode(
      nacl.secret.SecretBox(crypt_key).encrypt(json.dumps({
          'user': sys.argv[2],
          'class': sys.argv[3],
          'port': sys.argv[4],
      }).encode('utf-8'))
    ).decode('utf-8')
  print(f"Token: {token}")
  print(f"URL: {sys.argv[1]}/?token={urllib.parse.quote(token)}")
