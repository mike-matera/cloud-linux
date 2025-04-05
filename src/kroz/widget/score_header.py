from textual.app import RenderResult
from textual.widgets import (
    Header,
)
from textual.widget import Widget
from textual.widgets._header import HeaderIcon, HeaderTitle
from rich.text import Text


class ScoreHeader(Header):
    class HeaderScore(Widget):
        DEFAULT_CSS = """
        HeaderScore {
            background: $foreground-darken-1 5%;
            color: $foreground;
            text-opacity: 85%;
            content-align: center middle;
            dock: right;
            width: 20;
            padding: 0 1;
        }
        """

        def __init__(self):
            super().__init__()
            self._total = 0
            self._score = 0
            self._format = ""

        def render(self) -> RenderResult:
            return Text(
                self._format.format(score=self._score, total=self._total)
            )

        async def set_total(self, total: int) -> None:
            self._total = total
            self.refresh()

        async def set_score(self, score: int) -> None:
            self._score = score
            self.refresh()

        async def set_format(self, format: str) -> None:
            self._format = format
            self.refresh()

    def __init__(self):
        super().__init__()
        self._total = None
        self._score = None
        self._score_widget = ScoreHeader.HeaderScore()

    def compose(self):
        yield HeaderIcon().data_bind(Header.icon)
        yield HeaderTitle()
        yield self._score_widget

    def on_mount(self):
        self.watch(self.app, "total", self._score_widget.set_total)
        self.watch(self.app, "score", self._score_widget.set_score)
        self.watch(self.app, "score_format", self._score_widget.set_format)
