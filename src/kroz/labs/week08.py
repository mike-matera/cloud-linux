from kroz import KrozApp
from kroz.flows.question import (
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
    RandomRando(points=10, checkpoint="1").show()
    RandomDeleteMe(points=10, checkpoint="2").show()
    RandomRandoTick(points=10, checkpoint="3").show()
    DeepMessage(points=10, checkpoint="4").show()

    return app.confirmation()


if __name__ == "__main__":
    app.run()
