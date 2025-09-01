"""
# Lesson 7: Input/Output Processing

After this lesson you should be able to:

- Use redirects
- Build command pipelines

Reading:

- Chapter 6

Commands:

1. `cat`
1. `sort`
1. `uniq`
1. `grep`
1. `wc`
1. `head`
1. `tail`
1. `tee`
1. `cut`

"""

from pathlib import Path

import textual.validation

import kroz.random as random
from kroz.flow.base import KrozFlowABC
from kroz.flow.interaction import Interaction
from kroz.flow.question import (
    MultipleChoiceQuestion,
    Question,
    ShortAnswerQuestion,
    TrueOrFalseQuestion,
)
from kroz.questions.lesson04 import WordInBigfile
from kroz.random.bigfile import random_big_file

title = "Getting Help"

state = "rtfm"


class CountOranges(Question):
    """Use grep and wc together to find lines with a word."""

    validators = [textual.validation.Integer()]
    placeholder = "Number of lines"

    @property
    def text(self):
        return f"""
        # Find a Word

        I have just created the file called:
         
        `{self._file.path}`

        How many lines contain the word "orange" or "Orange" where "orange" 
        is not a part of another word (i.e. "oranges" and "orangeade" do not 
        count)?

        Hint: Look in the manual for `grep`.
        """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._solution = None

    def setup_attempt(self):
        self._file = random_big_file(rows=10000, cols=100)
        self._file.setup()
        self._solution = int(
            self.shell(f"grep -iw orange {self._file.path}  | wc -l")
        )

    def cleanup_attempt(self):
        self._file.cleanup()

    def check(self, answer: str):
        assert int(answer) == self._solution, f"""
            # Not Correct 

            That was not the correct answer. The correct answer is {self._solution}
            but will change after you exit this screen. 
            """


class SortedWords(Question):
    """Sort words in a file."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @property
    def text(self):
        return f"""
        # Sort a Big File

        I have just created the file called:
         
        `{self._file.path}`

        If the file is sorted in alphabetical order what would be the first word? 
    """

    placeholder = "Word"

    def setup_attempt(self):
        self._file = random_big_file(rows=1000, cols=1)
        self._file.setup()
        self._word = self.shell(f"sort {self._file.path} | head -n 1").strip()

    def cleanup_attempt(self):
        self._file.cleanup()

    def check(self, answer):
        assert answer.strip() == self._word, (
            f"""That's not the correct answer. {self._word}"""
        )


class UniqueWords(Question):
    """Unique words in a file."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @property
    def text(self):
        return f"""
        # Unique Words

        I have just created the file called:
         
        `{self._file.path}`

        How many unique words are in it? 
    """

    validators = [textual.validation.Integer()]
    placeholder = "Number of unique words"

    def setup_attempt(self):
        self._file = random_big_file(rows=random.randint(2000, 4000), cols=1)
        self._file.setup()
        self._answer = int(
            self.shell(f"sort {self._file.path} | uniq | wc -l")
        )

    def cleanup_attempt(self):
        self._file.cleanup()

    def check(self, answer):
        assert int(answer) == self._answer, f"""
            # Not Correct 

            That was not the correct answer. The correct answer is {self._answer}
            but will change after you exit this screen. 
            """


walks: dict[str, list[KrozFlowABC]] = {
    "Build a pipeline to find spelling errors": [
        Interaction(
            """
# Building Pipelines 

Pipelines let you do some powerful things with just a few commands. They can be
tricky to build for beginners. The most important thing to remember is to build
them one command at a time from left to right. In this walk through we're going
to find and count the misspelled words in a document. 

Start by using the `spell` command to find all the misspelled words in the
`spellk` file:

```console
$ spell spellk
```
""",
            filter=lambda cmd: cmd.command == "spell"
            and cmd.args == ["spellk"],
        ),
        Interaction(
            """
