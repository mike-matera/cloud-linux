"""
Testing Flows
"""

from unittest.mock import MagicMock, Mock

import pytest

from kroz.app import KrozApp
from kroz.flow.base import FlowContext, FlowResult
from kroz.flow.question import Question


@pytest.fixture
def kroz_app(mocker, tmp_path):
    app = KrozApp("Testing", config_dir=tmp_path, default_path=tmp_path)

    # Mock interfaces so we don't have to run the app.
    mocker.patch("kroz.app.KrozApp.running", new=Mock(return_value=app))
    mocker.patch("kroz.app.KrozApp.show", new=Mock(return_value="show-return"))

    p = MagicMock()
    mocker.patch("kroz.app.KrozApp.progress", new=p)

    app._setup_user_app()

    yield app


@pytest.fixture
def correct_q():
    class _correct(Question):
        points = 10
        progress = True

        def check(self, answer: str) -> None:
            return

    return _correct


@pytest.fixture
def incorrect_q():
    class _incorrect(Question):
        points = 10
        progress = True
        tries = 1

        def check(self, answer: str) -> None:
            raise ValueError("")

    return _incorrect


def test_flow_correct(kroz_app, correct_q):
    """Test a flow with correct result"""

    result = FlowContext.run(correct_q(progress=False))
    assert isinstance(result, correct_q)
    assert result.result == FlowResult.CORRECT
    assert result.answer == "show-return"
    assert kroz_app.show.call_count == 2
    assert kroz_app.score == 10
    assert "Success" == kroz_app.show.call_args_list[1].args[0]._text_title
    assert "checkpoints" in kroz_app.state
    assert 0 == len(kroz_app.state["checkpoints"])


def test_flow_failure(kroz_app, incorrect_q):
    """Test a flow with failure result"""

    result = FlowContext.run(incorrect_q(progress=False))
    assert isinstance(result, incorrect_q)
    assert result.result == FlowResult.INCORRECT
    assert result.answer == "show-return"
    assert kroz_app.show.call_count == 2
    assert kroz_app.score == 0
    assert "Error" in kroz_app.show.call_args_list[1].args[0]._text_title
    assert "checkpoints" in kroz_app.state
    assert 0 == len(kroz_app.state["checkpoints"])


def test_flow_skip(mocker, kroz_app, incorrect_q):
    """Test a flow with skipped result"""

    mocker.patch("kroz.app.KrozApp.show", new=Mock(return_value=None))
    result = FlowContext.run(incorrect_q(progress=False))
    assert isinstance(result, incorrect_q)
    assert result.result == FlowResult.SKIPPED
    assert result.answer is None
    assert kroz_app.show.call_count == 1
    assert kroz_app.score == 0
    assert "checkpoints" in kroz_app.state
    assert 0 == len(kroz_app.state["checkpoints"])


def test_flow_checkpoint_success(kroz_app, correct_q):
    q = correct_q()
    result1 = FlowContext.run(q)
    assert kroz_app.show.call_count == 2
    assert kroz_app.score == 10

    # Reset the show, mock and score
    del kroz_app.state["_flow"]
    kroz_app.show.reset_mock()
    kroz_app.score = 0

    q2 = correct_q()
    result2 = FlowContext.run(q2)
    # assert result1 == result2
    assert kroz_app.show.call_count == 0
    assert kroz_app.score == 10


def test_checkpoint_failure(kroz_app, incorrect_q):
    """Test a flow with failure result"""

    q1 = incorrect_q()
    result1 = FlowContext.run(q1)
    assert kroz_app.show.call_count == 2
    assert kroz_app.score == 0

    # Reset the flow, mock and score
    del kroz_app.state["_flow"]
    kroz_app.show.reset_mock()
    kroz_app.score = 0

    q2 = incorrect_q()
    result2 = FlowContext.run(q2)
    # assert result1 == result2
    assert kroz_app.show.call_count == 2  # The question was re-shown
    assert kroz_app.score == 0


def test_checkpoint_skip(mocker, kroz_app, incorrect_q):
    """Test a flow with skipped result"""

    mocker.patch("kroz.app.KrozApp.show", new=Mock(return_value=None))

    q = incorrect_q()
    result1 = FlowContext.run(q)
    assert kroz_app.show.call_count == 1
    assert kroz_app.score == 0

    # Reset the flow, mock and score
    del kroz_app.state["_flow"]
    kroz_app.show.reset_mock()
    kroz_app.score = 0

    q2 = incorrect_q()
    result2 = FlowContext.run(q2)
    # assert result1 == result2
    assert kroz_app.show.call_count == 1  # The question was re-shown
    assert kroz_app.score == 0


def test_flow_checkpoint_data(kroz_app, correct_q):
    with FlowContext(flowname="test") as flow:
        flow.run(correct_q())
        flow.run(correct_q())
        flow.run(correct_q())
        flow.run(correct_q())
        flow.run(correct_q())

    assert 5 == len(kroz_app.state["checkpoints"])
    for i in range(5):
        assert f"root-test-{i}" in kroz_app.state["checkpoints"]


def test_flow_checkpoint_data_nested(kroz_app, correct_q):
    with FlowContext(flowname="test1") as flow:
        flow.run(correct_q())
        assert "root-test1-0" in kroz_app.state["checkpoints"]
        flow.run(correct_q())
        assert "root-test1-1" in kroz_app.state["checkpoints"]
        with FlowContext(flowname="test2") as flow:
            flow.run(correct_q())
            assert "root-test1-test2-0" in kroz_app.state["checkpoints"]
            flow.run(correct_q())
            assert "root-test1-test2-1" in kroz_app.state["checkpoints"]
        flow.run(correct_q())
        assert "root-test1-2" in kroz_app.state["checkpoints"]

    assert 5 == len(kroz_app.state["checkpoints"])


def test_flow_complete(kroz_app):
    assert not FlowContext.is_complete("foo")
    with FlowContext("foo"):
        assert not FlowContext.is_complete("foo")
    assert FlowContext.is_complete("foo")


def test_flow_complete_nested(kroz_app):
    assert not FlowContext.is_complete("foo")
    with FlowContext("foo"):
        assert not FlowContext.is_complete("foo")
        assert not FlowContext.is_complete("bar")
        with FlowContext("bar"):
            assert not FlowContext.is_complete("bar")
        assert FlowContext.is_complete("bar")

    assert FlowContext.is_complete("foo-bar")
    assert FlowContext.is_complete("foo")


def test_flow_status_success(kroz_app, correct_q, incorrect_q):
    with FlowContext("test") as flow:
        flow.run(correct_q())
    assert FlowContext.flow_status("test") == FlowResult.CORRECT


def test_flow_status_failure(kroz_app, correct_q, incorrect_q):
    with FlowContext("test") as flow:
        flow.run(incorrect_q())

    assert FlowContext.flow_status("test") == FlowResult.INCORRECT


def test_flow_status_mixed(kroz_app, correct_q, incorrect_q):
    with FlowContext("test") as flow:
        flow.run(correct_q())
        flow.run(incorrect_q())

    assert FlowContext.flow_status("test") == FlowResult.INCORRECT


def test_flow_status_none(kroz_app, correct_q, incorrect_q):
    assert FlowContext.flow_status("test") == FlowResult.INCOMPLETE


def test_flow_status_error(kroz_app, correct_q, incorrect_q):
    with pytest.raises(ValueError):
        with FlowContext("test") as flow:
            flow.run(correct_q())
            flow.run(incorrect_q())
            raise ValueError()

    assert FlowContext.flow_status("test") == FlowResult.SKIPPED
