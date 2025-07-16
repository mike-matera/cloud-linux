"""
Walk through for week 3: The File System
"""

import kroz
from kroz.flow.base import FlowContext
from kroz.flow.interaction import Interaction

app = kroz.KrozApp("The File System")


@app.main
def main():
    app.show("""
             # Welcome !

             This walk through will get you familiar with navigating the filesystem. 

             **Press `Enter` to get started**
             """)

    with FlowContext() as flow:
        flow.run(
            Interaction(
                """ 
    # There's No Place Like Home

    Your *home directory* is the place where you keep your personal files. It's also
    the initial *working directory* of the shell when you log in over `ssh`. On opus
    your home directory has files that are used as examples in the class, Including
    the `Poems` directory. 

    The `cd` command navigates your shell through the file system. Running `cd` with
    no arguments navigates to your home directory. Start off by navigating to your 
    home directory:

    ```console
    $ cd 
    ```

    **Before you go further you should be in your home directory.** 
    """,
                lambda cmd: cmd.command == "cd" and cmd.args == [],
            )
        )

    return "Congratulations, your journey is complete."


if __name__ == "__main__":
    app.run()
