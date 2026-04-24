# Copyright © 2009/2023 Andrey Vlasovskikh
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this
# software and associated documentation files (the "Software"), to deal in the Software
# without restriction, including without limitation the rights to use, copy, modify,
# merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be included in all copies
# or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
# PARTICULAR PURPOSE AND NON-INFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
# CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE
# OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

__all__ = ["make_tokenizer", "TokenSpec", "Token", "LexerError"]

import re
from typing import Callable, Iterable, List, Tuple, Optional, Sequence, Pattern, Union


_Place = Tuple[int, int]
_Spec = Tuple[str, Tuple]


class LexerError(Exception):
    def __init__(self, place: _Place, msg: str) -> None:
        raise NotImplementedError

    def __str__(self) -> str:
        raise NotImplementedError


class TokenSpec:
    """A token specification for generating a lexer via `make_tokenizer()`."""

    def __init__(self, type: str, pattern: str, flags: int = 0) -> None:
        """Initialize a `TokenSpec` object.

        Parameters:
            type (str): User-defined type of the token (e.g. `"name"`, `"number"`,
                `"operator"`)
            pattern (str): Regexp for matching this token type
            flags (int, optional): Regexp flags, the second argument of `re.compile()`
        """
        raise NotImplementedError

    def __repr__(self) -> str:
        raise NotImplementedError


class Token:
    """A token object that represents a substring of certain type in your text.

    You can compare tokens for equality using the `==` operator. Tokens also define
    custom `repr()` and `str()`.

    Attributes:
        type (str): User-defined type of the token (e.g. `"name"`, `"number"`,
            `"operator"`)
        value (str): Text value of the token
        start (Optional[Tuple[int, int]]): Start position (_line_, _column_)
        end (Optional[Tuple[int, int]]): End position (_line_, _column_)
    """

    def __init__(
        self,
        type: str,
        value: str,
        start: Optional[_Place] = None,
        end: Optional[_Place] = None,
    ) -> None:
        """Initialize a `Token` object."""
        raise NotImplementedError

    def __repr__(self) -> str:
        raise NotImplementedError

    def __eq__(self, other: object) -> bool:
        # FIXME: Case sensitivity is assumed here
        raise NotImplementedError

    def _pos_str(self) -> str:
        raise NotImplementedError

    def __str__(self) -> str:
        raise NotImplementedError

    @property
    def name(self) -> str:
        pass

    def pformat(self) -> str:
        raise NotImplementedError


def make_tokenizer(
    specs: Sequence[Union[TokenSpec, _Spec]],
) -> Callable[[str], Iterable[Token]]:
    # noinspection GrazieInspection
    """Make a function that tokenizes text based on the regexp specs.

    Type: `(Sequence[TokenSpec | Tuple]) -> Callable[[str], Iterable[Token]]`

    A token spec is `TokenSpec` instance.

    !!! Note

        For legacy reasons, a token spec may also be a tuple of (_type_, _args_), where
        _type_ sets the value of `Token.type` for the token, and _args_ are the
        positional arguments for `re.compile()`: either just (_pattern_,) or
        (_pattern_, _flags_).

    It returns a tokenizer function that takes a string and returns an iterable of
    `Token` objects, or raises `LexerError` if it cannot tokenize the string according
    to its token specs.

    Examples:

    ```pycon
    >>> tokenize = make_tokenizer([
    ...     TokenSpec("space", r"\\s+"),
    ...     TokenSpec("id", r"\\w+"),
    ...     TokenSpec("op", r"[,!]"),
    ... ])
    >>> text = "Hello, World!"
    >>> [t for t in tokenize(text) if t.type != "space"]  # noqa
    [Token('id', 'Hello'), Token('op', ','), Token('id', 'World'), Token('op', '!')]
    >>> text = "Bye?"
    >>> list(tokenize(text))
    Traceback (most recent call last):
        ...
    lexer.LexerError: cannot tokenize data: 1,4: "Bye?"

    ```
    """
    def match_specs(s, i, position):
        raise NotImplementedError

    def f(s):
        raise NotImplementedError

    raise NotImplementedError
