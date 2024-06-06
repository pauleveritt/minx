import asyncio
import contextlib
from pathlib import Path
from typing import AsyncIterator, TypedDict

from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route, Mount
from starlette.staticfiles import StaticFiles
from watchfiles import awatch, Change

from src.minx.sphinx_builder import MinxApp, make_app

HERE = Path(__file__).parent
PROJECT = HERE.parent.parent
VAR = PROJECT / "var"
TESTS = PROJECT / "tests"
DOCS = TESTS / "roots/test-sphinx-setup"


async def homepage(request) -> JSONResponse:
    """Root of the site."""
    return JSONResponse({"hello": "world"})


class State(TypedDict):
    """Provide some type info."""
    sphinx_app: Starlette


def my_filter(change: Change, filename: str) -> bool:  # noqa: D103
    return filename.endswith(".rst") and "build" not in filename


async def watch_changes(this_app: Starlette) -> None:  # noqa: D103
    print(f"Watching changes in directory: {DOCS}")
    async for changes in awatch(DOCS, watch_filter=my_filter):
        sphinx_app = make_app(srcdir=DOCS)
        sphinx_app.build()
        print(changes)


@contextlib.asynccontextmanager
async def lifespan(this_app: Starlette) -> AsyncIterator[State]:  # noqa: D103
    # sphinx_app = make_app(srcdir=DOCS)
    # sphinx_app.build()
    # noinspection PyAsyncCall
    asyncio.create_task(watch_changes(this_app))
    yield {"sphinx_app": app}


app = Starlette(
    debug=True,
    routes=[
        Mount("/root", app=StaticFiles(directory=VAR), name="var"),
        Route("/", homepage),
    ],
    lifespan=lifespan,
)
