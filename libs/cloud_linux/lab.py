"""
Module with helpers for Linux tests.
"""

import getpass
import platform
import sys
import pathlib
import traceback
import datetime 
import argparse
import textwrap 
import logging 

from cloud_linux.secrets import JsonBox

class Formatting:
    Bold = "\x1b[1m"
    Dim = "\x1b[2m"
    Italic = "\x1b[3m"
    Underlined = "\x1b[4m"
    Blink = "\x1b[5m"
    Reverse = "\x1b[7m"
    Hidden = "\x1b[8m"
    # Reset part
    Reset = "\x1b[0m"
    Reset_Bold = "\x1b[21m"
    Reset_Dim = "\x1b[22m"
    Reset_Italic = "\x1b[23m"
    Reset_Underlined = "\x1b[24"
    Reset_Blink = "\x1b[25m"
    Reset_Reverse = "\x1b[27m"
    Reset_Hidden = "\x1b[28m"


class Color:
    # Foreground
    F_Default = "\x1b[39m"
    F_Black = "\x1b[30m"
    F_Red = "\x1b[31m"
    F_Green = "\x1b[32m"
    F_Yellow = "\x1b[33m"
    F_Blue = "\x1b[34m"
    F_Magenta = "\x1b[35m"
    F_Cyan = "\x1b[36m"
    F_LightGray = "\x1b[37m"
    F_DarkGray = "\x1b[90m"
    F_LightRed = "\x1b[91m"
    F_LightGreen = "\x1b[92m"
    F_LightYellow = "\x1b[93m"
    F_LightBlue = "\x1b[94m"
    F_LightMagenta = "\x1b[95m"
    F_LightCyan = "\x1b[96m"
    F_White = "\x1b[97m"
    # Background
    B_Default = "\x1b[49m"
    B_Black = "\x1b[40m"
    B_Red = "\x1b[41m"
    B_Green = "\x1b[42m"
    B_Yellow = "\x1b[43m"
    B_Blue = "\x1b[44m"
    B_Magenta = "\x1b[45m"
    B_Cyan = "\x1b[46m"
    B_LightGray = "\x1b[47m"
    B_DarkGray = "\x1b[100m"
    B_LightRed = "\x1b[101m"
    B_LightGreen = "\x1b[102m"
    B_LightYellow = "\x1b[103m"
    B_LightBlue = "\x1b[104m"
    B_LightMagenta = "\x1b[105m"
    B_LightCyan = "\x1b[106m"
    B_White = "\x1b[107m"


class LinuxLabQuestion:

    def ask():
        pass 

    def check():
        pass 


class LinuxLab:

    def __init__(self, name, secret, debug=False):
        self.score = 0
        self.total = 0
        self.debug = debug
        self.questions = []
        self.box = JsonBox(secret)
        self.progress_file = pathlib.Path.home() / '.linuxlabs' / name
        self.progress_file.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
        try:
            with open(self.progress_file) as fh:
                self.progress = self.box.decrypt(fh.read())
            assert self.progress['user'] == getpass.getuser()
            assert self.progress['host'] == platform.node()
            assert self.progress['cmd'] == sys.argv[0]
            self.progress['date'] = round(datetime.datetime.now(datetime.timezone.utc).timestamp())
        except:
            # Clear on any error
            self.progress = {
                'user': getpass.getuser(),
                'host': platform.node(),
                'cmd': sys.argv[0],
                'date': round(datetime.datetime.now(datetime.timezone.utc).timestamp()),
            }

    def print_error(self, *stuff):
        print(Formatting.Bold, Color.F_LightRed, sep='', end='')
        print(*stuff)
        print(Color.F_Default, Formatting.Reset, sep='', end='')

    def print_success(self, *stuff):
        print(Formatting.Bold, Color.F_LightGreen, sep='', end='')
        print(*stuff)
        print(Color.F_Default, Formatting.Reset, sep='', end='')

    def question(self, func):
        def _wrapper(points, *args, **kwargs):
            if self.total > -1:
                self.total += points

            if self.progress.get(f"question.{func.__name__}") is not None:
                self.score += points
                print(Formatting.Bold, end='')
                print(func.__name__, " (", points, " points)", sep='', end="")
                self.print_success(" **Complete**")
                print(Formatting.Reset, end='')
                return

            try:
                while True:
                    try:
                        print(Formatting.Bold, end='')
                        print(func.__name__, " (", points, " points)", sep='', end="")
                        print(Formatting.Reset, end='')
                        if (func.__doc__ is not None):
                            print("\n" + func.__doc__.format(**kwargs))
                        rval = func(**kwargs)
                        self.score += points
                        with open(self.progress_file, 'w') as fh:
                            self.progress[f"question.{func.__name__}"] = 1
                            self.progress['score'] = self.score
                            self.progress['total'] = self.total
                            fh.write(self.box.encrypt(self.progress))
                        self.print_success('** Correct **')
                        return rval
                    except Exception as e:
                        self.print_error('Error:', e)
                        if self.debug:
                            traceback.print_exc()
                        got = ask('Try again? (Y/n)? ').strip().lower()
                        if got.startswith('n'):
                            return None

            except (KeyboardInterrupt, EOFError) as e:
                exit(-1)

        return _wrapper

def do_question(question, debug=True):
    q = question()
    while True:
        print(textwrap.dedent(f"""
        {Formatting.Bold}Question: {question.__name__}{Formatting.Reset}
        """))

        prompt = q.setup()
        if prompt is not None:
            input(f"""\n{Color.F_LightYellow}{Formatting.Bold}{prompt}{Color.F_Default}""")
        try:
            q.check()
            print(f"""{Formatting.Bold}{Color.F_LightGreen}✅ Correct{Formatting.Reset}{Color.F_Default}""")
            break
        except Exception as e:
            print(textwrap.dedent(f"""
            {Formatting.Bold}{Color.F_LightRed}❌ Incorrect{Formatting.Reset}
            Error message: {e}
            """).strip())
            if debug:
                traceback.print_exc()



def main():
    """
    Run the lab
    """
    parser = argparse.ArgumentParser(description='Run a Linux lab.')
    #parser.add_argument('integers', metavar='N', type=int, nargs='+',
    #                    help='an integer for the accumulator')
    #parser.add_argument('--sum', dest='accumulate', action='store_const',
    #                    const=sum, default=max,
    #                    help='sum the integers (default: find the max)')
    #
    #args = parser.parse_args()
    #print(args.accumulate(args.integers))

    FORMAT = '🤖 %(message)s'
    logging.basicConfig(format=FORMAT, level=logging.INFO)


    import cloud_linux.labs.questions
    do_question(cloud_linux.labs.questions.boss.DeleteTheQuotes)
    do_question(cloud_linux.labs.questions.boss.DeleteTheMs)

if __name__ == '__main__':
    main()
    