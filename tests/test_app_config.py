import pathlib
import tempfile
import uuid

import pytest
from textual.worker import WorkerFailed

from kroz.app import KrozApp, _default_config
from kroz.screen import KrozScreen
from kroz.secrets import EncryptedStateFile


def get_app(**kwargs):
    app = KrozApp("Testing", **kwargs)
    screen = KrozScreen("Test Text", title="Test Title", can_skip=False)

    def worker() -> str:
        app.show(screen, title="Test Hello", classes="")
        return "bye!"

    app.main(worker)
    return app


@pytest.mark.asyncio
async def test_app_default_config():
    """Test the default configuration"""
    app = get_app()
    async with app.run_test() as pilot:
        # Check the default configuration
        for key, value in _default_config.items():
            assert app.config[key] == value

        await pilot.pause()

        # Now check expected defaults after initialization
        assert app.config["default_path"] == pathlib.Path.home()
        assert app.config["random_seed"] is None
        assert app.config["secret"] == str(uuid.getnode())
        assert app.config["config_dir"] == pathlib.Path.home() / ".kroz"
        assert app.config["state_file"] is None


@pytest.mark.asyncio
async def test_app_debug_config():
    """Test the debug configuration"""
    app = get_app(debug=True)
    async with app.run_test() as pilot:
        await pilot.pause()
        assert app.config["default_path"] == pathlib.Path.cwd()
        assert app.config["random_seed"] is None
        assert app.config["secret"] == str(uuid.getnode())
        assert app.config["config_dir"] == pathlib.Path.cwd()
        assert app.config["state_file"] is None


@pytest.mark.asyncio
async def test_app_config_items():
    """Test the configuration overrides"""
    app = get_app(default_path="/tmp")
    async with app.run_test() as pilot:
        await pilot.pause()
        assert isinstance(app.config["default_path"], pathlib.Path)
        assert app.config["default_path"] == pathlib.Path("/tmp")

    app = get_app(random_seed="20")
    async with app.run_test() as pilot:
        await pilot.pause()
        assert isinstance(app.config["random_seed"], int)
        assert app.config["random_seed"] == 20

    app = get_app(secret="foobar")
    async with app.run_test() as pilot:
        await pilot.pause()
        assert isinstance(app.config["secret"], str)
        assert app.config["secret"] == "foobar"

    app = get_app(config_dir="/tmp")
    async with app.run_test() as pilot:
        await pilot.pause()
        assert isinstance(app.config["config_dir"], pathlib.Path)
        assert app.config["config_dir"] == pathlib.Path("/tmp")

    with tempfile.TemporaryDirectory() as d:
        state_file = pathlib.Path(d) / "state.krs"
        app = get_app(config_dir=d, state_file="state")
        async with app.run_test() as pilot:
            await pilot.pause()
            assert isinstance(app.config["state_file"], pathlib.Path)
            assert isinstance(app.state, EncryptedStateFile)
            assert app.state._path == state_file

    with tempfile.TemporaryDirectory() as d:
        # No absolute paths for the state file.
        state_file = pathlib.Path(d) / "state.krs"
        with pytest.raises(WorkerFailed):
            app = get_app(config_dir=d, state_file=state_file)
            async with app.run_test() as pilot:
                await pilot.pause()
