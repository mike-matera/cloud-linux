"""
Generic flow of an interactive lab.
"""

from kroz.app import KrozApp
from kroz.flow import FlowContext
from kroz.flow.base import FlowResult, KrozFlowABC
from kroz.flow.question import Menu


def lab(package, debug=False):
    app = KrozApp(package.title, state_file=package.state, debug=debug)

    def main() -> None:
        app.show(package.welcome)

        while True:
            app.score = 0
            for name in package.walks:
                if (
                    FlowContext.flow_status(f"walk:{name}")
                    == FlowResult.CORRECT
                ):
                    app.score += 10 / len(package.walks)

            if FlowContext.flow_status("questions") == FlowResult.CORRECT:
                app.score += 10

            for name in package.lab:
                if (
                    FlowContext.flow_status(f"lab:{name}")
                    == FlowResult.CORRECT
                ):
                    app.score += 30 / len(package.lab)

            items = [
                (
                    f"walk:{key}",
                    f"{FlowContext.status_icon(f'walk:{key}')} {key}",
                    value,
                )
                for key, value in package.walks.items()
            ]
            items += [
                (
                    "questions",
                    f"{FlowContext.status_icon('questions')} Chapter questions",
                    package.questions,
                )
            ]
            items += [
                (
                    f"lab:{key}",
                    f"{FlowContext.status_icon(f'lab:{key}')} {key}",
                    value,
                )
                for key, value in package.lab.items()
            ]

            choice = FlowContext.run(
                Menu(
                    message="""
                    # Welcome!

                    **Choose a journey by entering a number and pressing `Enter`**
        """,
                    items=[i[1] for i in items],
                )
            )
            if choice.answer is not None:
                item = int(choice.answer) - 1
                with FlowContext(items[item][0]) as flow:
                    for f in items[item][2]:
                        if isinstance(f, KrozFlowABC):
                            flow.run(f)
                        elif issubclass(f, KrozFlowABC):
                            flow.run(f())

    app.main(main)
    return app.run()
