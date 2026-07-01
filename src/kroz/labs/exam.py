"""
Helper for doing an exam
"""

import datetime
from dataclasses import dataclass

from kroz.app import KrozApp
from kroz.flow.base import FlowResult


@dataclass
class StateItem:
    number: int
    status: FlowResult
    score: float
    updated: datetime.datetime = datetime.datetime.now(datetime.UTC)


def exam(*questions, timelimit=0):
    app = KrozApp.running()
    now = datetime.datetime.now(datetime.UTC)
    if "started" not in app.state:
        app.state["started"] = now

    # Build initial status
    state: list[StateItem] = [
        StateItem(number=i, status=FlowResult.INCOMPLETE, score=0)
        for i in range(len(questions))
    ]
    state = app.state.get("status", default=state, store=True)

    app.set_score(sum([s.score for s in state]))

    if timelimit > 0:
        if now > app.state["started"] + datetime.timedelta(minutes=timelimit):
            return "You have no more time to do this test."

    try:
        for number, question in enumerate(questions):
            if state[number].status != FlowResult.CORRECT:
                state[number].status = question.show()
                if state[number].status == FlowResult.CORRECT:
                    if question.points is not None:
                        state[number].score = question.points
                        app.update_score(question.points)

                if timelimit > 0:
                    if datetime.datetime.now(datetime.UTC) > app.state[
                        "started"
                    ] + datetime.timedelta(minutes=timelimit):
                        return "You are out of time."

    finally:
        app.state["exited"] = datetime.datetime.now(datetime.UTC)
