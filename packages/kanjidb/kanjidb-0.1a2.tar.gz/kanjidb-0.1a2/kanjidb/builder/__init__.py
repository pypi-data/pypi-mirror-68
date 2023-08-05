__all__ = ["build", "main"]
from kanjidb.builder.configuration import Configuration


def build(config):
    """Build a kanji database.

    :param config: builder configuration
    :return: build result
    """
    kwargs = {}

    for step in config.run:
        if config.verbose:
            print("Running {}...".format(step))

        new_kwargs = step(**kwargs)

        if new_kwargs is not None:
            kwargs = new_kwargs

    return kwargs


def main(argv):
    import argparse

    parser = argparse.ArgumentParser(
        prog="KanjiDB builder", description="Kanji database builder"
    )
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbosity level")
    parser.add_argument("config", nargs="?", help="YAML configuration file")
    args = parser.parse_args(argv)

    config = Configuration(verbose=args.verbose)
    config.load(args.config, default=args.config)

    build(config)