The `spell` command prints words at it encounters them. Notice how the word
"chequer" is misspelled twice in the document so it's listed twice. Let's pipe
the output of `spell` to `sort` so that misspelled words appear in alphabetical
order:

```console
$ spell spellk | sort 
```
""",
            filter=lambda cmd: cmd[0].command == "spell"
            and cmd[0].args == ["spellk"]
            and cmd[1].command == "sort",
        ),
        Interaction(
            """
The `uniq` command removes duplicate words in a stream. There's a catch,
however. The `uniq` command only removes duplicates when they're on consecutive
lines. So anytime you see the `uniq` command in a pipeline it's preceded by the
`sort` command because sort guarantees that duplicates are consecutive:

```console
$ spell spellk | sort | uniq
```
""",
            filter=lambda cmd: cmd[0].command == "spell"
            and cmd[0].args == ["spellk"]
            and cmd[1].command == "sort"
            and cmd[2].command == "uniq",
        ),
        Interaction(
            """
Why make the words unique? Suppose we want to know how many misspelled words are
in a document. If we count the output of `spell` the count will be too high
because words that are misspelled multiple times will be double counted. Since
we used `sort` and `uniq` the output doesn't have any duplicates. Let's use `wc
-l` to count the misspelled words:

```console
$ spell spellk | sort | uniq | wc -l
```
""",
            filter=lambda cmd: cmd[0].command == "spell"
            and cmd[0].args == ["spellk"]
            and cmd[1].command == "sort"
            and cmd[2].command == "uniq"
            and cmd[3].command == "wc"
            and cmd[3].args == ["-l"],
        ),
    ],
    """Grepping for *love*.""": [
        Interaction(
            """
# The `grep` Command

The `grep` command looks for words inside of text files. It's one of the most 
iconic and useful UNIX commands. Let's use it to find out what poets write 
about love the most. Start by going into your `Poems` directory:

```console
$ cd ~/Poems
```
""",
            filter=lambda cmd: cmd.command == "cd"
            and cmd.cwd == Path().home() / "Poems",
        ),
        Interaction(
            """
Let's have grep look at the poems of Yeats:

```console
$ grep love Yeats/*
```

Notice that `grep` shows you every line that contains `love`.
""",
            filter=lambda cmd: cmd.command == "grep"
            and cmd.args[-2] == "love"
            and cmd.args[-1] == "Yeats/*",
        ),
        Interaction(
            """
There's one missing!

`grep` is case sensitive, so our last search finds "love" but not "Love". Let's
add the `-i` switch to make it find the word without regard to capitalization:

```console
$ grep -i love Yeats/*
```

Notice that there's one more line in the `old` poem.
""",
            filter=lambda cmd: cmd.command == "grep"
            and cmd.args[-3] == "-i"
            and cmd.args[-2] == "love"
            and cmd.args[-1] == "Yeats/*",
        ),
        Interaction(
            """
There are also extras!

`grep` doesn't care where `love` is. Notice how it also matched `loved` and 
`beloved`. Let's fix that with the `-w` (for *word*) switch: 

```console
$ grep -wi love Yeats/*
```

Now you should only see two lines.
""",
            filter=lambda cmd: cmd.command == "grep"
            and cmd.args[-3] == "-wi"
            and cmd.args[-2] == "love"
            and cmd.args[-1] == "Yeats/*",
        ),
    ],
    """Find the names of your classmates.""": [
        Interaction(
            """
# The `/etc/passwd` File

The `/etc/passwd` file (said *et-see password*) file contains the login
information for all of the users on a UNIX system. Contrary to its name it does
not contain passwords. Take a look at the file and you'll see your name listed:

```console
$ less /etc/passwd
```
""",
            filter=lambda cmd: cmd[0].command == "less"
            and cmd[0].args == ["/etc/passwd"],
        ),
        Interaction(
            """
There are mix of system accounts and user accounts in `/etc/passwd`. System
accounts are a topic for another day. User accounts all have the following
information separated by colons (`:`):

