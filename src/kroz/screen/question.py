"""
The question view
"""

from functools import partial
import textwrap
from textual import on
from textual.binding import Binding
from textual.screen import Screen
from textual.widgets import (
    Footer,
    MarkdownViewer,
    Label,
    Input,
)
from textual.containers import HorizontalGroup
from textual.worker import Worker, WorkerState


from kroz.widget.score_header import ScoreHeader


class QuestionScreen(Screen[bool]):
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
        Binding("ctrl+q", "app.cleanup_quit", "Quit", priority=True),
    ]

    CSS_PATH = "../app.tcss"

    def __init__(self, question):
        super().__init__()
        self._question = question

    def compose(self):
        yield ScoreHeader()
        yield Footer()
        yield MarkdownViewer(
            textwrap.dedent(self._question.text),
            show_table_of_contents=False,
            classes="content",
        )
        with HorizontalGroup(id="answer_container"):
            yield Label("$", id="answer_label")
            yield Input(
                id="answer",
                placeholder="Answer",
                validate_on=["submitted"],
                validators=self._question.validators,
            )
            yield Label("", id="validation")

    def on_mount(self):
        self.refresh_bindings()
        self.query_one("Input").disabled = True
        self.run_worker(
            self._question.setup, "setup", exclusive=True, thread=True
        )

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

    def check_action(self, action: str, parameters: tuple[object, ...]):
        if self.is_mounted:
            instructions = self.query_one("MarkdownViewer")
            if action in ["key_up", "key_pageup", "key_down", "key_pagedown"]:
                return instructions.scrollbars_enabled[0]
            else:
                return True

    @on(Input.Submitted)
    async def submit(self, event: Input.Changed) -> None:
        if event.validation_result.is_valid:
            self.query_one("#validation").update("")
            self.query_one("Input").disabled = True
            self.run_worker(
                partial(self._question.check, event.value),
                "check",
                thread=True,
                exclusive=True,
                exit_on_error=False,
            )
        else:
            self.query_one("#validation").update(
                "\n".join(
                    (
                        f"❌ {x}"
                        for x in event.validation_result.failure_descriptions
                    )
                )
            )

    def on_worker_state_changed(self, event: Worker.StateChanged) -> None:
        if event.worker.name == "setup" and event.state == WorkerState.SUCCESS:
            input = self.query_one("Input")
            input.disabled = False
            self.set_focus(input)

        elif event.worker.name == "check":
            if event.state == WorkerState.ERROR:
                # TODO: Display feedback.
                input = self.query_one("Input")
                input.disabled = False
                self.set_focus(input)
            elif event.state == WorkerState.SUCCESS:
                # TODO: Display congratulations.
                self.run_worker(
                    self._question.cleanup,
                    "cleanup",
                    exclusive=True,
                    thread=True,
                )

        elif (
            event.worker.name == "cleanup"
            and event.state == WorkerState.SUCCESS
        ):
            self.dismiss(True)
