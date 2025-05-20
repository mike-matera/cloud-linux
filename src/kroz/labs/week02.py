"""
Lab for week 2.
"""

from kroz import KrozApp
from kroz.questions.week02 import (
    FreeMemory,
    NewYearFuture,
    OsRelease,
    WhatsUname,
    questions,
)

app = KrozApp("Anatomy of a Command", state_file="anatomy")


@app.main
def main():
    app.show(
        """
        # The Anatomy of a Command 

        This lab tests your knowledge of the material from the second week of class and 
        Chapter 1 of the book. You should familiarize yourself with the commands for the 
        week before you get going.

        This lab starts with some questions. Get them all correct to move on to the 
        challenges that are worth points. 
        """,
        classes="welcome",
        title="Welcome!",
    )

    for i, q in enumerate(questions):
        q.checkpoint = True
        app.ask(q)

    app.show(
        """
        # Challenges
        
        Congratulations. You've answered all the questions. The next part of 
        the lab will ask questions that you can only answer by running 
        commands. To complete this section you should either have another 
        terminal open or use the ctrl-s key to escape the lab to the shell.              
        
        """,
        classes="welcome",
    )

    app.ask(FreeMemory(key="total", points=5, checkpoint=True))
    app.ask(
        WhatsUname(
            key=WhatsUname.Keys.KERNEL_VERSION, points=5, checkpoint=True
        )
    )
    app.ask(OsRelease(key="NAME", points=5, checkpoint=True))
    app.ask(NewYearFuture(points=5, checkpoint=True))
    app.show(
        """
        # Complete! 

        You've completed the lab. Your score is {} out of {}. 

        You will receive a confirmation code on the command line to submit to canvas.

        """.format(app.score, 20),
        classes="welcome",
        title="Bye!",
    )


if __name__ == "__main__":
    code = app.run()
    print("Your confirmation code is:", code)
