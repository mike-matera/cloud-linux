"""
Testing Flows
"""

from unittest.mock import Mock

import pytest

from kroz.app import KrozApp
from kroz.flow.base import FlowContext, KrozFlowABC
from kroz.flow.question import Question


@pytest.fixture
def kroz_app(mocker, tmp_path):
    app = KrozApp("Testing", config_dir=tmp_path, default_path=tmp_path)

    # Mock interfaces so we don't have to run the app.
    mocker.patch("kroz.app.KrozApp.running", new=Mock(return_value=app))
    mocker.patch("kroz.app.KrozApp.show", new=Mock(return_value="show-return"))

    app._setup_user_app()

    yield app


def test_flow_correct(kroz_app):
    """Test a flow with correct result"""

    class qq(Question):
        points = 10

        def check(self, answer: str) -> None:
            return

    result = FlowContext.run(qq())
    assert isinstance(result, KrozFlowABC.Result)
    assert result.result == KrozFlowABC.Result.QuestionResult.CORRECT
    assert result.message == "show-return"
    assert kroz_app.show.call_count == 2
    assert kroz_app.score == 10
    assert "Success" == kroz_app.show.call_args_list[1].args[0]._text_title
    assert "checkpoints" in kroz_app.state
    assert 0 == len(kroz_app.state["checkpoints"])


@pytest.mark.parametrize("do_tries", [1, 2, 3])
def test_flow_failure(kroz_app, do_tries):
    """Test a flow with failure result"""

    class qq(Question):
        points = 10
        tries = do_tries

        def check(self, answer: str) -> None:
            raise ValueError("")

    result = FlowContext.run(qq())
    assert isinstance(result, KrozFlowABC.Result)
    assert result.result == KrozFlowABC.Result.QuestionResult.INCORRECT
    assert result.message == "show-return"
    assert kroz_app.show.call_count == do_tries * 2
    assert kroz_app.score == 0
    assert "Error" in kroz_app.show.call_args_list[1].args[0]._text_title
    assert "checkpoints" in kroz_app.state
    assert 0 == len(kroz_app.state["checkpoints"])


def test_flow_skip(mocker, kroz_app):
    """Test a flow with skipped result"""

    mocker.patch("kroz.app.KrozApp.show", new=Mock(return_value=None))

    class qq(Question):
        points = 10

        def check(self, answer: str) -> None:
            raise ValueError("")

    result = FlowContext.run(qq())
    assert isinstance(result, KrozFlowABC.Result)
    assert result.result == KrozFlowABC.Result.QuestionResult.SKIPPED
    assert result.message is None
    assert kroz_app.show.call_count == 1
    assert kroz_app.score == 0
    assert "checkpoints" in kroz_app.state
    assert 0 == len(kroz_app.state["checkpoints"])


def test_flow_checkpoint_success(kroz_app):
    class qq(Question):
        points = 10
        checkpoint = True

        def check(self, answer: str) -> None:
            return

    result1 = FlowContext.run(qq())
    assert "checkpoints" in kroz_app.state
    assert 1 == len(kroz_app.state["checkpoints"])
    assert "qq0" in kroz_app.state["checkpoints"]
    assert "message" in kroz_app.state["checkpoints"]["qq0"]
    assert "show-return" == kroz_app.state["checkpoints"]["qq0"]["message"]
    assert "result" in kroz_app.state["checkpoints"]["qq0"]
    assert (
        "QuestionResult.CORRECT"
        == kroz_app.state["checkpoints"]["qq0"]["result"]
    )
    assert kroz_app.show.call_count == 2
    assert "_sequence" in kroz_app.state
    assert 1 == kroz_app.state["_sequence"]
    assert kroz_app.score == 10

    # Reset the sequence, show and score
    kroz_app.state["_sequence"] = 0
    kroz_app.show.reset_mock()
    kroz_app.score = 0

    result2 = FlowContext.run(qq())
    assert result1 == result2
    assert kroz_app.show.call_count == 0
    assert kroz_app.score == 10


def test_checkpoint_failure(kroz_app):
    """Test a flow with failure result"""

    class qq(Question):
        points = 10
        tries = 1
        checkpoint = True

        def check(self, answer: str) -> None:
            raise ValueError("")

    result1 = FlowContext.run(qq())
    assert "checkpoints" in kroz_app.state
    assert 1 == len(kroz_app.state["checkpoints"])
    assert "qq0" in kroz_app.state["checkpoints"]
    assert "message" in kroz_app.state["checkpoints"]["qq0"]
    assert "show-return" == kroz_app.state["checkpoints"]["qq0"]["message"]
    assert "result" in kroz_app.state["checkpoints"]["qq0"]
    assert (
        "QuestionResult.INCORRECT"
        == kroz_app.state["checkpoints"]["qq0"]["result"]
    )
    assert kroz_app.show.call_count == 2
    assert "_sequence" in kroz_app.state
    assert 1 == kroz_app.state["_sequence"]

    # Reset the sequence, show and score
    kroz_app.state["_sequence"] = 0
    kroz_app.show.reset_mock()
    kroz_app.score = 0

    result2 = FlowContext.run(qq())
    assert result1 == result2
    assert kroz_app.show.call_count == 2  # The question was re-shown
    assert kroz_app.score == 0


def test_checkpoint_skip(mocker, kroz_app):
    """Test a flow with skipped result"""

    mocker.patch("kroz.app.KrozApp.show", new=Mock(return_value=None))

    class qq(Question):
        points = 10
        checkpoint = True

        def check(self, answer: str) -> None:
            raise ValueError("")

    result1 = FlowContext.run(qq())
    assert "checkpoints" in kroz_app.state
    assert 1 == len(kroz_app.state["checkpoints"])
    assert "qq0" in kroz_app.state["checkpoints"]
    assert "message" in kroz_app.state["checkpoints"]["qq0"]
    assert kroz_app.state["checkpoints"]["qq0"]["message"] is None
    assert "result" in kroz_app.state["checkpoints"]["qq0"]
    assert (
        "QuestionResult.SKIPPED"
        == kroz_app.state["checkpoints"]["qq0"]["result"]
    )
    assert kroz_app.show.call_count == 1
    assert "_sequence" in kroz_app.state
    assert 1 == kroz_app.state["_sequence"]

    # Reset the sequence, show and score
    kroz_app.state["_sequence"] = 0
    kroz_app.show.reset_mock()
    kroz_app.score = 0

    result2 = FlowContext.run(qq())
    assert result1 == result2
    assert kroz_app.show.call_count == 1  # The question was re-shown
    assert kroz_app.score == 0
