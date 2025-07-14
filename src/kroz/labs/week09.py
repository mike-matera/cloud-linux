"""
Manage files with permissions.
"""

import kroz
from kroz.questions.week09 import Islands2

WELCOME = """
# Sort the Islands

This lab builds on the original islands lab. It covers lessons X and Y. To do 
this lab you will need to understand the `chmod` and `chgrp` commands. 

Good luck!
"""

app = kroz.KrozApp("Sort the Islands", debug=True)


@app.main
def main():
    app.show(WELCOME, classes="welcome")
    Islands2().ask()


if __name__ == "__main__":
    quit(app.run())
