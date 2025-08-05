"""
# Lesson 12. Love Your Text Editor

- Edit a file with vi, emacs and nano

Reading:

- Chapter 12
"""

import os
import pathlib

from kroz.app import KrozApp
from kroz.flow.interaction import CommandLineCommand, InteractionABC
from kroz.flow.question import (
    Question,
)


class MakeScript(Question):
    text = """
# Make a Script 

Create a text file called `home` in your `~/bin` directory using your favorite 
editor. Make it contain the following lines:

```
cd
clear
echo This is the home directory of $LOGNAME
echo =======================================
ls -F
```

Use the `chmod` command to set the permissions on the file to `rwxr-xr-x`.
"""

    placeholder = "Press Enter when ready..."

    def check(self, answer):
        path = pathlib.Path.home() / "bin" / "home"
        assert path.exists(), """I can't find `~/bin/home`"""

        with open(path) as fh:
            lines = fh.readlines()

        assert lines[0].strip() == "cd", (
            """The `cd` command isn't on the first line of your file."""
        )
        assert lines[1].strip() == "clear", (
            """The `clear` command isn't on the second line of your file."""
        )

        assert lines[-1].strip() == "", (
            """Your file **must** end with an empty line."""
        )

        lastline = 0
        for lastline in range(1, len(lines)):
            if lines[-lastline].strip() != "":
                break

        assert lines[-lastline].strip() == "ls -F", (
            """The `ls -F` command isn't on the last non-empty line of your file."""
        )

        assert os.stat(path).st_mode & 0o777 == 0o755, (
            """Your file has the wrong permissions."""
        )


class RunYourScript(InteractionABC):
    text = """
# You Made a Command! 

If you successfully answered the last question you now have a new command called `home`.
Run the `home` command at the command line and see what it does.
"""

    def on_command(self, command: CommandLineCommand) -> bool:
        return command.strip() == "home"


class FixSpelling(Question):
    file_text = """
Alice was beginning to got very tired of sitting by her sister on the bank, and
of having nothing to do: once or twice she had peeped into the book her sister
was reading, but it had no pictures or conversations in it, “and what is the use
of a book,” thought Alice “without pitures or conversations?”

    So she was considering in her own mind (as well as she could, for the hot day
    made her feel very sleepy and stupid), whether the pleasure of making a
    daisy-chain would be worth the trouble of getting up and picking the daisies,
    when suddenly a White Rabbit with pink eyes ran cloose by her.
    
        There was nothing so very remarkable in that; nor did Alice think it so very
        much out of the way to hear the Rabbit say to itself, “Oh dear! Oh dear! I shall
        be late!” (when she thought it rover afterwards, it occurred to her that she
        ought to have wondered at this, but at the time it all seemed quite natural);
        but when the Rabbit actually took a watch out of its waistcoat-pocket, and
        looked at it, and then hurried on, Alice started to her feet, for it flashed
        across her mind that she had never before seen a rabbit with either a
        waistcoat-pocket, or a watch to take out of it, and burning with curiosity, she
        ran across the field after it, and fortnately was just in time to see it pop
        down a large rabbit-hole under the hedge.
"""

    @property
    def text(self):
        return f"""
# Alice's Adventures in Wonderland 

I have created a file called `{self._alice()}`. Run the `spell` command on it to
reveal spelling errors. *Note all the misspelled words*. 

Use your favorite editor to edit file and do the following:

1. Correct all the misspelled words.
1. Use consistent indentation. Make all lines start from the left most column.
1. Fix the typo: "Alice was beginning to got very tired…" (change "got" to
   "get")
1. Fix the typo: "when she thought it rover afterwards…" (change to "rover" to
   "over")

When you have made all the fixes press `Enter`. **If you want to start over
delete `~/alice.txt` and restart the lab.**
"""

    def _alice(self) -> pathlib.Path:
        return KrozApp.appconfig("default_path") / "alice.txt"

    def setup(self) -> None:
        if not self._alice().exists():
            with open(self._alice(), "w") as fh:
                fh.write(self.file_text)

    def check(self, answer):
        alice = self._alice()
        assert alice.exists(), f"""I can't find the file: {alice}"""
        with open(self._alice()) as fh:
            alice_txt = fh.read()

        assert "pitures" not in alice_txt, (
            """You didn't correct the word "pitures" """
        )
        assert "cloose" not in alice_txt, (
            """You didn't correct the word "cloose" """
        )
        assert "fortnately" not in alice_txt, (
            """You didn't correct the word "fortnately" """
        )
        assert "Alice was beginning to get very tired" in alice_txt, (
            """You didn't correct "got" to "get" """
        )
        assert "when she thought it over afterwards" in alice_txt, (
            """You didn't correct "rover" to "over" """
        )

        for line in alice_txt.split("\n"):
            if line.strip() != "":
                assert not line.startswith(" "), (
                    """I see a line that isn't all the way to the left."""
                )
