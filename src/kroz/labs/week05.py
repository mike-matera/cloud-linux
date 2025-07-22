"""
Manage files without permissions.
"""

import kroz
from kroz.flow import FlowContext
from kroz.questions.week05 import Islands

WELCOME = """
# Sort the Islands

This lab builds on the original islands lab. It covers lessons X and Y. To do 
this lab you will need to understand the `chmod` and `chgrp` commands. 

Good luck!
"""

app = kroz.KrozApp("Sort the Islands")


@app.main
def main():
    app.show(WELCOME, classes="welcome")
    with FlowContext("challenges", progress=True) as flow:
        flow.run(Islands(points=20))


if __name__ == "__main__":
    app.run()
