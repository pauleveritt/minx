import asyncio
from time import time

from fastapi import FastAPI
from sphinx.application import Sphinx
from sphinx.util.docutils import patch_docutils, docutils_namespace
from watchgod import awatch

WATCH_DIR = "docs"
app = FastAPI()


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


async def watch_changes():
    print(f"Watching changes in directory: {WATCH_DIR}")
    async for changes in awatch(WATCH_DIR):
        print(changes)
        start = time()
        build_docs()
        elapsed = time() - start
        print(elapsed * 1000)


@app.on_event("startup")
async def app_startup():
    asyncio.create_task(watch_changes())


@app.on_event("shutdown")
async def shutdown_event():
    print("On shutdown")


@app.get("/")
def read_root():
    return {"Hello": "World"}
