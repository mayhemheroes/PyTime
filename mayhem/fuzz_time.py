#!/usr/bin/env python3
import atheris
import sys
import fuzz_helpers
import random

with atheris.instrument_imports():
    from pytime import pytime

from pytime.exception import PyTimeException

def TestOneInput(data):
    fdp = fuzz_helpers.EnhancedFuzzedDataProvider(data)
    test = fdp.ConsumeIntInRange(0, 2)
    try:
        if test == 0:
            pytime.before(fdp.ConsumeRemainingString())
        elif test == 1:
            pytime.tomorrow(fdp.ConsumeRemainingString())
        elif test == 2:
            pytime.parse(fdp.ConsumeRemainingString())
    except (PyTimeException, ValueError):
        return -1
    except (TypeError, IndexError):
        if random.random() > 0.9:
            raise
        return -1
def main():
    atheris.Setup(sys.argv, TestOneInput)
    atheris.Fuzz()


if __name__ == "__main__":
    main()
