__all__ = ["help", "main"]
import sys


def help():
    return """
Usage:  kanjidb COMMAND [OPTIONS]

A kanji database accessible via REST API

Options:
  -v, --version            Print version information and quit
  -h, --help               Show this help

Commands:
  build       Build kanji database from sources
  run         Run local server and REST API

Run 'kanjidb COMMAND --help' for more information on a command.

"""


def main(argv=None):
    if argv is None:
        argv = sys.argv

    if isinstance(argv, str):
        import shlex

        argv = shlex.split(argv)
    elif not hasattr(argv, "__iter__"):
        raise Exception("expected a list or string")

    if len(argv) >= 2:
        # python -m kanjidb build [ARGS...]
        if argv[1] == "build":
            from kanjidb import builder

            return builder.main(argv[2:])
        # python -m kanjidb run [ARGS...]
        elif argv[1] == "run":
            from kanjidb import service

            return service.main(argv[2:])

    print(help())


if __name__ == "__main__":
    main()
