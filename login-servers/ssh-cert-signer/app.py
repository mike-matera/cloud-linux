"""
A web application to sign SSH public keys.
"""

import os
import re
import sys
import json
import flask 
import logging
import pathlib
import tempfile
import hashlib
import subprocess
import zipfile
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

  pubkey = pubkey.strip()
  if (m := re.search('^ssh-(rsa|ed25519)\s', pubkey)) is not None:
    keytype = m.group(1)
  else:
    return flask.render_template('keygen.html', username=data['user'], token=token, pubkey=pubkey, error="Invalid public key! (Invalid type)")

  with tempfile.TemporaryDirectory() as temp:
      temppath = pathlib.Path(temp)

      with open(temppath / f'id_{keytype}.pub', 'w') as fh:
        fh.write(pubkey)

      with open('./secrets/ca_key.pub') as pub:
        with open(temppath / 'known_hosts', 'w') as fh:
          fh.write(f"""@cert-authority * {pub.read().strip()}""")

      kg = subprocess.run(
        f"""ssh-keygen -s ./secrets/ca_key -n "{data['user']}" -I "{data['user']}" {temppath / f"id_{keytype}.pub"}""", 
        shell=True,
      )

      if (kg.returncode != 0):
          return flask.render_template('keygen.html', username=data['user'], token=token, pubkey=pubkey, error="Invalid public key!")
      
      with zipfile.ZipFile(temppath / 'opus-signed.zip', mode='w') as zip:
        zip.write(temppath / f'id_{keytype}-cert.pub', arcname=f'id_{keytype}-cert.pub')
        zip.write(temppath / 'known_hosts', arcname='known_hosts')

      return flask.send_file(temppath / 'opus-signed.zip', as_attachment=True)


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
