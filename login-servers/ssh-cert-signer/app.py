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
import nacl.encoding

logging.basicConfig(level=logging.DEBUG)

app = flask.Flask(__name__)
os.umask(0o0077)

with open('./secrets/ca_key') as fh:
  crypt_key = hashlib.blake2b(
      fh.read().encode('utf-8'), 
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
  try:
    data = decode_token(token, crypt_key)
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


def encode_token(user, key):
  """Make a token."""
  return nacl.secret.SecretBox(key).encrypt(json.dumps({
          'user': user,
      }).encode('utf-8'), 
      encoder=nacl.encoding.URLSafeBase64Encoder).decode('utf-8')


def decode_token(token, key):
  """Get the token data."""
  return json.loads(
    nacl.secret.SecretBox(key).decrypt(
      token, encoder=nacl.encoding.URLSafeBase64Encoder,
    )
  )


if __name__ == '__main__':
  token = encode_token(sys.argv[2], crypt_key)
  print(f"Token: {token}")
  print(f"URL: {sys.argv[1]}/?token={token}")
