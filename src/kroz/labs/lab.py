"""
Generic flow of an interactive lab.
"""

import datetime
from dataclasses import dataclass

from kroz.app import KrozApp
from kroz.flow.base import FlowResult, KrozFlowABC
from kroz.flow.question import Menu


@dataclass
class QuestionItem:
    title: str
    series: tuple[KrozFlowABC]
    points: float


@dataclass
class StateItem:
    title: str
    status: FlowResult
    score: float
    updated: datetime.datetime = datetime.datetime.now(datetime.UTC)


def lab(package, debug=False):
    app = KrozApp(package.title, state_file=package.state, debug=debug)

    def main() -> None:
        # Assemble the questions...
        questions: list[QuestionItem] = (
            [
                QuestionItem(
                    title=key,
                    series=tuple(value),
                    points=10 / len(package.walks),
                )
                for key, value in package.walks.items()
            ]
            + [
                QuestionItem(
                    title="Chapter Questions",
                    series=tuple(package.questions),
                    points=10,
                )
            ]
            + [
                QuestionItem(
                    title=key,
                    series=tuple(value),
                    points=30 / len(package.lab),
                )
                for key, value in package.lab.items()
            ]
        )

        # Create the default state dictionary.
        state: dict[str, StateItem] = {
            q.title: StateItem(
                title=q.title, status=FlowResult.INCOMPLETE, score=0
            )
            for q in questions
        }

        # Recover the stored state if present. If not store the default.
        state = app.state.get("progress", default=state, store=True)

        # Put timestamps into the state file
        app.state.get(
            "first_started",
            default=datetime.datetime.now(datetime.UTC),
            store=True,
        )
        app.state["last_started"] = datetime.datetime.now(datetime.UTC)

        app.set_score(sum([s.score for s in state.values()]))

        app.show(package.__doc__, title="Welcome!", classes="welcome")

        while True:
            # TODO: Log each attempt

            menu = Menu(
                message="""
                    # Choose Your Path

                    **Choose a journey by entering a number and pressing `Enter`**
        """,
                items=[
                    f"[{state[i.title].status.value.short}] {i.title}"
                    for i in questions
                ],
            )
            menu.show()

            if menu.answer is not None:
                item = int(menu.answer) - 1

                # Last item is always exit
                if item == len(questions):
                    return

                # Execute the questions
                results = [
                    f.show() if isinstance(f, KrozFlowABC) else f().show()
                    for f in questions[item].series
                ]

                if all([r == FlowResult.CORRECT for r in results]):
                    state[questions[item].title].status = FlowResult.CORRECT
                    state[questions[item].title].score = questions[item].points
                else:
                    state[questions[item].title].status = FlowResult.SKIPPED
                    state[questions[item].title].score = 0

                app.state.store()
                app.set_score(sum([s.score for s in state.values()]))

    app.main(main)
    return app.run()
