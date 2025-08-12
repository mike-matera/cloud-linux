"""
Manage files without permissions.
"""

import kroz
from kroz.flow import FlowContext
from kroz.questions.lesson05 import Islands

WELCOME = """
"""

app = kroz.KrozApp("Sort the Islands")


@app.main
def main():
    app.show(WELCOME, classes="welcome")
    with FlowContext("challenges", progress=True) as flow:
        flow.run(Islands(points=20))


if __name__ == "__main__":
    app.run()
