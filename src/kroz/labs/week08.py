from kroz import KrozApp
from kroz.question import (
    MultipleChoiceQuestion,
)
from kroz.questions.week08 import (
    DeepMessage,
    RandomDeleteMe,
    RandomRando,
    RandomRandoTick,
)

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
    RandomRando(points=10, checkpoint="1").ask()
    RandomDeleteMe(points=10, checkpoint="2").ask()
    RandomRandoTick(points=10, checkpoint="3").ask()
    DeepMessage(points=10, checkpoint="4").ask()


if __name__ == "__main__":
    app.run()
