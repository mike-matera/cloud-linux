# Lab: Create a Web Application 

In this lab you'll create a web application that runs on your Vagrant VM. The process of creating an application on a VM is manual. Later, you'll containerize this application by repeating these instruction in a `Dockerfile`. The application you will create is a Python application using [Flask](http://flask.pocoo.org/). Flask has a built-in web server and is all you need to create your own web application. 

## Step 1: Install Python and Pip

Your vagrant VM is minimal. You will have to install the pip package manager, which is used to install Python packages. 

```bash 
$ sudo apt update && sudo apt install -y python3-pip 
```

## Step 2: Install Flask 

Flask is installed with `pip3`, which works similarly to `apt`. 

```bash
$ pip3 install Flask 
```

## Step 3: You Web Application 

Create a directory for your application:

```bash
$ mkdir ~/MyApp
```

Copy-and-paste the python code below into a file called `app.py`:

```python
from flask import Flask
import subprocess
import sys
app = Flask(__name__)


@app.route('/')
def hello_world():
  html = '<html><h2>Hello World!</h2>'
  html += '<p>Python version:</p>'
  html += '<pre>' + str(sys.version) + '</pre>'
  html += '<p>Interfaces:</p>'
  html += '<pre>' + subprocess.check_output(['ip', 'addr']).decode('UTF-8') + '</pre>'
  html += '</html>'
  return html


if __name__ == '__main__':
  app.run(debug=True,host='0.0.0.0',port=80)
```

## Step 4: Run Your Application 

The web application uses port 80, so it must be run as root. Under normal circumstances you would want to run it using an unprivileged port. Run the application using the command below. You should see similar output:

```bash
$ sudo python3 ./app.py 
 * Serving Flask app "app" (lazy loading)
 * Environment: production
   WARNING: Do not use the development server in a production environment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Running on http://0.0.0.0:80/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 273-382-339
```

## Step 5: Access the Application 

You should now be able to see the application using your browser:

> [http://localhost:8080](http://localhost:8080)

## Turn In 

Turn in a screenshot of your browser. 
