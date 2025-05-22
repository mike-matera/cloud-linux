"""
KROZ CLI
"""

import argparse
import runpy
from kroz.secrets import cli as secrets_cli
from kroz.app import KrozApp


def run(args):
    """Run a script or a module"""
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
        raise RuntimeError(
            f"""No application named "{app}" is in module {mod}"""
        )
    if not isinstance(modns[app], KrozApp):
        raise RuntimeError(
            f"""The member named "{app}" is not a KrozApp in module {mod}"""
        )
    modns[app]._debug = args.debug
    modns[app].run()


def ask(args):
    """
    Ask a single question by creating an instance and a wrapper application. The
    question is instantiated using the supplied arguments which must be in the
    form "arg=value" for strings or "arg:=value" to use Python's `eval` function
    on value.
    """
    module: str = args.module
    assert ":" in module, """Module must be in the format module:class"""

    mod, question = module.split(":")
    modns = runpy.run_module(mod)

    assert question in modns, (
        f"""The question {question} is not in the module."""
    )

    kwargs = {}
    for extra in args.args:
        assert "=" in extra, (
            f"""Argument "{extra}" must be in the format parameter=value"""
        )
        key, val = extra.split("=")
        if key.endswith(":"):
            kwargs[key[:-1]] = eval(val, modns, None)
        else:
            kwargs[key] = val

    app = KrozApp(module)

    def _main():
        app.ask(modns[question](**kwargs))

    app.main(_main)
    app.run()


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="KROZ CLI",
        description="Command line tools for the KROZ player.",
        epilog="Nothing happens here.",
    )

    subparsers = parser.add_subparsers(
        title="subcommands",
        description="valid subcommands",
        help="additional help",
        required=True,
    )

    secrets_cli(subparsers)

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

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    exit(main())
