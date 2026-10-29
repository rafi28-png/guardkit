"""ShmPipe: zero-copy shared-memory pipes for polyglot data."""
from .core import list_pipes, read_pandas, read_table, remove, write_table

__version__ = "0.1.0"
__all__ = ["write_table", "read_table", "read_pandas", "list_pipes", "remove"]
