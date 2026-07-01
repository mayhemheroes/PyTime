#!/usr/bin/env python3
"""Atheris fuzz harness for PyTime.

PyTime parses human-supplied date/time strings into datetime objects. This
harness drives the public string-parsing + relative-date API on arbitrary
input; Atheris instruments the imported pytime modules (coverage) so libFuzzer
steers the parser toward new code paths.

Run modes (driven by the compiled launcher `fuzz_time` / `-standalone`):
  * fuzzing      — `python3 fuzz_time.py [libFuzzer args]`
  * single input — `python3 fuzz_time.py <file>` (libFuzzer runs it once)
"""
import os
import sys

# fuzz_helpers.py lives alongside this harness — make it importable when the
# launcher execs us by absolute path.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import atheris
import fuzz_helpers

# Instrument the library under test so the fuzzer gets coverage feedback.
with atheris.instrument_imports():
    from pytime import pytime
    from pytime.exception import PyTimeException


def TestOneInput(data: bytes) -> None:
    fdp = fuzz_helpers.EnhancedFuzzedDataProvider(data)
    which = fdp.ConsumeIntInRange(0, 4)
    text = fdp.ConsumeRemainingString()
    try:
        if which == 0:
            pytime.parse(text)
        elif which == 1:
            pytime.before(text)
        elif which == 2:
            pytime.after(text)
        elif which == 3:
            pytime.tomorrow(text)
        else:
            pytime.count(text, text)
    except (PyTimeException, ValueError, TypeError, IndexError, OverflowError):
        # Library-defined and standard input-validation errors are expected for
        # malformed date strings — not defects.
        pass


def main() -> None:
    atheris.Setup(sys.argv, TestOneInput)
    atheris.Fuzz()


if __name__ == "__main__":
    main()
