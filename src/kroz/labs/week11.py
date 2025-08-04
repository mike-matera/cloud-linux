from kroz import KrozApp
from kroz.flow import FlowContext
from kroz.questions.week11 import MakeScript, RunYourScript

app = KrozApp("Processes", state_file="processlab")

WELCOME = """
# Your Favorite Editory 

This lab will give you practice editing.
"""


@app.main
def main():
    app.show(WELCOME, classes="welcome")

    with FlowContext("challenges", progress=False, points=4) as flow:
        flow.run(MakeScript(progress=False))
        flow.run(RunYourScript())


if __name__ == "__main__":
    app.run()