1. Login name (e.g. `mich431`)
1. The letter `x`
1. User ID number
1. Primary group ID number
1. Real name (e.g. Mike Matera)
1. Home directory (e.g. /home/cis90/mich431)
1. Shell (e.g. /usr/bin/bash)

Each entry looks like this: 

```
mich431:x:354520433:354520433:Michael Matera:/home/cis90/mich431:/bin/bash
```

Let's use the `grep` command to show us only the lines in `/etc/passwd` that 
contain the word `cis90`:

```console
$ grep cis90 /etc/passwd
```
""",
            filter=lambda cmd: cmd[0].command == "grep"
            and cmd[0].args[-2] == "cis90"
            and cmd[0].args[-1] == "/etc/passwd",
        ),
        Interaction(
            """
The `grep` command only shows us the lines we're interested in. But each line has
a bunch of data. How do we cut out parts we're not interested in? Well the `cut`
command. The cut command is a bit weird. It requires two pieces of information:

1. The *delimiter*, which is the character that separates the different pieces
   of data 
1. The field number which is the column of data we want to see

The delimiter in the password file is the colon (`:`). Field numbers start at 1
so if we want to see everyone's login name we do this:

```console
$ grep cis90 /etc/passwd | cut -d: -f1
```
""",
            filter=lambda cmd: cmd[0].command == "grep"
            and cmd[0].args[-2] == "cis90"
            and cmd[0].args[-1] == "/etc/passwd"
            and cmd[1].command == "cut"
            and "-d:" in cmd[1].args
            and "-f1" in cmd[1].args,
        ),
        Interaction(
            """
Let's look at field number 5. That's the user's real name:

```console
$ grep cis90 /etc/passwd | cut -d: -f5
```
""",
            filter=lambda cmd: cmd[0].command == "grep"
            and cmd[0].args[-2] == "cis90"
            and cmd[0].args[-1] == "/etc/passwd"
            and cmd[1].command == "cut"
            and "-d:" in cmd[1].args
            and "-f5" in cmd[1].args,
        ),
    ],
    """Top and bottom, right and left.""": [
        Interaction(
            """
What happens if you only want to see the beginning or end of a file? There're 
commands for that! The `head` and `tail` commands show you the top and bottom
lines of a text file. They were a bit more useful in the days of the hardware
terminals. 

Start by going to your `~/Poems/Neruda` directory: 

```console
$ cd ~/Poems/Neruda
```
""",
            filter=lambda cmd: cmd.command == "cd"
            and cmd.cwd == Path().home() / "Poems" / "Neruda",
        ),
        Interaction(
            """
The poem `artichoke` is pretty long. Let's see the first 10 lines with `head`:

```console
$ head artichoke
```
""",
            filter=lambda cmd: cmd.command == "head"
            and cmd.args == ["artichoke"],
        ),
        Interaction(
            """
We can ask `head` to give us any amount of lines. Let's see only one:

```console
$ head -n 1 artichoke
```
""",
            filter=lambda cmd: cmd.command == "head"
            and cmd.args == ["-n", "1", "artichoke"],
        ),
        Interaction(
            """
Now let's see the bottom few lines:

```console
$ tail artichoke
```
""",
            filter=lambda cmd: cmd.command == "tail"
            and cmd.args == ["artichoke"],
        ),
        Interaction(
            """
Now let's see the bottom lines:

```console
$ tail -n 1 artichoke
```
""",
            filter=lambda cmd: cmd.command == "tail"
            and cmd.args == ["-n", "1", "artichoke"],
        ),
        Interaction(
            """
What if we only want to see a particular line, say line #20? Well, we can ask 
`head` to show us the first 20 lines, then pipe that to `tail` and ask only for 
the last line. Try this:

