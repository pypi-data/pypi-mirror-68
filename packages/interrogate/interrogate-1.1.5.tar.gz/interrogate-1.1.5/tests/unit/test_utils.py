# Copyright 2020 Lynn Root
"""Unit tests for interrogate/utils.py module"""

import re
import sys

import pytest

from interrogate import utils


IS_WINDOWS = sys.platform in ("cygwin", "win32")


@pytest.mark.parametrize(
    "value,exp",
    (
        # no regex given
        (None, None),
        ((), None),
        # single regex
        (["^_.*"], [re.compile("^_.*")]),
        # multiple regexes
        (
            ["^get_.*", "^post_.*"],
            [re.compile("^get_.*"), re.compile("^post_.*")],
        ),
    ),
)
def test_parse_regex(value, exp):
    """Compile a given string into regex."""
    actual = utils.parse_regex({}, "ignore_regex", value)
    assert exp == actual


@pytest.mark.parametrize("filename", (None, "-", "input.txt"))
def test_smart_open(filename, mocker):
    """Handles both opening a file and stdout in the same manner."""
    m_open = mocker.mock_open()
    mock_open = mocker.patch("interrogate.utils.open", m_open)

    with utils.smart_open(filename, fmode="r") as act_ret:
        pass

    if filename and filename != "-":
        mock_open.assert_called_once_with(filename, "r")
        assert act_ret.closed
    else:
        mock_open.assert_not_called()
        assert act_ret == sys.stdout


@pytest.mark.skipif(IS_WINDOWS, reason="unix-only tests")
@pytest.mark.parametrize(
    "files,side_effect,expected",
    (
        (("/usr/src/app", "/usr/src/tests"), (True,), "/usr/src"),
        (
            ("/usr/src/app/sample.py", "/usr/src/app/sample2.py"),
            (False, True),
            "/usr/src/app",
        ),
        (("/usr/src/app/sample.py", "/usr/src/tests"), (True,), "/usr/src"),
        (("/usr/src/app", "/src/tests"), (True,), "/"),
    ),
)
def test_get_common_base(files, side_effect, expected, mocker, monkeypatch):
    """Return common base of a set of files/directories, if any."""
    mock_exists = mocker.Mock(side_effect=side_effect)
    monkeypatch.setattr(utils.pathlib.Path, "exists", mock_exists)
    actual = utils.get_common_base(files)
    assert expected == actual


@pytest.mark.skipif(not IS_WINDOWS, reason="windows-only tests")
@pytest.mark.parametrize(
    "files,side_effect,expected",
    (
        ((r"C:\usr\src\app", r"C:\usr\src\tests"), (True,), r"C:\usr\src"),
        (
            (r"C:\usr\src\app\sample.py", r"C:\usr\src\app\sample2.py"),
            (False, True),
            r"C:\usr\src\app",
        ),
        (
            (r"C:\usr\src\app\sample.py", r"C:\usr\src\tests"),
            (True,),
            r"C:\usr\src",
        ),
        ((r"C:\usr\src\app", r"C:\src\tests"), (True,), "C:\\"),
        (
            (r"C:\path\to\src\file.py", r"C:\path\to\tests\test_file.py"),
            (True,),
            r"C:\path\to",
        ),
    ),
)
def test_get_common_base_windows(
    files, side_effect, expected, mocker, monkeypatch
):
    """Return common base of a set of files/directories, if any."""
    mock_exists = mocker.Mock(side_effect=side_effect)
    monkeypatch.setattr(utils.pathlib.Path, "exists", mock_exists)
    actual = utils.get_common_base(files)
    assert expected == actual


@pytest.mark.skipif(IS_WINDOWS, reason="unix-only tests")
@pytest.mark.parametrize(
    "padded_cells,colwidths,colaligns,width,expected",
    (
        # no data
        ([""], [0], ["left"], 15, "|             |"),
        # left & right align
        (["foo", "bar"], [3, 3], ["left", "right"], 15, "|foo   |   bar|"),
        # left & right align with a non-equal amount of padding per column
        (["foo", "bar"], [3, 3], ["left", "right"], 14, "|foo   |  bar|"),
        # table separator
        (["---", ""], [3, 0], ["left", "right"], 15, "|--------|----|"),
        # default to left alignment
        (["foo", "bar"], [3, 3], ["?", "?"], 15, "|foo   |bar   |"),
    ),
)
def test_interrogate_line_formatter(
    padded_cells, colwidths, colaligns, width, expected, monkeypatch
):
    """Data is padded and aligned correctly to fit the terminal width."""
    monkeypatch.setattr(utils, "TERMINAL_WIDTH", width)

    actual = utils.interrogate_line_formatter(
        padded_cells, colwidths, colaligns
    )

    assert width == len(actual)
    assert expected == actual


@pytest.mark.skipif(not IS_WINDOWS, reason="windows-only tests")
@pytest.mark.parametrize(
    "padded_cells,colwidths,colaligns,width,expected",
    (
        # no data
        ([""], [0], ["left"], 15, "|            |"),
        # left & right align
        (["foo", "bar"], [3, 3], ["left", "right"], 15, "|foo   |  bar|"),
        # left & right align with a non-equal amount of padding per column
        (["foo", "bar"], [3, 3], ["left", "right"], 14, "|foo  |  bar|"),
        # table separator
        (["---", ""], [3, 0], ["left", "right"], 15, "|-------|----|"),
        # default to left alignment
        (["foo", "bar"], [3, 3], ["?", "?"], 15, "|foo   |bar  |"),
    ),
)
def test_interrogate_line_formatter_windows(
    padded_cells, colwidths, colaligns, width, expected, monkeypatch
):
    """Data is padded and aligned correctly to fit the terminal width."""
    monkeypatch.setattr(utils, "TERMINAL_WIDTH", width)

    actual = utils.interrogate_line_formatter(
        padded_cells, colwidths, colaligns
    )

    assert width - 1 == len(actual)
    assert expected == actual
