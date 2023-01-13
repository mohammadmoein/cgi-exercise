from pathlib import Path

import click


class PathPath(click.Path):
    """A Click path argument that returns a pathlib Path, not a string"""

    def convert(self, value, param, ctx):
        res = Path(super().convert(value, param, ctx))
        assert res.exists(), f"given file {res} does not exist"
        return res
