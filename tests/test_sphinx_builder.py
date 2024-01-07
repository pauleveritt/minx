from pathlib import Path

import pytest
from sphinx.testing.util import SphinxTestApp

from minx.sphinx_builder import make_app


@pytest.fixture
def sphinx_app(srcdir: Path) -> SphinxTestApp:
    return make_app(srcdir=srcdir / "test-sphinx-setup")


def test_make_app(sphinx_app):
    sphinx_app.build(filenames=["roots/test-sphinx-setup/index.rst"])
    assert sphinx_app.builder.name == "html"
    assert sphinx_app.outdir.endswith("html")
