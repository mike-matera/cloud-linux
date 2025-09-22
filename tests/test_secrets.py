import base64
import tempfile
from pathlib import Path

import pytest

from kroz.secrets import ConfirmationCode, EncryptedStateFile


def test_cfm_encoding():
    c = ConfirmationCode(key="test")
    got = c.confirmation({"foo": "bar"})
    base64.b64decode(got)


def test_cfm_contents():
    c = ConfirmationCode(key="test")
    got = c.validate(
        c.confirmation(
            {
                "foo": "bar",
                "bar": [1, 2, 3, 4],
                "bak": {1: 2, 3: 4},
                "grr": True,
            }
        )
    )
    assert isinstance(got, dict)
    assert "user" in got
    assert "host" in got
    assert "date" in got
    assert "foo" in got
    assert got["foo"] == "bar"
    assert "bar" in got
    assert got["bar"] == [1, 2, 3, 4]
    assert "bak" in got
    # JSON keys are always strings
    assert got["bak"] == {"1": 2, "3": 4}
    assert "grr" in got
    assert got["grr"]


def test_secret_box():
    """Unit tests for the box file."""
    b = EncryptedStateFile(key="test", filename=None)
    b["foo"] = "bar"
    b["bar"] = [1, 2, 3, 4]
    b["bak"] = {1: 2, 3: 4}
    b["grr"] = True
    b["_volatile"] = "me"

    # Store is automatically called

    assert "user" in b
    assert "host" in b
    assert "cmd" in b
    assert "date" in b
    assert "foo" in b
    assert b["foo"] == "bar"
    assert "bar" in b
    assert b["bar"] == [1, 2, 3, 4]
    assert "bak" in b
    assert b["bak"] == {1: 2, 3: 4}
    assert "grr" in b
    assert b["grr"]
    assert "_volatile" in b
    assert b["_volatile"] == "me"


def test_secret_box_load_store():
    """Unit tests for the box file."""
    with tempfile.TemporaryDirectory() as d:
        boxfile = Path(d) / "secret"
        b = EncryptedStateFile(key="test", filename=boxfile)
        b["foo"] = "bar"
        b["bar"] = [1, 2, 3, 4]
        b["bak"] = {1: 2, 3: 4}
        b["grr"] = True
        b["_volatile"] = "me"

        # Store is automatically called
        b = EncryptedStateFile(key="test", filename=boxfile)
        assert "user" in b
        assert "host" in b
        assert "cmd" in b
        assert "date" in b
        assert "foo" in b
        assert b["foo"] == "bar"
        assert "bar" in b
        assert b["bar"] == [1, 2, 3, 4]
        assert "bak" in b
        assert b["bak"] == {1: 2, 3: 4}
        assert "grr" in b
        assert b["grr"]

        # Volatile values should not have been saved.
        assert "_volatile" not in b


def test_wrong_cfm_key():
    c = ConfirmationCode(key="k1")
    d = ConfirmationCode(key="k2")
    with pytest.raises(AssertionError):
        d.validate(c.confirmation({}))


def test_wrong_box_key():
    with tempfile.TemporaryDirectory() as d:
        boxfile = Path(d) / "secret"
        c = EncryptedStateFile(key="k1", filename=boxfile)
        c.store()
        d = EncryptedStateFile(key="k1", filename=boxfile)
        assert "user" in d

        # Bad key gives an empty dictionary
        d = EncryptedStateFile(key="k2", filename=boxfile)
        assert "user" not in d
