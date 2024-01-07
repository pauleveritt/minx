import asyncio
from pathlib import Path

from anyio import to_thread
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from watchfiles import awatch, Change

from src.minx.sphinx_builder import make_app

HERE = Path(__file__).parent
PROJECT = HERE.parent.parent
TESTS = PROJECT / "tests"
DOCS = TESTS / "roots/test-sphinx-setup"


async def homepage(request):
    return JSONResponse({"hello": "world"})


app = Starlette(
    debug=True,
    routes=[
        Route("/", homepage),
    ],
)


def build_docs(this_sphinx_app):
    force_all = False
    filenames = ["docs/index.md"]
    this_sphinx_app.build(force_all, filenames)
    return this_sphinx_app.statuscode


def my_filter(change: Change, filename: str) -> bool:
    return filename.endswith(".rst") and "build" not in filename


async def watch_changes():
    sphinx_app = make_app(srcdir=DOCS)
    sphinx_app.build()
    print(f"Watching changes in directory: {DOCS}")
    async for changes in awatch(DOCS, watch_filter=my_filter):
        await to_thread.run_sync(build_docs, sphinx_app)


@app.on_event("startup")
async def app_startup():
    asyncio.create_task(watch_changes())


@app.on_event("shutdown")
async def shutdown_event():
    print("On shutdown")
