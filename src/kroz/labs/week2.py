"""
Lab for week 2.
"""

from kroz import KrozApp
from kroz.questions.week2 import questions

app = KrozApp("Anatomy of a Command", state_file="anatomy")

WELCOME = """
# The Anatomy of a Command 

This lab tests your knowledge of the material from the second week of class and 
Chapter 1 of the book. You should familiarize yourself with the commands for the 
week before you get going. 
"""

GOODBYE = """
# Complete! 

You've completed the lab. Your score is {} out of {}. 

You will receive a confirmation code on the command line to submit to canvas.
"""


@app.main
def main():
    app.show(WELCOME, classes="welcome", title="Welcome!")
    for i, q in enumerate(questions):
        q.checkpoint = True
        app.ask(q)
    app.show(GOODBYE.format(app.score, 20), classes="welcome", title="Bye!")


if __name__ == "__main__":
    code = app.run()
    print("Your confirmation code is:", code)
