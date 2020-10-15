# A Docker Microservice 

The Python programming language makes it easy to run so-called microservices. Those are simple web applications that fulfill a single purpose. For example, you could write a microservice that lets you add and remove users to a host remotely. Microservices are popular in part because they're easy to write and deploy in containers. In this lab you'll write a microservice in Python and deploy it into a custom built container. 

## Part 1: Manually Customize a Container 

Creating a custom container starts with exploring how to build the container as if you were building a VM. In part 1 we will start with a bare Ubuntu container and build it up so it works just as we want it to. 

### Step 1.1: Setup

Let's start from a fresh directory: 

```
$ mkdir ~/HelloService
$ cd ~/HelloService
```

Now copy this Python code into a file called `hello.py`:

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
  app.run(debug=True,host='0.0.0.0',port=5000)
```

### Step 1.2: Create a Bare Container 

Now we'll crete a bare Ubuntu container that shares this directory:

```
$ docker run -it -p 5000:5000 -v $(pwd):/app --name hello-test ubuntu:20.04 /bin/bash
```

Running the command above will put you at the prompt of your new container. Try running the following command inside the container you will see an error.

```
$ python3 /app/hello.py 
```

Why do you get the error? 

### Step 1.3: Install Python 

There is no Python in a bare container! Install it with apt:

```
$ apt update 
$ apt install python3 
```

Again, try to run the app. What error do you see now? 

### Step 1.4: Install Python Libraries 

There's still an error because some Python components are missing. Python has it's own package manager called `pip`. First, install it with `apt`:

```
$ apt install python3-pip 
```

Once installed use `pip` to install `Flask`: 

```
$ pip3 install flask 
```

Now try to launch your app. You should see something like this:

```
$ python3 /app/hello.py 
 * Serving Flask app "hello" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 143-467-916
```

Verify that it's working by browsing to:

> [http://localhost:5000](http://localhost:5000)

But there's still a problem!

### Step 1.5 Install the `ip` Command 

The services uses the `ip` command which is not installed by default. Install it with apt.

```
$ apt install iproute2
```

Rerun your application. Success!

## Part 2: Write a `Dockerfile`

Customizing a container this way is great, but not permanent. If we want to deploy this container we should remember our steps and encode them in a `Dockerfile`. Our steps were:

1. Run `apt update` to get the latest package indexes
1. Install the packages:
    1. python3
    1. python3-pip 
    1. iproute2 
1. Install `flask` using `pip3` 

A `Dockerfile` is like a script that does the steps: 

### Step 2.1: Create a Dockerfile 

Stop the container you made and remove it. We only needed it to help us understand what do to. Create a `Dockerfile` in your HelloService directory with the contents:

```Dockerfile 
FROM ubuntu:20.04
MAINTAINER You "you@you.cis.cabrillo.edu"
RUN apt-get update -y
RUN apt-get install -y python3 python3-pip iproute2
RUN pip3 install flask
COPY . /app
WORKDIR /app
ENTRYPOINT ["python3"]
CMD ["hello.py"]
```

> Is embedding `app.py` the right thing to do? 

### Step 2.2: Build Your Container 

Build your custom container with the command:

```
$ docker build -t myapp:test1 
```

Notice that the customization is being done automatically!

### Step 2.2: Run Your Custom Container 

Let's try running your application: 

```
$ docker run -it --rm myapp:test1 
```

### Step 2.3: Update `hello.py`

What happens when we want to update `hello.py`? Do we have to rebuild completely? Try it. Change "Hello World" to your name and re-run `docker build` and `docker run`. 

**What happened?**

**Take a screenshot of your customized app.**

## Turn In 

A screenshot of your custom application running.
