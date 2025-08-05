from kroz import KrozApp
from kroz.flow import FlowContext
from kroz.questions.lesson10 import (
    ChildFind,
    ThisGrandparent,
    ThisParent,
    ThisProcess,
)

app = KrozApp("Processes", state_file="processlab")

WELCOME = """
# Processes 

This lab will give you practice managing processes.
"""


@app.main
def main():
    app.show(WELCOME, classes="welcome")

    with FlowContext("challenges", progress=True, points=4) as flow:
        flow.run(ThisProcess())
        flow.run(ThisParent())
        flow.run(ThisGrandparent())
        flow.run(ChildFind(type=ChildFind.ResourceType.COUNT))
        flow.run(ChildFind(type=ChildFind.ResourceType.CPU))


if __name__ == "__main__":
    app.run()
