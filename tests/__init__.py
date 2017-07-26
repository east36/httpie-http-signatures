from httpie.core import main
from httpie.context import Environment


class TestEnvironment(Environment):
    """Environment subclass with reasonable defaults for testing."""

    colors = 0
    stdin_isatty = True,
    stdout_isatty = True
    is_windows = False


class BaseCLIResponse(object):
    """
    Represents the result of simulated `$ http' invocation  via `http()`.

    Holds and provides access to:
        - stdout output: print(self)
        - stderr output: print(self.stderr)
        - exit_status output: print(self.exit_status)
    """

    stderr = None
    json = None
    exit_status = None


def http(*args, **kwargs):
    error_exit_ok = kwargs.pop('error_exit_ok', False)
    env = TestEnvironment()

    stdout = env.stdout
    stderr = env.stderr

    args = list(args)
    args_with_config_defaults = args + env.config.default_options
    add_to_args = []
    if '--debug' not in args_with_config_defaults:
        if not error_exit_ok and '--traceback' not in args_with_config_defaults:
            add_to_args.append('--traceback')
        if not any('--timeout' in arg for arg in args_with_config_defaults):
            add_to_args.append('--timeout=3')
    args = add_to_args + args

    def dump_stderr():
        stderr.seek(0)
        sys.stderr.write(stderr.read())

    try:
        try:
            exit_status = main(args=args, **kwargs)
            if '--download' in args:
                # Let the progress reporter thread finish.
                time.sleep(.5)
        except SystemExit:
            if error_exit_ok:
                exit_status = ExitStatus.ERROR
            else:
                dump_stderr()
                raise
        except Exception:
            stderr.seek(0)
            sys.stderr.write(stderr.read())
            raise
        else:
            if not error_exit_ok and exit_status != ExitStatus.OK:
                dump_stderr()
                raise ExitStatusError(
                    'httpie.core.main() unexpectedly returned'
                    ' a non-zero exit status: {0} ({1})'.format(
                        exit_status,
                        EXIT_STATUS_LABELS[exit_status]
                    )
                )

        stdout.seek(0)
        stderr.seek(0)
        output = stdout.read()
        try:
            output = output.decode('utf8')
        except UnicodeDecodeError:
            # noinspection PyArgumentList
            r = BytesCLIResponse(output)
        else:
            # noinspection PyArgumentList
            r = StrCLIResponse(output)
        r.stderr = stderr.read()
        r.exit_status = exit_status

        if r.exit_status != ExitStatus.OK:
            sys.stderr.write(r.stderr)

        return r

    finally:
        stdout.close()
        stderr.close()
