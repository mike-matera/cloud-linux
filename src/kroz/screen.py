"""
KROZ Screen Base
"""

import importlib.resources
import textwrap

from textual.app import ComposeResult
from textual.binding import Binding
from textual.screen import Screen
from textual.widgets import (
    Footer,
    MarkdownViewer,
)

from kroz.widget.score_header import ScoreHeader


class KrozScreen(Screen[str]):
    """A screen for the kroz player."""

    BINDINGS = [
        Binding("up", "key_up", "Scroll Up", priority=True),
        Binding("down", "key_down", "Scroll Down", priority=True),
        Binding(
            "pageup",
            "key_pageup",
            "Page Up",
            priority=True,
            show=False,
        ),
        Binding(
            "pagedown",
            "key_pagedown",
            "Page Down",
            priority=True,
            show=False,
        ),
        Binding("escape", "skip", "Skip", priority=True),
        Binding("enter", "dismiss", "Continue"),
    ]

    CSS_PATH = str(importlib.resources.files("kroz").joinpath("app.tcss"))

    def __init__(
        self,
        text: str,
        *,
        title: str | None = None,
        can_skip: bool = False,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self._text = text
        self._can_skip = can_skip
        self._text_title = title

    def compose(self) -> ComposeResult:
        yield ScoreHeader()
        yield Footer()
        yield MarkdownViewer(
            textwrap.dedent(self._text),
            show_table_of_contents=False,
            classes="content",
        )

    def on_mount(self) -> None:
        md = self.query_one("Markdown")
        md.border_title = self._text_title
        self.refresh_bindings()

    def key_down(self, key):
        instructions = self.query_one("MarkdownViewer")
        if instructions.scrollbars_enabled[0]:
            instructions.action_scroll_down()
            self.refresh_bindings()

    def key_up(self, key):
        instructions = self.query_one("MarkdownViewer")
        if instructions.scrollbars_enabled[0]:
            instructions.action_scroll_up()
            self.refresh_bindings()

    def key_pagedown(self, key):
        instructions = self.query_one("MarkdownViewer")
        if instructions.scrollbars_enabled[0]:
            instructions.action_page_down()
            self.refresh_bindings()

    def key_pageup(self, key):
        instructions = self.query_one("MarkdownViewer")
        if instructions.scrollbars_enabled[0]:
            instructions.action_page_up()
            self.refresh_bindings()

    def action_skip(self):
        self.dismiss(None)

    def check_action(self, action: str, parameters: tuple[object, ...]):
        if action == "skip":
            return self._can_skip
        elif action in [
            "key_up",
            "key_pageup",
            "key_down",
            "key_pagedown",
        ]:
            if self.is_mounted:
                instructions = self.query_one("MarkdownViewer")
                return instructions.scrollbars_enabled[0]
            else:
                return False
        else:
            return True
