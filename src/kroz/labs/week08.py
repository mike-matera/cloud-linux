from kroz.app import KrozApp
from kroz.flow import FlowContext
from kroz.flow.question import (
    MultipleChoiceQuestion,
)
from kroz.questions.lesson08 import (
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

    with FlowContext("challenges", progress=True, points=5) as flow:
        flow.run(RandomRando())
        flow.run(RandomDeleteMe())
        flow.run(RandomRandoTick())
        flow.run(DeepMessage())


if __name__ == "__main__":
    app.run()
