"""
Some lab called iolab or whatever.
"""

from kroz.app import KrozApp 
from kroz.question import Question

class NumberGuess(Question):
    """Guess a number"""

    @property
    def text(self):
        return """
            # Guess a Number

            Guess a number between 1 and 100
        """ * 100

    def check(self, answer):
        return int(answer) == 69

WELCOME = """
# I/O Lab 

This is foo.
""" * 100

app = KrozApp("The I/O Lab", WELCOME)

@app.setup
async def setup():
    print("Doing setup.")

@app.cleanup
async def cleanup():
    print("Doing cleanup.")

@app.main
async def main():
    q1 = NumberGuess()
    await app.ask(q1)

if __name__ == '__main__':
    app.run()
