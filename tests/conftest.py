import os
from pathlib import Path

import pytest
from bs4 import BeautifulSoup
from sphinx.testing.path import path
from sphinx.testing.util import SphinxTestApp

pytest_plugins = "sphinx.testing.fixtures"
collect_ignore = ["roots"]

os.environ["SPHINX_AUTODOC_RELOAD_MODULES"] = "1"


@pytest.fixture()
def rootdir() -> path:
    """Top of the Sphinx document tree."""
    roots = path(os.path.dirname(__file__) or ".").abspath() / "roots"
    yield roots


@pytest.fixture
def srcdir(rootdir) -> Path:
    """Part of Sphinx wants path, part wants Path."""
    return Path(rootdir)


@pytest.fixture()
def content(app: SphinxTestApp) -> None:
    """The content generated from a Sphinx site."""
    app.build()
    yield app


@pytest.fixture()
def page(content: SphinxTestApp, request) -> BeautifulSoup:
    """Get the text for a page and convert to BeautifulSoup document."""
    page_name = request.param
    c = (content.outdir / page_name).read_text()

    yield BeautifulSoup(c, "html.parser")
