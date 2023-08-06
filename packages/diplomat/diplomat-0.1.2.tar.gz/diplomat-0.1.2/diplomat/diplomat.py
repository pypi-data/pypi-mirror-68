import os
import subprocess
import tempfile
import threading


class Attachee:
    """
    is a simple, reader version of the diplomat.
    """

    def __init__(self, out, err):
        """initializes an Attachee by giving it two filenames to read from."""
        self._outfile = open(out)
        self._errfile = open(err)

    def output(self):
        """returns the standard output."""
        # make a new one, so we don’t interfere with writing
        with open(self._outfile.name) as f:
            return f.read()

    def output_stream(self):
        """returns a line-based generator over the standard output."""
        with open(self._outfile.name) as f:
            for line in f:
                yield line

    def output_file(self):
        """returns the standard output file."""
        return self._outfile

    def output_file_name(self):
        """returns the standard output file’s name."""
        return self._outfile.name

    def error(self):
        """returns the standard error output."""
        # make a new one, so we don’t interfere with writing
        with open(self._errfile.name) as f:
            return f.read()

    def error_stream(self):
        """returns a line-based generator over the standard error output."""
        with open(self._errfile.name) as f:
            for line in f:
                yield line

    def error_file(self):
        """returns the standard error file."""
        return self._errfile

    def error_file_name(self):
        """returns the standard error file’s name."""
        return self._errfile.name


class Diplomat(Attachee):
    """
    is a simple wrapper around subprocesses and temporary files.

    You can inquire it about its state and properties, and most
    importantly about its file contents.
    """

    def __init__(
        self,
        *cmd,
        out=None,
        err=None,
        single_file=False,
        env=None,
        on_exit=None,
        pre_start=None,
        post_start=None
    ):
        """initializes a Diplomat by giving it a command to execute."""
        self._outfile = self._open_or_default(out)
        if single_file:
            self._errfile = self._outfile
        else:
            self._errfile = self._open_or_default(err)

        self.env = os.environ.copy()
        if env:
            self.env = {**self.env, **env}

        self.failed = None
        self._process = None
        self.cmd = cmd

        if pre_start:
            pre_start(self)

        try:
            self._process = subprocess.Popen(
                self.cmd,
                stdout=self._outfile,
                stderr=self._errfile,
                stdin=subprocess.PIPE,
                env=self.env,
            )
        except FileNotFoundError as e:
            self.failed = e

        if on_exit:
            self.register_exit_fn(on_exit)

        if post_start:
            post_start(self)

    def _open_or_default(self, f):
        if f:
            return open(f, "a+", buffering=1)
        return self._create_tmp_file()

    def _create_tmp_file(self):
        return tempfile.NamedTemporaryFile(mode="w+", delete=False, buffering=1)

    def register_exit_fn(self, f):
        """registers a function to run when the process terminates."""

        def wrapped():
            self._process.wait()
            f(self)

        t = threading.Thread(target=wrapped, daemon=True)
        t.start()

    def process(self):
        """returns the underlying process."""
        if self.failed:
            raise self.failed
        return self._process

    def poll(self):
        """polls the underlying process and returns the resulting code."""
        if self.failed:
            raise self.failed
        return self._process.poll()

    def terminate(self):
        """terminates the underlying process."""
        if self.failed:
            raise self.failed
        return self._process.terminate()

    def wait(self):
        """waits for the underlying process."""
        if self.failed:
            raise self.failed
        return self._process.wait()

    def write(self, text):
        """
        write to the standard input of the underlying process. Requires a bytes
        object.
        """
        self._process._stdin_write(text)

    def is_running(self):
        """checks whether the underlying process is_running."""
        return (
            self.failed is None and self._process and self._process.returncode == None
        )

    def has_succeeded(self, expected_code=0):
        """checks whether the underlying process has succeeded."""
        return self.failed is None and self._process.returncode == 0

    def has_failed(self, expected_code=0):
        """checks whether the underlying process has failed."""
        return self.failed is not None and not self.has_succeeded(
            expected_code=expected_code
        )

    def to_attachee(self):
        """creates an attachee from a diplomat."""
        return Attachee(self.output_file_name(), self.error_file_name())
