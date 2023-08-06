"""
Convenience context managers
"""

import os
import sys

import runez.convert
import runez.system
from runez.base import PY2, stringified


if PY2:
    import StringIO
    StringIO = StringIO.StringIO

else:
    from io import StringIO


class CapturedStream(object):
    """Capture output to a stream by hijacking temporarily its write() function"""

    def __init__(self, name, target):
        self.name = name
        self.target = target
        self.buffer = StringIO()
        self.capture_write = "_pytest" in stringified(self.target.__class__)
        if self.capture_write and self.target.write.__name__ == self.captured_write.__name__:
            self.capture_write = False

    def __repr__(self):
        return self.contents()

    def __contains__(self, item):
        return item is not None and item in self.contents()

    def __len__(self):
        return len(self.contents())

    def captured_write(self, message):
        self.buffer.write(message)

    def contents(self):
        """
        Returns:
            (str): Contents of `self.buffer`
        """
        return self.buffer.getvalue()

    def _start_capture(self):
        if self.capture_write:
            # setting sys.stdout doesn't survive with cross module fixtures, so we hijack its write the 1st time we see it
            self.original = self.target.write
            self.target.write = self.captured_write

        else:
            self.original = getattr(sys, self.name)
            setattr(sys, self.name, self.buffer)

    def _stop_capture(self):
        if self.capture_write:
            self.target.write = self.original

        else:
            setattr(sys, self.name, self.original)

    def pop(self, strip=False):
        """Current content popped, useful for testing"""
        r = self.contents()
        self.clear()
        if r and strip:
            r = r.strip()
        return r

    def clear(self):
        """Clear captured content"""
        self.buffer.seek(0)
        self.buffer.truncate(0)


class TrackedOutput(object):
    """Track captured output"""

    def __init__(self, stdout, stderr):
        """
        Args:
            stdout (CapturedStream | None): Captured stdout
            stderr (CapturedStream | None): Captured stderr
        """
        self.stdout = stdout
        self.stderr = stderr
        self.captured = [c for c in (self.stdout, self.stderr) if c is not None]

    def __repr__(self):
        return "\n".join("%s: %s" % (s.name, s) for s in self.captured)

    def __contains__(self, item):
        return any(item in s for s in self.captured)

    def __len__(self):
        return sum(len(s) for s in self.captured)

    def contents(self):
        return "".join(s.contents() for s in self.captured)

    def pop(self):
        """Current content popped, useful for testing"""
        r = self.contents()
        self.clear()
        return r

    def clear(self):
        """Clear captured content"""
        assert True
        for s in self.captured:
            s.clear()


class CaptureOutput(object):
    """Output is captured and made available only for the duration of the context.

    Sample usage:

    >>> with CaptureOutput() as logged:
    >>>     print("foo bar")
    >>>     # output has been captured in `logged`, see `logged.stdout` etc
    >>>     assert "foo" in logged
    >>>     assert "bar" in logged.stdout
    """

    _capture_stack = []  # Shared across all objects, tracks possibly nested CaptureOutput buffers

    def __init__(self, stdout=True, stderr=True, anchors=None, dryrun=None):
        """Context manager allowing to temporarily grab stdout/stderr/log output.

        Args:
            stdout (bool): Capture stdout?
            stderr (bool): Capture stderr?
            anchors (str | list | None): Optional paths to use as anchors for `runez.short()`
            dryrun (bool | None): Override dryrun (when explicitly specified, ie not None)
        """
        self.stdout = stdout
        self.stderr = stderr
        self.anchors = anchors
        self.dryrun = dryrun

    @classmethod
    def current_capture_buffer(cls):
        if cls._capture_stack:
            return cls._capture_stack[-1].buffer

    def __enter__(self):
        """
        Returns:
            (TrackedOutput): Object holding captured stdout/stderr/log output
        """
        self.tracked = TrackedOutput(
            CapturedStream("stdout", sys.stdout) if self.stdout else None,
            CapturedStream("stderr", sys.stderr) if self.stderr else None,
        )

        for c in self.tracked.captured:
            c._start_capture()

        if self.tracked.captured:
            self._capture_stack.append(self.tracked.captured[-1])

        if self.anchors:
            runez.convert.Anchored.add(self.anchors)

        if self.dryrun is not None:
            self.dryrun = runez.system.set_dryrun(self.dryrun)

        return self.tracked

    def __exit__(self, *args):
        if self.tracked.captured:
            self._capture_stack.pop()

        for c in self.tracked.captured:
            c._stop_capture()

        if self.anchors:
            runez.convert.Anchored.pop(self.anchors)

        if self.dryrun is not None:
            runez.system.set_dryrun(self.dryrun)


class CurrentFolder(object):
    """Context manager for changing the current working directory"""

    def __init__(self, destination, anchor=False):
        self.anchor = anchor
        self.destination = runez.convert.resolved_path(destination)

    def __enter__(self):
        self.current_folder = os.getcwd()
        os.chdir(self.destination)
        if self.anchor:
            runez.convert.Anchored.add(self.destination)

    def __exit__(self, *_):
        os.chdir(self.current_folder)
        if self.anchor:
            runez.convert.Anchored.pop(self.destination)


class TempArgv(object):
    """Context manager for changing the current sys.argv"""

    def __init__(self, args, exe=sys.executable):
        self.args = args
        self.exe = exe
        self.old_argv = sys.argv

    def __enter__(self):
        sys.argv = [self.exe] + self.args

    def __exit__(self, *_):
        sys.argv = self.old_argv


def verify_abort(func, *args, **kwargs):
    """
    Convenient wrapper around functions that should exit or raise an exception

    Example:

        >>> assert "Can't create folder" in verify_abort(runez.ensure_folder, "/dev/null/not-there")

    Args:
        func (callable): Function to execute
        *args: Args to pass to 'func'
        **kwargs: Named args to pass to 'func'

    Returns:
        (str): Chatter from call to 'func', if it did indeed raise
    """
    expected_exception = kwargs.pop("expected_exception", runez.system.AbortException)
    with CaptureOutput() as logged:
        try:
            value = func(*args, **kwargs)
            assert False, "%s did not raise, but returned %s" % (func, value)

        except expected_exception:
            return stringified(logged)
