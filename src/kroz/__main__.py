"""
KROZ CLI
"""

import argparse
import binascii
import importlib
import os
import re
import runpy
import sys
import uuid
from importlib.resources import files


def run(args) -> int:
    """Run a script or a module"""
    if args.debug:
        os.environ["TEXTUAL"] = "debug,devtools"

    from kroz.app import KrozApp

    module: str = args.module
    if module.endswith(".py"):
        # Run an app in a Python file.
        modns = runpy.run_path(module)
        app = "app"
    else:
        # Run an app after importing a module
        if ":" in module:
            mod, app = module.split(":")
        else:
            mod = module
            app = "app"
        modns = runpy.run_module(mod)

    if app not in modns:
        raise RuntimeError(f"""No application named "{app}" is in {module}""")

    if isinstance(modns[app], KrozApp):
        modns[app]._debug = args.debug
        modns[app].run()

    elif callable(modns[app]):
        newapp = KrozApp(module, debug=args.debug)
        newapp.main(modns[app])
        newapp.run()
    else:
        raise RuntimeError(
            f"""The member named "{app}" is not a KrozApp or a callable in {module}"""
        )
    return 0


def lesson_run(module: str, debug: bool) -> int:
    """Run a lesson module"""
    if debug:
        os.environ["TEXTUAL"] = "debug,devtools"

    from kroz.labs import lab

    mod = importlib.import_module(module)
    lab.lab(mod, debug=debug)
    return 0


def lesson(args) -> int:
    """Run a lesson module from the command line."""
    return lesson_run(args.module, args.debug)


def ask(args) -> int:
    """
    Ask a single question by creating an instance and a wrapper application. The
    question is instantiated using the supplied arguments which must be in the
    form "arg=value" for strings or "arg:=value" to use Python's `eval` function
    on value.
    """

    # Always enable debugging...
    os.environ["TEXTUAL"] = "debug,devtools"

    from kroz.app import KrozApp
    from kroz.flow import FlowContext

    module: str = args.module
    assert ":" in module, """Module must be in the format module:class"""

    mod, question = module.split(":")
    modmodule = importlib.import_module(mod)

    assert hasattr(modmodule, question), (
        f"""The question {question} is not in the module."""
    )

    kwargs = {"progress": True, "tries": 1}
    for extra in args.args:
        assert "=" in extra, (
            f"""Argument "{extra}" must be in the format parameter=value or parameter:=value"""
        )
        parts = extra.split("=")
        key, val = parts[0], "=".join(parts[1:])
        if key.endswith(":"):
            kwargs[key[:-1]] = eval(val, modmodule.__dict__, None)
        else:
            kwargs[key] = val

    app = KrozApp(module, state_file="ask", debug=True)

    def _main():
        with FlowContext("ask") as flow:
            flow.run(getattr(modmodule, question)(**kwargs))

    app.main(_main)
    print(app.run())
    return 0


def config(args) -> int:
    """Write the BASH configuration to the screen so it can be eval'd."""
    print(files("kroz.bash").joinpath("setup.sh").read_text())
    return 0


