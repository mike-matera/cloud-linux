from kroz import KrozApp
from kroz.question import (
    MultipleChoiceQuestion,
)
from kroz.questions.week08 import DeepMessage, RandomDeleteMe, RandomRando, RandomRandoTick


app = KrozApp("Like a BOSS!", state_file="bosslab")

WELCOME = """
# Use Linux Like a BOSS!

In this lab you will use the advanced command features you learned in X Y 
"""


class Test(MultipleChoiceQuestion):
    pass


@app.main
def main():
    app.show(WELCOME, classes="welcome")
    app.ask(RandomRando(points=10, checkpoint="1"))
    app.ask(RandomDeleteMe(points=10, checkpoint="2"))
    app.ask(RandomRandoTick(points=10, checkpoint="3"))
    app.ask(DeepMessage(points=10, checkpoint="4"))


if __name__ == "__main__":
    app.run()
