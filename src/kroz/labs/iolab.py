"""
Some lab called iolab or whatever.
"""

from kroz.app import KrozApp 

app = KrozApp("The I/O Lab")

@app.setup
def setup():
    print("Doing setup.")

@app.cleanup
def cleanup():
    print("Doing cleanup.")

@app.main
def main():
    print("Doing main.")

if __name__ == '__main__':
    app.run()
