# -*- coding: utf-8 -*-
__all__ = ["dumps", "dump"]
import sys
import os
import json


def dumps(db, *, encode=None, indent=None):
    """Dump the JSON database.

    Parameter `output` may be a `str` or `filelike` object:

    .. code-block:: python

        # Create and write to "foo.json" file
        with open("foo.json", "wb+") as f:
            save_db(f, db=db)

        # Create and write to "foo.json" file
        save_db("foo.json", db=db)

        # Write to sys.stdout
        save_db(sys.stdout, db=db)

    Parameter `output` may be omitted to print to `sys.stdout`:

    .. code-block:: python

        save_db(db=db)

    Parameter `dumps` can be provided to customize how db is printed:

    .. code-block:: python

        save_db(db=db, dumps=json.dumps)

    :param output: output file
    :param db: JSON database
    :param indent: JSON indent level
    :param dumps: dumps JSON database
    """
    indent = indent if indent is not None else 4

    if encode:
        db = {encode(k): v for k, v in db.items()}

    return json.dumps(db, indent=indent, ensure_ascii=False)


def dump(db, output=None, *, encode=None, indent=None):
    """Dump the JSON database.

    Parameter `output` may be a `str` or `filelike` object:

    .. code-block:: python

        # Create and write to "foo.json" file
        with open("foo.json", "wb+") as f:
            save_db(f, db=db)

        # Create and write to "foo.json" file
        save_db("foo.json", db=db)

        # Write to sys.stdout
        save_db(sys.stdout, db=db)

    Parameter `output` may be omitted to print to `sys.stdout`:

    .. code-block:: python

        save_db(db=db)

    Parameter `dumps` can be provided to customize how db is printed:

    .. code-block:: python

        save_db(db=db, dumps=json.dumps)

    :param output: output file
    :param db: JSON database
    :param indent: JSON indent level
    :param dumps: dumps JSON database
    :param verbose: verbosity level
    """
    output = output if output is not None else sys.stdout

    content = dumps(db, encode=encode, indent=indent)

    # Filelike object
    if hasattr(output, "write"):
        output.write(content)
    # For filename
    elif isinstance(output, str):
        parent = os.path.dirname(output)
        if parent:
            os.makedirs(parent, exist_ok=True)

        with open(output, "wb+") as f:
            f.write(content.encode())
    # Unknown output type
    else:
        raise Exception("output expected to be str, filelike or callable")
