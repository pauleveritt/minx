"""Tests for constructing a Sphinx app for rendering."""
from pathlib import Path

import pytest
from sphinx.testing.util import SphinxTestApp

from minx.sphinx_builder import make_app


@pytest.fixture
def sphinx_app(srcdir: Path) -> SphinxTestApp:
    """Fixture for making a Sphinx test app."""
    return make_app(srcdir=srcdir / "test_sphinx_setup")


def test_make_app(sphinx_app):
    """Sphinx test app should be constructable."""
    sphinx_app.build(filenames=["roots/test_sphinx_setup/index.rst"])
    assert sphinx_app.builder.name == "html"
    assert sphinx_app.outdir.endswith("html")
