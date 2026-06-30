"""
Helper for doing an exam
"""

import datetime

from kroz.app import KrozApp
from kroz.flow.base import FlowResult


def exam(*questions, timelimit=0):
    app = KrozApp.running()
    now = datetime.datetime.now(datetime.UTC)
    if "started" not in app.state:
        app.state["started"] = now

    if timelimit > 0:
        if now > app.state["started"] + datetime.timedelta(minutes=timelimit):
            return "You have no more time to do this test."

    try:
        for question in questions:
            result = question.show()
            if result == FlowResult.CORRECT:
                if question.points is not None:
                    app.update_score(question.points)

            if timelimit > 0:
                if datetime.datetime.now(datetime.UTC) > app.state[
                    "started"
                ] + datetime.timedelta(minutes=timelimit):
                    return "You are out of time."

    finally:
        app.state["exited"] = datetime.datetime.now(datetime.UTC)
