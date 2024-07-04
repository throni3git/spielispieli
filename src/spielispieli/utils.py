import sys
import time

improved_sleep = time.sleep
if sys.platform == "win32":
    # on Windows, set timer resolution to a higher value
    # see https://learn.microsoft.com/en-us/windows/win32/api/timeapi/nf-timeapi-timebeginperiod
    # also see https://stackoverflow.com/a/38488544/5345750
    from ctypes import windll
    # increase timer resolution

    def _improved_sleep(seconds: float) -> None:
        """
        Delay execution for a given number of seconds.
        The argument may be a floating point number for subsecond precision.
        Sets the minimum sleep period to 1ms, sleeps and reverts the value to the Windows default.

        Parameters
        ----------
        seconds : float
            seconds to wait
        """
        windll.winmm.timeBeginPeriod(1)
        time.sleep(seconds)
        windll.winmm.timeEndPeriod(1)

    # overwrite improved_sleep symbol with pimped function
    improved_sleep = _improved_sleep
