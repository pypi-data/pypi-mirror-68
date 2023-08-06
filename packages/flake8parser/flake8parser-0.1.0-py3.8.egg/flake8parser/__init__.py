from typing import NamedTuple
from typing import Iterable
from typing import Optional
import asyncio
import re
import sys


class Violation(NamedTuple):
    """ Violation output with attributes. """

    path: str
    line: int
    column: int
    letter: str
    number: int
    message: str

    def __str__(self) -> str:
        return (
            f"{self.path}:{self.line}:{self.column}: "
            f"{self.letter}{self.number} {self.message}"
        )


class ParserError(ValueError):
    """ Raised upon all parsing errors. """

    pass


_parse_re = re.compile(
    r"(?P<path>.*):(?P<line>\d+):(?P<column>\d+): "
    r"(?P<class>\S)(?P<number>\d+) (?P<message>.*)"
)


def parse_line(line: str) -> Violation:
    """
    Parses a line of textual output from flake8.

    Args:
        line: Line of text to parse.

    Raies:
        ParserError: Unable to parse line.
    """
    m = _parse_re.match(line)
    if m:
        return Violation(
            path=str(m["path"]),
            line=int(m["line"]),
            column=int(m["column"]),
            letter=str(m["class"]),
            number=int(m["number"]),
            message=str(m["message"]),
        )
    else:
        raise ParserError(f"unable to parse {line} with {_parse_re.pattern}")


async def flake8(*args: str, cwd: Optional[str] = None) -> Iterable[Violation]:
    """
    Runs flake8, asynchronously generating results.

    Args:
        args: Extra command line arguments to supply to flake8.
        cwd: Working directory.

    Returns:
        Asynchronously generates violations.

    Examples:

        Basic usage::

            import asyncio
            from parse import flake8


            async def main():
                async for violation in flake8(cwd="/home/alex/git/voluptuous"):
                    print(violation)


            asyncio.run(main())
    """
    proc = await asyncio.create_subprocess_exec(
        sys.executable, "-m", "flake8", *args, cwd=cwd, stdout=asyncio.subprocess.PIPE,
    )

    while True:
        line = await proc.stdout.readline()
        if line:
            line = line.decode("utf-8")
            yield parse_line(line)
        else:
            break