```console
$ head -n 20 artichoke | tail -n 1
```
""",
            filter=lambda cmd: cmd[0].command == "head"
            and cmd[0].args == ["-n", "20", "artichoke"]
            and cmd[1].command == "tail"
            and cmd[1].args == ["-n", "1"],
        ),
        Interaction(
            """
This might seem silly here but it's handy. What if you only wanted the first 
word on line 20? Well we can use cut for that. 

> Notice how when we want the delimiter to be a space we use: `-d' '`

```console
$ head -n 20 artichoke | tail -n 1 | cut -d' ' -f1 
```
""",
            filter=lambda cmd: cmd[0].command == "head"
            and cmd[0].args == ["-n", "20", "artichoke"]
            and cmd[1].command == "tail"
            and cmd[1].args == ["-n", "1"]
            and cmd[2].command == "cut"
            and "-d' '" in cmd[2].args
            and "-f1" in cmd[2].args,
        ),
    ],
    """Don't cross the streams.""": [
        Interaction(
            """
In UNIX programs access the terminal using *streams*. In this walk you'll use 
the redirect operators `>` and `>>` to redirect the output of a program to a 
file. Start of by running the `find` command to see all the files on the system:

```console
$ find / 
```
""",
            filter=lambda cmd: cmd.command == "find" and cmd.args == ["/"],
        ),
        Interaction(
            """
Now try saving the names of files you find into a file:

```console
$ find / > allfiles.txt
```
""",
            filter=lambda cmd: cmd.command == "find"
            and cmd.args == ["/", ">", "allfiles.txt"],
        ),
        Interaction(
            """
Notice how there's still a lot of output? That's because you don't have 
permission to access all the files and directories on opus. Let's save the 
errors separately: 

```console
$ find / > allfiles.txt 2> errors.txt
```
""",
            filter=lambda cmd: cmd.command == "find"
            and cmd.args == ["/", ">", "allfiles.txt", "2>", "errors.txt"],
        ),
        Interaction(
            """
If you don't care about errors you can *throw them away* while also keeping your
screen clear. The special file `/dev/null` is used for this purpose:

```console
$ find / > allfiles.txt 2> /dev/null
```
""",
            filter=lambda cmd: cmd.command == "find"
            and cmd.args == ["/", ">", "allfiles.txt", "2>", "/dev/null"],
        ),
    ],
}


questions: list[KrozFlowABC] = [
    TrueOrFalseQuestion(
        "Every program on UNIX has one input *stream* and two output *streams*.",
        True,
    ),
    ShortAnswerQuestion(
        "What command finds a word or words in a file?",
        "grep",
    ),
    TrueOrFalseQuestion(
        "When using the `uniq` command in a pipeline it always comes after `sort`.",
        True,
    ),
    MultipleChoiceQuestion(
        """
You run this command:

```console
$ find . > one.txt 2> two.txt
```

Where does STDOUT go? 
""",
        "Into `one.txt`",
        "To the screen",
        "Into `two.txt`",
        "STDOUT is discarded",
    ),
    MultipleChoiceQuestion(
        """
You run this command:

```console
$ find . > one.txt 2> two.txt
```

Where does STDERR go? 
""",
        "Into `two.txt`",
        "Into `one.txt`",
        "To the screen",
        "STDERR is discarded",
    ),
    MultipleChoiceQuestion(
        """
You run this command:

```console
$ find . > one.txt 2>&1
```

Where does STDERR go? 
""",
        "Into `one.txt`",
        "Into `two.txt`",
        "To the screen",
        "STDERR is discarded",
    ),
]

lab: dict[str, list[KrozFlowABC]] = {
    "Find the word": [WordInBigfile(find=[None, 1])],
    "Count oranges": [CountOranges()],
    "Count unique words": [UniqueWords()],
    "Sort the words": [SortedWords()],
    "Find from the bottom": [WordInBigfile(from_bottom=True, find=[None, 1])],
    "Find from the right": [WordInBigfile(from_right=True)],
}
