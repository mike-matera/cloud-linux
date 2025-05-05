"""
The question view
"""

from functools import partial
import textwrap
from textual import on
from textual.binding import Binding
from textual.screen import Screen, ModalScreen
from textual.widgets import (
    Footer,
    MarkdownViewer,
    Label,
    Input,
)
from textual.worker import Worker, WorkerState
from textual.containers import HorizontalGroup, VerticalGroup

from kroz.question import Question
from kroz.widget.score_header import ScoreHeader


class CongratsScreen(ModalScreen):
    BINDINGS = [
        ("enter", "dismiss", "Continue"),
        ("ctrl+q", "app.cleanup_quit", "Quit"),
    ]

    CSS_PATH = "../app.tcss"

    def __init__(self):
        super().__init__()

    def compose(self):
        yield ScoreHeader()
        yield Footer()
        yield MarkdownViewer(
            textwrap.dedent("""
            # Congratulations            
                You got the correct answer.
            """),
            show_table_of_contents=False,
            classes="content",
        )


class FeedbackScreen(ModalScreen[bool]):
    BINDINGS = [
        ("enter", "try_again", "Continue"),
        ("escape", "skip", "Skip"),
        ("ctrl+q", "app.cleanup_quit", "Quit"),
    ]

    CSS_PATH = "../app.tcss"

    def __init__(self, error: Exception, can_skip):
        super().__init__()
        self._err = error
        self._can_skip = can_skip

    def on_mount(self):
        md = self.query_one("Markdown")
        if isinstance(self._err, AssertionError):
            md.border_title = "Incorrect Answer"
        else:
            md.border_title = f"Error: {self._err.__class__.__name__}"

    def action_skip(self):
        self.dismiss(False)

    def action_try_again(self):
        self.dismiss(True)

    def check_action(self, action: str, parameters: tuple[object, ...]):
        if action == "skip":
            return self._can_skip
        else:
            return True

    def compose(self):
        yield ScoreHeader()
        yield Footer()
        yield MarkdownViewer(
            textwrap.dedent(str(self._err)),
            show_table_of_contents=False,
            classes="content",
        )


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
        Binding("escape", "skip", "Skip", priority=True),
        Binding("ctrl+q", "app.cleanup_quit", "Quit", priority=True),
    ]

    CSS_PATH = "../app.tcss"

    def __init__(
        self, question: Question, points: int, tries: int, can_skip: bool
    ):
        super().__init__()
        self._question = question
        self._points = points
        self._tries_total = tries
        self._tries = 0
        self._can_skip = can_skip
        self._result = None

    def compose(self):
        yield ScoreHeader()
        yield Footer()
        yield MarkdownViewer(
            textwrap.dedent(self._question.text),
            show_table_of_contents=False,
            classes="content",
        )
        with VerticalGroup(classes="answer"):
            with HorizontalGroup():
                yield Label("$", id="prompt")
                yield Input(
                    placeholder=self._question.placeholder,
                    validate_on=["submitted"],
                    validators=self._question.validators,
                )

    def on_mount(self):
        self.refresh_bindings()
        self.query_one("Input").disabled = True
        self._setup()

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

    @on(Input.Submitted)
    async def submit(self, event: Input.Changed) -> None:
        query = self.query("#validation")
        if query:
            feedback = query.first()
        else:
            feedback = Label("", id="validation")
            await self.query_one(".answer").mount(feedback, before=0)

        if not event.validation_result or event.validation_result.is_valid:
            feedback.remove()
            self.query_one("Input").disabled = True
            self._tries += 1
            self._check(event.value)
        else:
            self.query_one("#validation").update(
                "\n".join(
                    (
                        f"❌ {x}"
                        for x in event.validation_result.failure_descriptions
                    )
                )
            )

    def action_skip(self):
        self._result = Question.Result.SKIPPED
        self._cleanup()

    def on_worker_state_changed(self, event: Worker.StateChanged) -> None:
        if event.worker.name == "setup" and event.state == WorkerState.SUCCESS:
            if self._tries_total:
                self.app.notify(f"You have {self._tries_total} tries.")
            input = self.query_one("Input")
            input.disabled = False
            self.set_focus(input)

        elif event.worker.name == "check":
            if event.state == WorkerState.ERROR:
                # Wrong answer...
                def cb(again: bool):
                    if not again:
                        self._result = Question.Result.SKIPPED
                        self._cleanup()
                    if self._tries_total and self._tries == self._tries_total:
                        # Too many tries.
                        self._result = Question.Result.INCORRECT
                        self._cleanup()
                    else:
                        if self._tries_total:
                            self.app.notify(
                                f"You have {self._tries_total - self._tries} trie(s) remaining."
                            )

                        # Try again.
                        input = self.query_one("Input")
                        input.disabled = False
                        self.set_focus(input)

                self.app.push_screen(
                    FeedbackScreen(event.worker.error, self._can_skip),
                    callback=cb,
                )

            elif event.state == WorkerState.SUCCESS:
                # Correct answer...
                self.app.score += self._points
                self._result = Question.Result.CORRECT

                def cb(_: None):
                    self._cleanup()

                self.app.push_screen(CongratsScreen(), callback=cb)

        elif (
            event.worker.name == "cleanup"
            and event.state == WorkerState.SUCCESS
        ):
            self.dismiss(self._result)

    def _setup(self):
        self.run_worker(
            self._question.setup, "setup", exclusive=True, thread=True
        )

    def _check(self, value):
        self.run_worker(
            partial(self._question.check, value),
            "check",
            thread=True,
            exclusive=True,
            exit_on_error=False,
        )

    def _cleanup(self):
        self.run_worker(
            self._question.cleanup,
            "cleanup",
            exclusive=True,
            thread=True,
        )
