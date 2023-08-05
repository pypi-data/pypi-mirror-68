# -*- coding: utf-8 -*-
__all__ = [
    "UNICODE_ESCAPE",
    "UNICODE_PLUS",
    "UTF8",
    "encode",
    "decode",
    "encode_all",
    "decode_all",
    "get_codepoint",
]
import re

UNICODE_ESCAPE = "unicode_escape"
UNICODE_PLUS = "unicode_plus"
UTF8 = "utf8"


def get_codepoint(kanji):
    return kanji.encode("unicode_escape")[2:].decode().lower()


def decode(s, *, encoding=None):
    """Decode a kanji.

    The kanji may be unicode encoded:

    ..code-block:: python

        >> decode("U+4E00", encoding=UNICODE_PLUS)
        "一"

        >> decode("U4E00", encoding=UNICODE_PLUS)
        "一"

        >> decode("\\u4E00", encoding=UNICODE_ESCAPE)
        "一"

    Or UTF-8 encoded:

    ..code-block:: python

        >> decode("一", encoding=UTF8)
        "一"

        >> decode("一")
        "一"

    :param s: kanji to decode
    :param encoding: how kanji is encoded
    :return: decoded kanji
    """
    if encoding == UNICODE_ESCAPE or encoding == UNICODE_PLUS:
        m = re.match("^(?:\\\\[uU]|[uU][+]?)([0-9a-fA-F]+)$", s)
        if not m:
            raise Exception('Invalid unicode string "{}"'.format(s))

        return chr(int(m.group(1).upper(), 16))
    else:
        return s


def encode(s, *, encoding=None, prefix=None):
    """Encode a kanji.

    The kanji may be unicode encoded:

    ..code-block:: python

        >> encode("一", encoding=UNICODE_PLUS)
        "U+4e00"

        >> encode("一", encoding=UNICODE_PLUS, prefix="U")
        "U4e00"

        >> encode("一", encoding=UNICODE_ESCAPE)
        "\u4e00"

    Or UTF-8 encoded:

    ..code-block:: python

        >> encode("一", encoding=UTF8)
        "一"

        >> encode("一")
        "一"

    :param s: kanji to encode
    :return: encoded kanji
    """
    if encoding == UNICODE_PLUS or encoding == UNICODE_ESCAPE:
        prefix = (
            prefix
            if prefix is not None
            else ("U+" if encoding == UNICODE_PLUS else "\\u")
        )

        return "{}{}".format(prefix, get_codepoint(s))

    return s


def decode_all(kanjis, *, encoding=None):
    """Decode a list of kanjis.

    :param kanjis: list of kanjis
    :param encoding: encoding
    :return: list of decoded kanjis
    """
    encoding = encoding if encoding is not None else UTF8

    return [decode(_, encoding=encoding) for _ in kanjis]


def encode_all(kanjis, *, encoding=None):
    """Reencode a list of UTF-8 encoded kanjis with a new encoding.

    :param kanjis: list of kanjis
    :param encoding: new encoding
    :return: list of encoded kanjis
    """
    encoding = encoding if encoding is not None else UTF8

    return [encode(_, encoding=encoding) for _ in kanjis]
