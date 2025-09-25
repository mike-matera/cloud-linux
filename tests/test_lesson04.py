from pathlib import Path

import pytest

from kroz.questions.lesson04 import LinkInfo


@pytest.fixture
def temp_symlinks(tmp_path):
    # Create a real file and a symlink to it
    target = tmp_path / "target.txt"
    target.write_text("hello")
    abs_link = tmp_path / "abs_link"
    abs_link.symlink_to(target)
    rel_link = tmp_path / "rel_link"
    rel_link.symlink_to(Path(".") / target.name)
    indirect_link = tmp_path / "indirect_link"
    indirect_link.symlink_to(rel_link.name)
    indirect_abs_link = tmp_path / "indirect_abs_link"
    indirect_abs_link.symlink_to(abs_link)
    return abs_link, rel_link, indirect_link, indirect_abs_link, target


def do_question(question, answer):
    question.setup()
    question.setup_attempt()
    assert question.text is not None
    question.check(answer)
    question.cleanup_attempt()
    question.cleanup()


def test_linkinfo_target(temp_symlinks):
    abs_link, rel_link, indirect_link, indirect_abs_link, target = (
        temp_symlinks
    )
    q = LinkInfo(type=LinkInfo.Info.TARGET, path=abs_link)
    do_question(q, str(target))

    q = LinkInfo(type=LinkInfo.Info.TARGET, path=rel_link)
    do_question(q, str(target.name))


def test_linkinfo_target_path(temp_symlinks):
    abs_link, rel_link, indirect_link, indirect_abs_link, target = (
        temp_symlinks
    )
    q = LinkInfo(type=LinkInfo.Info.TARGET_PATH, path=rel_link)
    do_question(q, str(target.resolve()))

    # Test validator
    q = LinkInfo(type=LinkInfo.Info.TARGET_PATH, path=rel_link)
    assert not q.validators.validate("relpath").is_valid
    assert q.validators.validate("/abspath").is_valid

    # Test that an absolute link is not accepted
    with pytest.raises(AssertionError):
        q = LinkInfo(type=LinkInfo.Info.TARGET_PATH, path=abs_link)
        q.setup()

    # Test that an indirect link is not accepted
    with pytest.raises(AssertionError):
        q = LinkInfo(type=LinkInfo.Info.TARGET_PATH, path=indirect_link)
        do_question(q, None)

    # Test that an indirect link is not accepted
    with pytest.raises(AssertionError):
        q = LinkInfo(type=LinkInfo.Info.TARGET_PATH, path=indirect_abs_link)
        do_question(q, None)


def test_linkinfo_target_path_indirect(temp_symlinks):
    abs_link, rel_link, indirect_link, indirect_abs_link, target = (
        temp_symlinks
    )

    q = LinkInfo(type=LinkInfo.Info.TARGET_PATH_INDIRECT, path=indirect_link)
    do_question(q, str(target.resolve()))

    q = LinkInfo(
        type=LinkInfo.Info.TARGET_PATH_INDIRECT, path=indirect_abs_link
    )
    do_question(q, str(target.resolve()))

    # Test validator
    q = LinkInfo(type=LinkInfo.Info.TARGET_PATH_INDIRECT, path=indirect_link)
    assert not q.validators.validate("relpath").is_valid
    assert q.validators.validate("/abspath").is_valid

    # Test that an absolute link is not accepted
    with pytest.raises(AssertionError):
        q = LinkInfo(type=LinkInfo.Info.TARGET_PATH_INDIRECT, path=abs_link)
        do_question(q, None)

    # Test that an direct link is not accepted
    with pytest.raises(AssertionError):
        q = LinkInfo(type=LinkInfo.Info.TARGET_PATH_INDIRECT, path=rel_link)
        do_question(q, None)
