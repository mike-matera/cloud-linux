"""
Some lab called iolab or whatever.
"""

from kroz.app import KrozApp 
from kroz.question import Question
import asyncio 

class NumberGuess(Question):
    """Guess a number"""

    @property
    def text(self):
        return """
            # Guess a Number

            Guess a number between 1 and 100
        """

    def check(self, answer):
        return int(answer) == 69

WELCOME = """
# I/O Lab 

This is foo.
"""

app = KrozApp("The I/O Lab", WELCOME, total_score=100)

@app.setup
async def setup():
    for progress in range(0,100,2):
        app.progress(progress, f"Doing stuff: {progress}%")
        await asyncio.sleep(0.01)

@app.cleanup
async def cleanup():
    app.progress(None, "Deleting bifile")
    await asyncio.sleep(1)
    app.progress(None, "Removing files in Rando")
    await asyncio.sleep(2)

@app.main
async def main():
    q1 = NumberGuess(points=10)
    await app.ask(q1)

    for progress in range(0,100,2):
        app.progress(progress, f"Doing other stuff: {progress}%")
        await asyncio.sleep(0.01)

    await asyncio.sleep(3)

    q2 = NumberGuess(points=10)
    await app.ask(q2)

    q3 = NumberGuess(points=10)
    await app.ask(q3)

if __name__ == '__main__':
    app.run()
