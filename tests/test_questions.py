"""
Unit tests for the kroz.questions package
"""

from concurrent.futures import Future
from unittest.mock import Mock

import psutil
import pytest

from kroz.app import KrozApp
from kroz.questions.lesson02 import (
    FreeMemory,
    NewYearFuture,
    OsRelease,
    WhatsUname,
)


@pytest.fixture
def kroz_app(mocker, tmp_path):
    fut = Future()
    app = KrozApp("Testing", config_dir=tmp_path, default_path=tmp_path)
    m = Mock(spec=[], return_value=app)
    mocker.patch("kroz.app.KrozApp.running", new=m)

    def worker() -> None:
        return fut.result()

    app.main(worker)
    yield app

    fut.set_result("")


mem_combos = [
    ("total", psutil.virtual_memory().total),
    ("free", psutil.virtual_memory().free),
    ("shared", psutil.virtual_memory().shared),
    ("available", psutil.virtual_memory().available),
    pytest.param(
        "used", psutil.virtual_memory().used, marks=[pytest.mark.xfail]
    ),
    pytest.param("bogus", 0, marks=[pytest.mark.xfail]),
]


@pytest.mark.parametrize("key,expected", mem_combos)
def test_free_mem(kroz_app, key, expected):
    """Test a question screen"""

    fm = FreeMemory(key)
    fm.check(str(expected // 1024))


year_days = [
    (2018, "Monday"),
    (2019, "Tuesday"),
    (2020, "Wednesday"),
    (2026, "Thursday"),
    (2021, "Friday"),
    (2022, "Saturday"),
    (2023, "Sunday"),
    pytest.param(2023, "Tuesday", marks=[pytest.mark.xfail]),
]


@pytest.mark.parametrize("year,day", year_days)
def test_nyf(kroz_app, year: int, day: str):
    nyf = NewYearFuture(year=year)
    nyf.check(f" {day} ")


uname_keys = [
    (WhatsUname.Keys.ALL),
    (WhatsUname.Keys.KERNEL_NAME),
    (WhatsUname.Keys.NODENAME),
    (WhatsUname.Keys.KERNEL_RELEASE),
    (WhatsUname.Keys.KERNEL_VERSION),
    (WhatsUname.Keys.MACHINE),
    (WhatsUname.Keys.PROCESSOR),
    (WhatsUname.Keys.HARDWARE_PLATFORM),
    (WhatsUname.Keys.OPERATING_SYSTEM),
    pytest.param(-1, marks=[pytest.mark.xfail]),
]


@pytest.mark.parametrize("key", uname_keys)
def test_uname(kroz_app, key):
    wun = WhatsUname(key)
    wun.check(f"  {wun._solution}  \n")


os_release_keys = [
    ("PRETTY_NAME"),
    ("NAME"),
    ("VERSION_ID"),
    ("VERSION"),
    ("VERSION_CODENAME"),
    ("ID"),
    ("ID_LIKE"),
    pytest.param("BOGUS", marks=[pytest.mark.xfail]),
]


@pytest.mark.parametrize("key", os_release_keys)
def test_os_release(kroz_app, key):
    osr = OsRelease(key)
    osr.check(f"  {osr._solution}  \n")
