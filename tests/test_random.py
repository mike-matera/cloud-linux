"""
Unit tests for the kroz.random package
"""

import getpass
import grp
import os
import pathlib
import subprocess
from unittest.mock import Mock

import pytest

from kroz.app import KrozApp
from kroz.random.path import CheckFile, CheckPath
from kroz.random.words import RandomWord
from kroz.screen import KrozScreen


@pytest.fixture
def kroz_screen():
    return KrozScreen("Test Text", title="Test Title", can_skip=False)


@pytest.fixture
def kroz_app(mocker, tmp_path, kroz_screen):
    app = KrozApp("Testing", config_dir=tmp_path, default_path=tmp_path)
    m = Mock(spec=[], return_value=app)
    mocker.patch("kroz.app.KrozApp.running", new=m)

    def worker() -> None:
        app.show(kroz_screen)

    app.main(worker)
    yield app
    # TODO: Cleanup?


@pytest.fixture
def fake_dict():
    return ["foo", "bar", "bak", "baz"]


@pytest.fixture
def fake_dict_file(tmp_path, fake_dict):
    dict_file = tmp_path / "words.txt"
    with open(dict_file, "w") as fh:
        for word in fake_dict:
            fh.write(f"{word}\n")
    return dict_file


def test_random_word(fake_dict, fake_dict_file):
    """Test on a fake dictionary"""
    rnd = RandomWord()
    rnd.setup(dictionary=fake_dict_file)

    got = []
    for _ in range(10000):
        w = rnd.choice()
        assert w in fake_dict
        got.append(w)

    freq = []
    for word in fake_dict:
        freq.append(got.count(word))

    # Check that the frequencies are approximately equal.
    avg = sum(freq) / len(freq)
    for f in freq:
        assert (avg - (avg / 10)) < f < (avg + (avg / 10))


@pytest.fixture(autouse=True)
def directory_contents(tmp_path):
    base = tmp_path / "testbase"
    base.mkdir()
    with open(base / "file.txt", "w") as fh:
        fh.write("A text file\n")
    os.chmod(base / "file.txt", 0o660)
    link = base / "link.txt"
    link.symlink_to("file.txt")
    dir = base / "mydir"
    dir.mkdir()
    with open(dir / "file.txt", "w") as fh:
        fh.write("Another text file\n")
    os.chmod(dir / "file.txt", 0o600)


@pytest.mark.asyncio
async def test_path_analysis(kroz_app, tmp_path):
    """Test the ability to create CheckPaths from filesystem paths."""
    kroz_app._setup_user_app()
    test_base = tmp_path / "testbase"
    p = CheckPath.from_path(test_base)
    assert p.basepath == test_base
    for path in test_base.glob("**/*"):
        f = p.find(path.relative_to(test_base))
        assert f.owner == path.owner()
        assert f.group == path.group()
        assert f.perms == os.stat(path, follow_symlinks=False).st_mode & 0o777
        if path.is_file() and not path.is_symlink():
            f = p.find_file(path.relative_to(test_base))
            with open(path) as fh:
                contents = fh.read()
            assert contents == f.contents
        elif path.is_symlink():
            f = p.find_link(path.relative_to(test_base))
            assert f.target == path.readlink()
        elif path.is_dir() and not path.is_symlink():
            f = p.find_dir(path.relative_to(test_base))
        else:
            assert False, f"Bogus path: {path}"


@pytest.mark.asyncio
async def test_path_creation(kroz_app, tmp_path):
    """Test the ability to create filesystem paths from CheckPaths"""
    kroz_app._setup_user_app()
    test_base = tmp_path / "testbase"
    p = CheckPath.from_path(test_base)
    p_copy = p
    p_copy.basepath = tmp_path / "testbase2"
    p.sync()
    subprocess.run(
        "diff -r testbase testbase2", shell=True, check=True, cwd=tmp_path
    )
    for diff in p_copy.check():
        assert False, f"File mismatch: {diff}"


@pytest.mark.asyncio
async def test_file_contents(kroz_app, tmp_path):
    """CheckFiles should add a newline to the end of the file if there is not one."""
    kroz_app._setup_user_app()
    cp = CheckPath(basepath=tmp_path / "base")
    cp.files = [
        CheckFile("foo", contents="Hello World", perms=0o777),
    ]
    cp.sync()
    with open(tmp_path / "base" / "foo") as fh:
        assert fh.read() == "Hello World\n"

    cp.files = [
        CheckFile("foo", contents="Hello World\n", perms=0o777),
    ]
    cp.sync()
    with open(tmp_path / "base" / "foo") as fh:
        assert fh.read() == "Hello World\n"


@pytest.mark.asyncio
async def test_diffs(kroz_app, tmp_path):
    kroz_app._setup_user_app()
    (tmp_path / "base").mkdir()
    testfile = tmp_path / "base" / "foo"
    cp = CheckPath(basepath=tmp_path / "base")
    cp.files = [
        CheckFile(
            "foo", contents="Hello World", perms=0o777, group=getpass.getuser()
        ),
    ]
    diff = list(cp.check())
    assert len(diff) == 1
    assert isinstance(diff[0], tuple)
    assert diff[0][0] == pathlib.Path("foo")
    assert diff[0][1] == "Missing"

    with open(testfile, "w") as fh:
        fh.write("bogus")
    testfile.chmod(0o777)
    diff = list(cp.check())
    assert len(diff) == 1
    assert isinstance(diff[0], tuple)
    assert diff[0][0] == pathlib.Path("foo")
    assert diff[0][1] == "Wrong contents"

    with open(testfile, "w") as fh:
        fh.write("Hello World")
    testfile.chmod(0o666)
    diff = list(cp.check())
    assert len(diff) == 1
    assert isinstance(diff[0], tuple)
    assert diff[0][0] == pathlib.Path("foo")
    assert diff[0][1] == "Wrong permissions"

    testfile.chmod(0o777)
    os.chown(testfile, os.stat(testfile).st_uid, grp.getgrnam("users").gr_gid)
    diff = list(cp.check())
    assert len(diff) == 1
    assert isinstance(diff[0], tuple)
    assert diff[0][0] == pathlib.Path("foo")
    assert diff[0][1] == "Wrong group"

    testfile.unlink()
    testfile.symlink_to(pathlib.Path.home())
    diff = list(cp.check())
    assert len(diff) == 1
    assert isinstance(diff[0], tuple)
    assert diff[0][0] == pathlib.Path("foo")
    assert diff[0][1] == "Wrong type"

    testfile.unlink()
    testfile.mkdir()
    testfile.chmod(0o777)
    diff = list(cp.check())
    assert len(diff) == 1
    assert isinstance(diff[0], tuple)
    assert diff[0][0] == pathlib.Path("foo")
    assert diff[0][1] == "Wrong type"

    testfile.rmdir()
    with open(testfile.with_suffix(".bad"), "w") as fh:
        fh.write("bogus")
    with open(testfile, "w") as fh:
        fh.write("Hello World")
    testfile.chmod(0o777)
    diff = list(cp.check())
    assert len(diff) == 1
    assert isinstance(diff[0], tuple)
    assert diff[0][0] == pathlib.Path("foo.bad")
    assert diff[0][1] == "Exists"
