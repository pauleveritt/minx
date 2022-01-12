"""Create an ``awatch`` iterable instance as a context var."""
from contextvars import ContextVar
from pathlib import Path

# Let's point at a docs dir two hops up
from watchgod import awatch

here_dir = Path(__file__).resolve().parent
docs_dir = here_dir.parent / "docs"
watcher = ContextVar("watcher", default=awatch(docs_dir))
