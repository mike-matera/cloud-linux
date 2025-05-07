"""
A KROZ screen
"""

import textwrap
from textual.screen import Screen
from textual.widgets import (
    Footer,
    MarkdownViewer,
)

from kroz.widget.score_header import ScoreHeader


from textual.binding import Binding

from typing import Iterable
from textual.validation import Validator


from textual import on
from textual.widgets import (
    Label,
    Input,
)
from textual.containers import HorizontalGroup, VerticalGroup


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

    CSS_PATH = "app.tcss"

    def __init__(
        self,
        text: str,
        *,
        title: str = None,
        can_skip: bool = False,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self._text = text
        self._can_skip = can_skip
        self._text_title = title

    def compose(self):
        yield ScoreHeader()
        yield Footer()
        yield MarkdownViewer(
            textwrap.dedent(self._text),
            show_table_of_contents=False,
            classes="content",
        )

    def on_mount(self):
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


class QuestionScreen(KrozScreen):
    CSS_PATH = "app.tcss"

    def __init__(
        self,
        text: str,
        placeholder: str,
        validators: Iterable[Validator],
        **kwargs,
    ):
        super().__init__(text, **kwargs)
        self._placeholder = placeholder
        self._validators = validators
        self._result = None

    def compose(self):
        yield from super().compose()
        with VerticalGroup(classes="answer"):
            with HorizontalGroup():
                yield Label("$", id="prompt")
                yield Input(
                    placeholder=self._placeholder,
                    validate_on=["submitted"],
                    validators=self._validators,
                )

    def on_mount(self):
        super().on_mount()
        self.query_one("Input").focus()

    @on(Input.Submitted)
    async def submit(self, event: Input.Changed) -> None:
        input = self.query_one("Input")
        query = self.query("#validation")
        if query:
            feedback = query.first()
        else:
            feedback = Label("", id="validation")
            await self.query_one(".answer").mount(feedback, before=0)

        if not event.validation_result or event.validation_result.is_valid:
            self.dismiss(event.value)
        else:
            self.query_one("#validation").update(
                "\n".join(
                    (
                        f"❌ {x}"
                        for x in event.validation_result.failure_descriptions
                    )
                )
            )
        input.clear()