def secrets_main(args):
    """
    Decode confirmation numbers from stdin.
    """
    from kroz.secrets import (
        ConfirmationCode,
        EncryptedStateFile,
        embedded_key,
        has_embedded_key,
    )

    constraints: list[tuple] = []
    if args.constraint is not None:
        for const in args.constraint:
            if (m := re.match(r"(\w+)=(\S+)", const)) is None:
                raise ValueError(f"Invalid constraint: {const}")
            constraints.append(
                (
                    m.group(1),
                    m.group(2),
                )
            )

    if args.key is not None:
        print("Using command line key.")
        key = args.key
    else:
        if has_embedded_key():
            print("Using embedded key.")
            key = embedded_key()
        else:
            print("Using machine key.")
            key = str(uuid.getnode())

    Bold = "\x1b[1m"
    Reset = "\x1b[0m"
    F_LightGreen = "\x1b[92m"
    F_LightRed = "\x1b[91m"
    F_Default = "\x1b[39m"
    B_Default = "\x1b[49m"
    B_Black = "\x1b[40m"

    if args.file is None:
        vault = ConfirmationCode(key=key)
        while True:
            line = None
            got = ""
            while line != ".":
                line = input("> ")
                got += line.strip()
            got = got.replace("\n", "")
            got = got.replace(" ", "")
            got = got.replace("\t", "")
            for i in range(len(got)):
                for j in range(i + 1, len(got)):
                    try:
                        data = vault.validate(got[i : j + 1])
                        for const in constraints:
                            if const[0] not in data:
                                raise ValueError(
                                    f"""Constraint failed: data does not contain: {const[0]}"""
                                )
                            if data[const[0]] != const[1]:
                                raise ValueError(
                                    f"""Constraint failed: {const[0]}: {data[const[0]]} != {const[1]}"""
                                )
                        print("\n")
                        print(Bold, F_LightGreen, B_Black, sep="", end="")
                        print(data)
                        print(B_Default, F_Default, Reset, sep="", end="")
                        print("\n")
                    except binascii.Error:
                        pass
                    except AssertionError:
                        pass
                    except ValueError as e:
                        print(e)
                    except Exception as e:
                        print("DEBUG:", type(e))
    else:
        import pprint

        pprint.pprint(EncryptedStateFile(key=key, filename=args.file)._data)


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="kroz",
        description="Command line tools for the KROZ player.",
        epilog="Nothing happens here.",
    )

    subparsers = parser.add_subparsers(
        title="subcommands",
        description="valid subcommands",
        help="additional help",
        required=True,
    )

    secrets_parser = subparsers.add_parser(
        "secrets", help="Decode secrets from STDIN."
    )
    secrets_parser.add_argument(
        "-k",
        "--key",
        type=str,
        required=False,
        help="The key used for operations.",
    )
    secrets_parser.add_argument(
        "-f", "--file", type=str, help="The encrypted file to read."
    )
    secrets_parser.add_argument(
        "-c",
        "--constraint",
        action="append",
        type=str,
        help="Constrain a particular value. Values should be key=value. Can be used multiple times.",
    )
    secrets_parser.set_defaults(func=secrets_main)

    runparser = subparsers.add_parser("run", help="Run a module or class.")
    runparser.add_argument(
        "-d", "--debug", action="store_true", help="Run in debugging mode."
    )
    runparser.add_argument(
        "module", help="The name of a script or a module to execute."
    )
    runparser.set_defaults(func=run)

    askparser = subparsers.add_parser(
        "ask", help="Ask a single question.", description=ask.__doc__
    )
    askparser.add_argument("module", help="The name of a class to execute.")
    askparser.add_argument(
        "args", nargs="*", help="An argument to the initializer."
    )
    askparser.set_defaults(func=ask)

    configparser = subparsers.add_parser(
        "config",
        help="Echo BASH configuration to the screen.",
        description=ask.__doc__,
    )
    configparser.set_defaults(func=config)

    lessonparser = subparsers.add_parser("lesson", help="Run a lesson module.")
    lessonparser.add_argument(
        "-d", "--debug", action="store_true", help="Run in debugging mode."
    )
    lessonparser.add_argument("module", help="The module to execute.")
    lessonparser.set_defaults(func=lesson)

    args = parser.parse_args()
    return args.func(args)


def cis90() -> int:
    parser = argparse.ArgumentParser(
        prog="cis90",
        description="Get your work done in Mike's cis-90 class.",
        epilog="No one ever leaves the island.",
    )

    parser.add_argument(
        "assignment", help="The name of the assignment you wish to run."
    )

    args = parser.parse_args()

    if args.assignment == "config":
        config(None)
        return 0

    print("Loading. Please wait...")
    sys.stdout.flush()

    from kroz.labs import lab

    if args.assignment == "commands":
        import kroz.questions.lesson02 as do_lab

        lab.lab(do_lab)
    elif args.assignment == "filesystem":
        import kroz.questions.lesson03 as do_lab

        lab.lab(do_lab)
    elif args.assignment == "files":
        import kroz.questions.lesson04 as do_lab

        lab.lab(do_lab)
    elif args.assignment == "islands":
        import kroz.questions.lesson05 as do_lab

        lab.lab(do_lab)
    elif args.assignment == "commands":
        import kroz.questions.lesson06 as do_lab

        lab.lab(do_lab)
    elif args.assignment == "io":
        import kroz.questions.lesson07 as do_lab

        lab.lab(do_lab)
    elif args.assignment == "boss":
        import kroz.questions.lesson08 as do_lab

        lab.lab(do_lab)
    elif args.assignment == "perms":
        import kroz.questions.lesson09 as do_lab

        lab.lab(do_lab)
    elif args.assignment == "processes":
        import kroz.questions.lesson10 as do_lab

        lab.lab(do_lab)
    elif args.assignment == "environment":
        import kroz.questions.lesson11 as do_lab

        lab.lab(do_lab)
    elif args.assignment == "editor":
        import kroz.questions.lesson12 as do_lab

        lab.lab(do_lab)
    elif args.assignment == "scripts":
        import kroz.questions.lesson13 as do_lab

        lab.lab(do_lab)

    else:
        print(f"Assignment not found: {args.assignment}")
    return 0


if __name__ == "__main__":
    exit(main())
