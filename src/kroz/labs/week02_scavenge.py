"""
Scavenger hunt.
"""

from kroz import KrozApp
from kroz.flow import FlowContext
from kroz.questions.lesson02 import (
    FreeMemory,
    OsRelease,
    WhatsUname,
)

app = KrozApp("Scavenger Hunt", state_file="scavenge")


@app.main
def main() -> None:
    with FlowContext("challenges", points=5, progress=True) as flow:
        flow.run(OsRelease(key="NAME"))
        flow.run(WhatsUname(key=WhatsUname.Keys.KERNEL_VERSION))
        flow.run(FreeMemory(key="total"))


if __name__ == "__main__":
    app.run()
