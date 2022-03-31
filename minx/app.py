import asyncio

from anyio import to_thread
from sphinx.application import Sphinx
from sphinx.util.docutils import patch_docutils, docutils_namespace
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from watchfiles import awatch, Change

WATCH_DIR = "docs"


async def homepage(request):
    return JSONResponse({'hello': 'world'})


app = Starlette(debug=True, routes=[
    Route('/', homepage),
])


class MySphinx(Sphinx):
    pass


def make_app():
    confdir = sourcedir = "docs"
    outputdir = doctreedir = "docs/_build"
    builder = "html"
    confoverrides = {}
    status = warning = None
    freshenv = False
    warningiserror = False
    tags = []
    verbosity = 0
    jobs = 0
    keep_going = False
    force_all = False
    filenames = []
    patch_docutils(confdir)
    docutils_namespace()
    app2 = MySphinx(
        srcdir=sourcedir,
        confdir=confdir,
        outdir=outputdir,
        buildername="html",
        doctreedir=doctreedir,
    )
    return app2


sphinx_app = make_app()


def build_docs():
    force_all = False
    filenames = ["docs/index.rst"]
    sphinx_app.build(force_all, filenames)
    return sphinx_app.statuscode


def my_filter(change: Change, filename: str) -> bool:
    return filename.endswith('.rst') and "build" not in filename


async def watch_changes():
    print(f"Watching changes in directory: {WATCH_DIR}")
    async for changes in awatch(WATCH_DIR, watch_filter=my_filter):
        await to_thread.run_sync(build_docs)


@app.on_event("startup")
async def app_startup():
    asyncio.create_task(watch_changes())


@app.on_event("shutdown")
async def shutdown_event():
    print("On shutdown")
