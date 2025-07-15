"""
KROZ CLI
"""

import argparse
import runpy
from importlib.resources import files

from kroz.app import KrozApp
from kroz.secrets import cli as secrets_cli


def run(args) -> int:
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
        raise RuntimeError(f"""No application named "{app}" is in {module}""")
    if not isinstance(modns[app], KrozApp):
        raise RuntimeError(
            f"""The member named "{app}" is not a KrozApp in {module}"""
        )
    modns[app]._debug = args.debug
    print(modns[app].run())
    return 0


def ask(args) -> int:
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
        parts = extra.split("=")
        key, val = parts[0], "=".join(parts[1:])
        if key.endswith(":"):
            kwargs[key[:-1]] = eval(val, modns, None)
        else:
            kwargs[key] = val

    app = KrozApp(module, debug=True)

    def _main():
        modns[question](**kwargs).ask()
        return ""

    app.main(_main)
    print(app.run())
    return 0


def config(args) -> int:
    """Write the BASH configuration to the screen so it can be eval'd."""
    print(files("kroz.bash").joinpath("setup.sh").read_text())
    return 0


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

    configparser = subparsers.add_parser(
        "config",
        help="Echo BASH configuration to the screen.",
        description=ask.__doc__,
    )
    configparser.set_defaults(func=config)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    exit(main())
